#!/usr/bin/env python3
"""
Main entry point for the ToDo App
Run this file to start the FastAPI server

Usage:
    python run.py
    or
    uvicorn run:app --reload
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )