import subprocess
import asyncio

async def stream_execution_output(websocket, code):
    """Execute Python code and stream output"""
    process = await asyncio.create_subprocess_exec(
        "python3", "-c", code,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async for line in process.stdout:
        await websocket.send_json({"action": "execution_output", "output": line.decode().strip()})

    async for line in process.stderr:
        await websocket.send_json({"action": "execution_output", "output": f"ERROR: {line.decode().strip()}"})
