import typer
import subprocess
import colorama
from colorama import Fore, Style

app = typer.Typer()

def print_info(message):
    typer.echo(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

def print_error(message):
    typer.echo(f"{Fore.RED}{message}{Style.RESET_ALL}")

def print_success(message):
    typer.echo(f"{Fore.GREEN}{message}{Style.RESET_ALL}")

@app.command()
def new(filename: str):
    """Start a new collaborative session"""
    print_info(f"Starting session for {filename}")
    subprocess.run(["python", "backend/main.py", filename])

@app.command()
def join(session_id: str):
    """Join an existing session"""
    print_info(f"Joining session {session_id}")
    subprocess.run(["python", "backend/editor.py", session_id])

@app.command()
def list_sessions():
    """List active sessions"""
    print_info("Fetching active sessions...")
    subprocess.run(["python", "backend/database.py", "list"])

if __name__ == "__main__":
    app()
