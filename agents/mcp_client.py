"""Thin sync MCP client: spawns a stdio server, discovers tools, exposes
them as LangChain tools. Hand-rolled to show what adapter libraries do."""
import sys, pathlib, asyncio, threading
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from contextlib import AsyncExitStack
from pydantic import create_model
from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

_TYPES = {"string": str, "integer": int, "number": float, "boolean": bool}

class MCPClient:
    def __init__(self, command, args, env=None):
        self._loop = asyncio.new_event_loop()
        threading.Thread(target=self._loop.run_forever, daemon=True).start()
        self._params = StdioServerParameters(command=command, args=args, env=env or {})
        self._stack, self.session = None, None
        self._run(self._connect())

    def _run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result(timeout=120)

    async def _connect(self):
        self._stack = AsyncExitStack()
        read, write = await self._stack.enter_async_context(stdio_client(self._params))
        self.session = await self._stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()

    def list_tools(self):
        return self._run(self.session.list_tools()).tools

    def call_tool(self, name, args):
        res = self._run(self.session.call_tool(name, args))
        return "\n".join(c.text for c in res.content if getattr(c, "text", None))

    def langchain_tools(self):
        """Discover server tools and wrap each as a LangChain StructuredTool."""
        out = []
        for t in self.list_tools():
            props = (t.inputSchema or {}).get("properties", {})
            required = set((t.inputSchema or {}).get("required", []))
            fields = {}
            for pname, spec in props.items():
                ptype = _TYPES.get(spec.get("type", "string"), str)
                default = ... if pname in required else spec.get("default", "")
                fields[pname] = (ptype, default)
            schema = create_model(f"{t.name}_args", **fields)

            def make_fn(tool_name):
                def fn(**kwargs):
                    return self.call_tool(tool_name, kwargs)
                return fn

            out.append(StructuredTool.from_function(
                func=make_fn(t.name), name=t.name,
                description=t.description or "", args_schema=schema))
        return out

if __name__ == "__main__":
    import os
    root = pathlib.Path(__file__).parent.parent
    client = MCPClient(
        command=sys.executable,
        args=[str(root / "mcp_server" / "server.py")],
        env={**os.environ, "MERIDIAN_EMPLOYEE_ID": "emp-001"})
    tools = client.langchain_tools()
    print("discovered:", [t.name for t in tools])
    gl = next(t for t in tools if t.name == "lookup_glossary")
    print(gl.invoke({"term": "EOB"}))