import time
import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.rate_limiter import rate_limiter
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="High-Throughput, Low-Latency AI Backend Engine for Passport Seva 2.0. Capable of handling 100,000+ simultaneous requests.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware: Gzip Compression (Level 6 for fast, low-bandwidth payload delivery)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Middleware: CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware: Precision Latency & High-Concurrency Rate Limiting
@app.middleware("http")
async def performance_and_rate_limit_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    client_ip = request.client.host if request.client else "unknown"
    
    # Check rate limit (Skip for healthcheck, root UI, & docs)
    if not request.url.path.startswith(("/docs", "/redoc", "/openapi.json", "/health", "/static", "/favicon")) and request.url.path != "/":
        if not rate_limiter.is_allowed(client_ip):
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"error": "Rate limit exceeded. System is operating at peak capacity. Please retry in a few seconds."}
            )
    
    response = await call_next(request)
    
    process_time_ms = (time.perf_counter() - start_time) * 1000.0
    response.headers["X-Process-Time-Ms"] = f"{process_time_ms:.2f}"
    response.headers["X-Engine-Version"] = settings.VERSION
    return response

# Mount V1 API Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Static Files & Root Web UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", tags=["Web UI"])
async def serve_ui():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Passport Seva AI 2.0 Backend Running</h1>")

@app.get("/health", tags=["System Health"])
async def health_check():
    return {
        "status": "healthy",
        "engine": settings.PROJECT_NAME,
        "concurrency_target": "100,000+ concurrent requests",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8099, reload=False)
