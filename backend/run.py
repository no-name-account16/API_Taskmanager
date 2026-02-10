"""
Simple launcher for Task Manager Application
Usage: python run.py
"""
import uvicorn
import webbrowser
import time
from threading import Timer


def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)  # Wait 2 seconds for server to start
    webbrowser.open('http://localhost:8000')


if __name__ == '__main__':
    print("=" * 70)
    print("  Starting Task Manager Application")
    print("=" * 70)
    print()
    print("  Application URL: http://localhost:8000")
    print("  API Documentation: http://localhost:8000/docs")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 70)
    print()

    # Open browser in background thread
    Timer(2, open_browser).start()

    # Start the FastAPI application.\
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
