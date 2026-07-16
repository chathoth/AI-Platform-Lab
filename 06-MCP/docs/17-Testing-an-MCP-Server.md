# 17 - Testing an MCP Server

## Introduction

Module 05 chapter 09 built a real evaluation harness for a RAG
pipeline instead of trusting "it looked right in a manual test."
This chapter applies the same discipline to an MCP server — automated
tests that call real tools through a real client connection. It also
includes a genuine gotcha found while verifying this chapter: a
tempting fixture pattern that looks correct but fails intermittently,
and the pattern that actually works reliably.

## Learning Objectives

After this chapter I should be able to:

-   Write a pytest test that spins up a server and calls its tools.
-   Avoid a specific async-fixture pitfall with MCP's `stdio_client`.
-   Test error paths (chapter 12) and schema regressions, not just
    happy-path behavior.

------------------------------------------------------------------------

# A Pattern That Looks Right But Isn't: Shared Async Fixtures

``` python
# tempting, but flaky - DON'T do this
@pytest.fixture
async def session():
    params = StdioServerParameters(command="python3", args=["server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            yield s
```

Tested directly: every individual assertion using this fixture passed,
but the test run reported errors anyway — `RuntimeError: Attempted to
exit cancel scope in a different task than it was entered in`. The
fixture's `stdio_client` context manager opens an `anyio` task group
that doesn't consistently tear down cleanly across pytest-asyncio's
per-test task boundaries. The tests were right; the fixture pattern
around them wasn't reliable.

## The Pattern That Actually Works: Connect Inside Each Test

``` python
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER = StdioServerParameters(command="python3", args=["server.py"])

@pytest.mark.asyncio
async def test_get_disk_usage_known_host():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("get_disk_usage", {"hostname": "db-primary-01"})
            assert "92" in result.content[0].text

@pytest.mark.asyncio
async def test_get_disk_usage_unknown_host_returns_structured_error():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("get_disk_usage", {"hostname": "totally-made-up-host"})
            assert "error" in result.content[0].text.lower()
```

Verified: both tests pass cleanly, every run, with no teardown errors —
each test opens and closes its own connection within a single task,
never crossing a task boundary the way the shared fixture did. Slightly
more repetition per test, in exchange for actually being reliable.

**This is worth internalizing as a general lesson, not just an MCP
one:** a test suite that "passes" with errors in the output is still
broken — investigate teardown noise instead of ignoring it because the
assertions happened to succeed.

## Testing Discovery and Schema, Not Just Behavior

``` python
@pytest.mark.asyncio
async def test_server_exposes_expected_tools():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            assert "get_disk_usage" in {t.name for t in tools.tools}

@pytest.mark.asyncio
async def test_tool_schema_has_required_hostname_param():
    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            disk_tool = next(t for t in tools.tools if t.name == "get_disk_usage")
            assert "hostname" in disk_tool.inputSchema["required"]
```

Verified passing alongside the two behavior tests above. The schema
test catches exactly the kind of regression that's easy to introduce
by accident — renaming a parameter, or forgetting `@mcp.tool()` on a
new function — before it reaches anyone actually connecting to the
server.

## Interactive Exploration With the MCP Inspector

For fast, manual exploration without writing a test file at all:

``` bash
npx @modelcontextprotocol/inspector python3 server.py
```

This opens a browser-based UI showing every tool, resource, and prompt
the server exposes, letting you call them interactively — genuinely
useful for a first pass of "does this server even do what I think it
does" before writing formal tests, the same role a tool like Postman
plays for exploring a REST API before writing integration tests
against it.

## Hands-on: Reproduce Both the Failure and the Fix

``` bash
pip install mcp pytest pytest-asyncio
```

Using chapter 08's server file, write the shared-fixture version first
and run it — reproduce the cancel-scope error yourself. Then rewrite it
using the per-test connection pattern and confirm it passes cleanly.
Seeing the actual failure, not just reading about it, is what makes
this gotcha stick.

## Common Misconceptions

❌ A pytest fixture is always the right way to share setup across
async tests.
(Verified directly: a shared async-generator fixture wrapping
`stdio_client` produces intermittent teardown errors — connecting
inside each test is more repetitive but reliable.)

❌ "4 passed, 4 errors" in test output means the 4 real tests are
broken.
(In this specific case, the assertions genuinely passed — the errors
were fixture teardown noise. Still worth treating as a real problem to
fix, not something to ignore because the assertions happened to
succeed.)

✔ Testing a tool's schema (not just its runtime output) catches
regressions that testing behavior alone would miss — a renamed
parameter breaks every client's assumptions even if the function
itself still "works."

## Interview Questions

1.  What specific error does a shared async-generator fixture produce
    with MCP's `stdio_client`, and why?
2.  What's the more reliable alternative pattern, and what does it
    cost in exchange for reliability?
3.  Why shouldn't "the assertions passed" be the only thing that
    matters when a test run reports errors?
4.  Why test a tool's schema specifically, separate from its runtime
    behavior?

## Summary

Testing an MCP server means spinning up a real server subprocess and
calling it through a real client connection — but a shared async
fixture wrapping `stdio_client` is a verified pitfall, producing
intermittent cancel-scope errors across pytest-asyncio's task
boundaries. Connecting inside each test individually is more
repetitive but reliable, confirmed directly rather than assumed.

## Next Chapter

➡️ `18-Best-Practices.md`
