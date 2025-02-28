import websockets
import asyncio
import json
import sys
from colorama import Fore, Style
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

async def edit_session(session_id, user):
    """Connect to WebSocket and start collaborative editing"""
    uri = f"ws://localhost:8000/ws/{session_id}/{user}"
    async with websockets.connect(uri) as websocket:
        print(f"{Fore.YELLOW}Connected to session {session_id} as {user}{Style.RESET_ALL}")

        while True:
            command = input(f"{Fore.YELLOW}Enter command (edit/run/undo/redo/chat/exit): {Style.RESET_ALL}")

            if command.lower() == "edit":
                code = input("Enter code: ")
                highlighted_code = highlight(code, PythonLexer(), TerminalFormatter())
                print(highlighted_code)
                await websocket.send(json.dumps({"action": "code_update", "code": code}))

            elif command.lower() == "run":
                await websocket.send(json.dumps({"action": "execute"}))

            elif command.lower() == "undo":
                await websocket.send(json.dumps({"action": "undo"}))

            elif command.lower() == "redo":
                await websocket.send(json.dumps({"action": "redo"}))

            elif command.lower() == "chat":
                message = input("Enter message: ")
                await websocket.send(json.dumps({"action": "chat", "message": message}))

            elif command.lower() == "exit":
                break

async def receive_messages(websocket):
    """Handle incoming WebSocket messages"""
    while True:
        response = await websocket.recv()
        response_data = json.loads(response)
        if response_data.get("action") == "chat":
            print(f"{Fore.CYAN}{response_data['user']}: {response_data['message']}{Style.RESET_ALL}")

if __name__ == "__main__":
    session_id = sys.argv[1]
    user = input("Enter your username: ")
    asyncio.run(edit_session(session_id, user))
# import websockets
# import asyncio
# import sys
# import colorama
# from colorama import Fore, Style
# from pygments import highlight
# from pygments.lexers import PythonLexer
# from pygments.formatters import TerminalFormatter

# async def edit_session(session_id, user):
#     uri = f"ws://localhost:8000/ws/{session_id}/{user}"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             code = input(f"{Fore.YELLOW}Enter code: {Style.RESET_ALL}")
#             highlighted_code = highlight(code, PythonLexer(), TerminalFormatter())
#             print(highlighted_code)
#             if code.lower() == "undo":
#                 await websocket.send("UNDO")
#             elif code.lower() == "redo":
#                 await websocket.send("REDO")
#             elif code.lower() == "run":
#                 await websocket.send("EXECUTE")
#             else:
#                 await websocket.send(code)
#             response = await websocket.recv()
#             print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")

# if __name__ == "__main__":
#     session_id = sys.argv[1]
#     user = input("Enter your username: ")
#     asyncio.run(edit_session(session_id, user))
