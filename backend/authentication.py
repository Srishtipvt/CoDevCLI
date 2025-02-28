from passlib.hash import bcrypt
import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

users_db = {
    "admin": bcrypt.hash("password123"),
    "guest": bcrypt.hash("guestpass")
}

def verify_user(username: str, password: str) -> bool:
    """Verify user credentials"""
    if username in users_db and bcrypt.verify(password, users_db[username]):
        return True
    return False

def create_session(username: str):
    """Create a session for the user"""
    session_token = bcrypt.hash(username)
    redis_client.set(username, session_token)
    return session_token

def validate_session(username: str, token: str) -> bool:
    """Validate user session"""
    return redis_client.get(username) == token

# from passlib.hash import bcrypt

# users_db = {
#     "admin": bcrypt.hash("password123"),
#     "guest": bcrypt.hash("guestpass")
# }

# def verify_user(username: str, password: str) -> bool:
#     print(f"Verifying user: {username}")  # Debugging

#     if username in users_db and bcrypt.verify(password, users_db[username]):
#         print(f"User {username} is authorized")
#         return True

#     print(f"User {username} is NOT authorized")
#     return False
# # Compare this snippet from backend/main.py:
# # from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, Query, HTTPException
# # import redis
# # from backend.authentication import verify_user        # <--- Add this line
# # from fastapi.middleware.cors import CORSMiddleware
# #
# # origins = [                                         # <--- Add this block