from fastapi import FastAPI, HTTPException, Query
from contextlib import asynccontextmanager
from app.models import CheckResponse
from app.core import CategoryChecker
import logging
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

checker = CategoryChecker()

async def background_refresh_task():
    """Background task that checks every 10 minutes if lists need refreshing."""
    logger.info("Background refresh task started")
    try:
        while True:
            await asyncio.sleep(600)  # Sleep for 10 minutes
            await checker.refresh_if_needed()
    except asyncio.CancelledError:
        logger.info("Background refresh task cancelled")
        raise

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load lists on startup
    logger.info("Loading blocklists...")
    checker.load_all()
    logger.info("Blocklists loaded.")

    # Start background refresh task
    refresh_task = asyncio.create_task(background_refresh_task())

    yield

    # Cleanup: cancel background task
    refresh_task.cancel()
    try:
        await refresh_task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="URLSafe", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "urlsafe"}

# Shared logic
def process_check(url: str) -> CheckResponse:
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")

    categories = checker.check_url(url)

    # Logic: is_safe if no categories match (excluding social)
    # However, 'porn' covers 'adult' as per requirements
    categories["adult"] = categories.get("porn", False)

    # Social is considered safe
    unsafe_categories = [v for k, v in categories.items() if k != "social"]
    is_safe = not any(unsafe_categories)

    return CheckResponse(
        url=url,
        is_safe=is_safe,
        categories=categories
    )

@app.get("/check", response_model=CheckResponse)
def check_url(url: str = Query(..., description="The URL to check")):
    return process_check(url)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
