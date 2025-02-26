from passlib.hash import bcrypt

users_db = {
    "admin": bcrypt.hash("password123"),
    "guest": bcrypt.hash("guestpass")
}

def verify_user(username: str, password: str) -> bool:
    print(f"Verifying user: {username}")  # Debugging

    if username in users_db and bcrypt.verify(password, users_db[username]):
        print(f"User {username} is authorized")
        return True

    print(f"User {username} is NOT authorized")
    return False
# Compare this snippet from backend/main.py:
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
# import redis
# from backend.authentication import verify_user        # <--- Add this line
# from fastapi.middleware.cors import CORSMiddleware
#
# origins = [                                         # <--- Add this block