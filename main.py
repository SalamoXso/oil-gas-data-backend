import asyncio
import platform
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import logging
from app.scarpers.trrc_scraper import scrape_trrc  # Import your scraper function
from app.utils.database import get_db  # Import your database setup
from app.models.flare import Flare  # Import the Flare model

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
    allow_origins=["https://oil-gas-data-frontend.onrender.com"],  # Allow requests from your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Global state to track scraping progress
scraping_state = {
    "is_running": False,
    "rows_scraped": 0,
}

@app.post("/api/v1/scrape/")
def trigger_scrape(background_tasks: BackgroundTasks):
    if scraping_state["is_running"]:
        raise HTTPException(status_code=400, detail="Scraping is already running.")

    scraping_state["is_running"] = True
    scraping_state["rows_scraped"] = 0

    background_tasks.add_task(scrape_trrc, scraping_state)  # Pass scraping_state
    return {"message": "Scraping started in the background."}

@app.post("/api/v1/stop-scrape/")
def stop_scrape():
    if not scraping_state["is_running"]:
        raise HTTPException(status_code=400, detail="Scraping is not running.")

    scraping_state["is_running"] = False  # This should stop the scraping loop
    return {"message": "Scraping stopped."}

@app.get("/api/v1/scraping-progress/")
def get_scraping_progress():
    return {
        "is_running": scraping_state["is_running"],
        "rows_scraped": scraping_state["rows_scraped"],
    }

# Endpoint to fetch flares data
@app.get("/api/v1/flares/")
def get_flares(db: Session = Depends(get_db)):
    try:
        flares = db.query(Flare).all()
        return [
            {
                "id": flare.id,
                "exception_number": flare.exception_number,
                "submittal_date": flare.submittal_date.isoformat() if flare.submittal_date else None,
                "filing_number": flare.filing_number,
                "status": flare.status,
                "filing_type": flare.filing_type,
                "operator_number": flare.operator_number,
                "operator_name": flare.operator_name,
                "property": flare.property,
                "effective_date": flare.effective_date.isoformat() if flare.effective_date else None,
                "expiration_date": flare.expiration_date.isoformat() if flare.expiration_date else None,
                "fv_district": flare.fv_district,
                "location_id": flare.location_id,
                "operator_id": flare.operator_id,
                "volume": flare.volume if hasattr(flare, "volume") else None,
                "duration": flare.duration if hasattr(flare, "duration") else None,
                "h2s": flare.h2s if hasattr(flare, "h2s") else None,
                "date": flare.date.isoformat() if flare.date else None,
                "latitude": float(flare.location.coordinates.split(",")[0].strip()) if flare.location and flare.location.coordinates else None,  # Parse latitude
                "longitude": float(flare.location.coordinates.split(",")[1].strip()) if flare.location and flare.location.coordinates else None,  # Parse longitude
                "location": flare.location.name if flare.location else "Unknown",
                "operator": flare.operator.name if flare.operator else "Unknown",
            }
            for flare in flares
        ]
    except Exception as e:
        logger.error(f"Error fetching flares: {e}")
        raise HTTPException(status_code=500, detail=str(e))
