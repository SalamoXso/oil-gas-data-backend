import asyncio
import platform
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.scarpers.trrc_scraper import scrape_trrc  # Import your scraper function

# Set the event loop policy for Windows
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Endpoint to trigger scraping
@app.post("/api/v1/scrape/")
def trigger_scrape(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(scrape_trrc)
        return {"message": "Scraping started in the background."}
    except Exception as e:
        logger.error(f"Error triggering scrape: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Define the /api/v1/flares/ endpoint
@app.get("/api/v1/flares/")
def get_flares():
    return [
        {
            "id": 1,
            "volume": 100.5,
            "duration": 2.5,
            "h2s": 0.5,
            "date": "2023-10-01T00:00:00",
            "latitude": 28.519861,
            "longitude": -98.463806,
            "location": "BOR FACILITY",
            "operator": "SILVERBOW RESOURCES OPER, LLC",
        }
    ]