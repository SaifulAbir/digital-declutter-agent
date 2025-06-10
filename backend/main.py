"""
Digital Declutter Agent API

A FastAPI application for AI-powered digital cleanup and organization.
This module provides the main application setup and basic health endpoints.
"""

from fastapi import FastAPI

# Initialize FastAPI application with metadata
# These parameters appear in the auto-generated OpenAPI documentation
app = FastAPI(
    title="Digital Declutter Agent",
    description="AI-powered digital cleanup and organization",
    version="1.0.0",
)


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.

    This serves as the main entry point for the API and provides
    basic information about the service.

    Returns:
        dict: A dictionary containing a welcome message
    """
    return {"message": "Digital Declutter Agent API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
