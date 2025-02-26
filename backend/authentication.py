from passlib.hash import bcrypt

def verify_user(username: str, password: str):
    users_db = {"admin": bcrypt.hash("password123"), "guest": bcrypt.hash("guestpass")}
    if username in users_db and bcrypt.verify(password, users_db[username]):
        return True
    return False
# Compare this snippet from backend/main.py:
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
# import redis  # Import the Redis client
# from authentication import verify_user
#
# app = FastAPI()
# redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
# active_connections = {}
#
# @app.websocket("/ws/{session_id}/{user}")
# async def websocket_endpoint(websocket: WebSocket, session_id: str, user: str, authorized: bool = Depends(verify_user)):
#     if not authorized:
#         await websocket.close()
#         return
#
#     await websocket.accept()
#     active_connections[user] = websocket
#
#     try:
#         while True:
#             data = await websocket.receive_text()
#             redis_client.rpush(session_id, data)  # Append history for undo/redo
#             for conn in active_connections.values():
#                 await conn.send_text(f"{user} edited: {data}")
#     except WebSocketDisconnect:
#         del active_connections[user]
# Compare this snippet from backend/main.py:
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
# import redis  # Import the Redis client
# from authentication import verify_user
#
# app = FastAPI()