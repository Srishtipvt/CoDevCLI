from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
import redis
from backend.authentication import verify_user
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost", "http://localhost:8000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
active_connections = {}

@app.websocket("/ws/{session_id}/{user}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, user: str):
    try:
        # Extract password from query params
        query_params = websocket.query_params
        password = query_params.get("password")

        print(f"Attempting to verify user: {user}")

        if not password or not verify_user(user, password):
            print(f"User {user} is unauthorized. Closing connection.")
            await websocket.accept()  # WebSocket must be accepted before closing
            await websocket.close(code=1008)  # 1008 = Policy Violation
            return

        print(f"User {user} authorized. Connection accepted.")
        await websocket.accept()
        active_connections[user] = websocket

        while True:
            data = await websocket.receive_text()
            redis_client.rpush(session_id, data)  # Append history for undo/redo

            # Broadcast message to all active connections
            for conn_user, conn in active_connections.items():
                if conn_user != user:  # Avoid sending to self
                    await conn.send_text(f"{user} edited: {data}")

    except WebSocketDisconnect:
        print(f"User {user} disconnected")
        if user in active_connections:
            del active_connections[user]
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()
