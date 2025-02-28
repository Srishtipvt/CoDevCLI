import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def save_code(session_id, code):
    """Save code in Redis for undo/redo"""
    redis_client.rpush(session_id, code)

def get_latest_code(session_id):
    """Retrieve the latest code from Redis"""
    return redis_client.lindex(session_id, -1)

def undo_code(session_id):
    """Undo last change"""
    if redis_client.llen(session_id) > 1:
        redis_client.rpop(session_id)
    return get_latest_code(session_id)

def redo_code(session_id):
    """Redo last undone change (not implemented yet)"""
    return get_latest_code(session_id)

def list_sessions():
    """List all active sessions"""
    return redis_client.keys("*")

# import redis
# import sys

# redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# def save_code(session_id, code):
#     redis_client.rpush(session_id, code)  # Save multiple versions for undo/redo

# def get_code(session_id):
#     return redis_client.lindex(session_id, -1)  # Get latest entry

# def list_sessions():
#     keys = redis_client.keys("*")
#     print("Active Sessions:")
#     for key in keys:
#         print(f"- {key}")

# if __name__ == "__main__" and len(sys.argv) > 1:
#     if sys.argv[1] == "list":
#         list_sessions()
