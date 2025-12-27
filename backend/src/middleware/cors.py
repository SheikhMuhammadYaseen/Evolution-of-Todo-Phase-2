"""
CORS middleware configuration.
Allows Next.js frontend to communicate with FastAPI backend.
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from src.config import settings


def setup_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,  # Next.js dev server
        allow_credentials=True,  # Required for cookies
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Authorization", "Content-Type"],
    )
