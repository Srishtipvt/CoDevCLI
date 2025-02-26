import websockets
import asyncio
import sys
import colorama
from colorama import Fore, Style
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

async def edit_session(session_id, user):
    uri = f"ws://localhost:8000/ws/{session_id}/{user}"
    async with websockets.connect(uri) as websocket:
        while True:
            code = input(f"{Fore.YELLOW}Enter code: {Style.RESET_ALL}")
            highlighted_code = highlight(code, PythonLexer(), TerminalFormatter())
            print(highlighted_code)
            if code.lower() == "undo":
                await websocket.send("UNDO")
            elif code.lower() == "redo":
                await websocket.send("REDO")
            elif code.lower() == "run":
                await websocket.send("EXECUTE")
            else:
                await websocket.send(code)
            response = await websocket.recv()
            print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")

if __name__ == "__main__":
    session_id = sys.argv[1]
    user = input("Enter your username: ")
    asyncio.run(edit_session(session_id, user))
