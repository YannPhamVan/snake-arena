from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, leaderboard, sessions

app = FastAPI(
    title="Snake Arena API",
    description="API for the Snake Arena game",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(leaderboard.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")

@app.get("/api")
async def root():
    return {"message": "Welcome to Snake Arena API"}

# Serve static files (SPA) if static directory exists (Unified Deployment)
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.gzip import GZipMiddleware

# Enable Gzip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

static_dir = os.path.join(os.getcwd(), "static")
if os.path.isdir(static_dir):
    # Mount assets folder
    if os.path.isdir(os.path.join(static_dir, "assets")):
        app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

    # Catch-all for SPA handling
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Allow API routes to pass through (just in case, though they match first)
        if full_path.startswith("api"):
             return {"error": "Not Found", "status": 404}
        
        # Check if actual file exists (e.g., favicon.ico, robots.txt)
        file_path = os.path.join(static_dir, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Fallback to index.html
        return FileResponse(os.path.join(static_dir, "index.html"))
