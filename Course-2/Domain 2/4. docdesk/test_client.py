"""
test_client.py
---------------
RUNNABLE DEMO (Part A): connect to the DocDesk MCP server and prove it works.

This speaks the SAME protocol (MCP over stdio) that Claude Code uses when it
launches a server from .mcp.json. It:

  1. starts mcp_servers/docdesk_server.py,
  2. lists the server's TOOLS (with their descriptions),
  3. lists the server's RESOURCES (the document catalog),
  4. CALLS a tool (load_document) and prints the result,
  5. READS the catalog resource and prints it.

Run it:
    pip install -r requirements.txt      # installs the 'mcp' package
    python test_client.py

You normally never do this by hand — Claude Code connects for you. We run it
here only to SHOW, live, exactly what Claude Code sees when it connects.
"""

import os
import sys
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    # Tell the server where the documents are (same env var .mcp.json sets).
    env = dict(os.environ)
    env.setdefault("DOCDESK_DOCS_DIR",
                   os.path.join(os.path.dirname(__file__), "documents"))

    # Launch the server exactly like .mcp.json would: python docdesk_server.py
    server = StdioServerParameters(
        command=sys.executable,
        args=[os.path.join("mcp_servers", "docdesk_server.py")],
        env=env,
    )

    print("Connecting to the DocDesk MCP server (over stdio)...\n")
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 1) TOOLS the server exposes
            print("=" * 62)
            print("TOOLS discovered on the server:")
            print("=" * 62)
            tools = await session.list_tools()
            for t in tools.tools:
                desc = (t.description or "").split("\n")[0]
                print(f"  • {t.name}")
                print(f"      {desc}")

            # 2) RESOURCES the server exposes (the content catalog)
            print("\n" + "=" * 62)
            print("RESOURCES discovered on the server:")
            print("=" * 62)
            resources = await session.list_resources()
            if not resources.resources:
                print("  (none)")
            for r in resources.resources:
                print(f"  • {r.uri}  —  {r.name}")

            # 3) CALL a tool: load_document
            print("\n" + "=" * 62)
            print("CALLING tool: load_document('returns_policy.md')")
            print("=" * 62)
            result = await session.call_tool(
                "load_document", {"name": "returns_policy.md"})
            for block in result.content:
                if getattr(block, "text", None):
                    print(block.text[:300])

            # 4) READ the catalog resource
            print("\n" + "=" * 62)
            print("READING resource: docdesk://catalog")
            print("=" * 62)
            catalog = await session.read_resource("docdesk://catalog")
            for block in catalog.contents:
                if getattr(block, "text", None):
                    print(block.text)

    print("\nDone. This is exactly what Claude Code sees when it connects to")
    print("the 'docdesk' server configured in .mcp.json.")


if __name__ == "__main__":
    asyncio.run(main())
