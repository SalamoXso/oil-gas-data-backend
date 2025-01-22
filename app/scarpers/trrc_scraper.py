import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from app.models.flare import Flare
from app.models.location import Location
from app.models.operator import Operator
from app.utils.database import SessionLocal
import logging
from datetime import datetime
from multiprocessing import Process

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def save_flare_data(flare_data):
    """Save flare data to the database."""
    db = SessionLocal()
    try:
        # Check if location and operator already exist
        location = db.query(Location).filter(Location.name == flare_data["fv_district"]).first()
        if not location:
            location = Location(name=flare_data["fv_district"], coordinates="0,0")
            db.add(location)
            db.commit()
            logger.info(f"Created new location: {location.name}")

        operator = db.query(Operator).filter(Operator.name == flare_data["operator_name"]).first()
        if not operator:
            operator = Operator(name=flare_data["operator_name"])
            db.add(operator)
            db.commit()
            logger.info(f"Created new operator: {operator.name}")

        # Create flare entry
        flare = Flare(
            exception_number=flare_data["exception_number"],
            submittal_date=datetime.strptime(flare_data["submittal_date"], "%m/%d/%Y"),
            filing_number=flare_data["filing_number"],
            status=flare_data["status"],
            filing_type=flare_data["filing_type"],
            operator_number=flare_data["operator_number"],
            operator_name=flare_data["operator_name"],
            property=flare_data["property"],
            effective_date=datetime.strptime(flare_data["effective_date"], "%m/%d/%Y") if flare_data["effective_date"] else None,
            expiration_date=datetime.strptime(flare_data["expiration_date"], "%m/%d/%Y") if flare_data["expiration_date"] else None,
            fv_district=flare_data["fv_district"],
            location_id=location.id,
            operator_id=operator.id,
        )
        db.add(flare)
        db.commit()
        logger.info(f"Created new flare: {flare.id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error saving data to database: {e}")
        raise
    finally:
        db.close()

async def _scrape_trrc():
    browser = None
    try:
        logger.info("Starting scraping process...")
        async with async_playwright() as p:
            # Launch a browser
            browser = await p.chromium.launch(headless=False)  # Set headless=False for debugging
            page = await browser.new_page()

            # Navigate to the SWR-32 Public Query page
            logger.info("Navigating to the SWR-32 Public Query page...")
            await page.goto("https://webapps.rrc.state.tx.us/swr32/publicquery.xhtml")
            logger.info("Page loaded.")

            # Wait for the search button to be visible
            logger.info("Waiting for the search button to be visible...")
            await page.wait_for_selector("#pbqueryForm\\:searchExceptions", state="visible")
            logger.info("Search button is visible.")

            # Click the search button
            logger.info("Clicking the search button...")
            await page.click("#pbqueryForm\\:searchExceptions")
            logger.info("Search button clicked.")

            # Wait for the results to load
            logger.info("Waiting for results to load...")
            await page.wait_for_selector("#pbqueryForm\\:pQueryTable", timeout=30000)  # Increase timeout if needed
            logger.info("Results loaded.")

            while True:
                # Add a delay to ensure the results are fully loaded
                await asyncio.sleep(2)  # Adjust the delay as needed

                # Extract the HTML content of the results table
                html = await page.inner_html("#pbqueryForm\\:pQueryTable")
                logger.info("HTML content of the results table extracted.")

                # Parse the HTML using BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")
                rows = soup.select("tr.ui-widget-content")
                logger.info(f"Found {len(rows)} rows on this page.")

                # Process and save data for the current page
                for row in rows:
                    columns = row.find_all("td")
                    if len(columns) >= 11:  # Ensure the row has enough columns
                        flare_data = {
                            "exception_number": columns[1].text.strip(),
                            "submittal_date": columns[2].text.strip(),
                            "filing_number": columns[3].text.strip(),
                            "status": columns[4].text.strip(),
                            "filing_type": columns[5].text.strip(),
                            "operator_number": columns[6].text.strip(),
                            "operator_name": columns[7].text.strip(),
                            "property": columns[8].text.strip(),
                            "effective_date": columns[9].text.strip(),
                            "expiration_date": columns[10].text.strip(),
                            "fv_district": columns[11].text.strip(),
                        }
                        await save_flare_data(flare_data)  # Save data to the database in real-time

                # Check if there is a next page
                next_button = page.locator("a.ui-paginator-next:not(.ui-state-disabled)").first  # Use .first to select the top "Next" button
                if await next_button.count() == 0:
                    break  # No more pages

                # Click the "Next" button
                logger.info("Navigating to the next page...")
                await next_button.click()

                # Wait for the results to load on the next page
                await page.wait_for_selector("#pbqueryForm\\:pQueryTable", timeout=30000)
                logger.info("Next page loaded.")

    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        raise
    finally:
        # Ensure the browser is closed even if an error occurs
        if browser:
            await browser.close()
            logger.info("Browser closed.")
        logger.info("Scraping process completed.")

def scrape_trrc():
    # Run the scraper in a separate process
    process = Process(target=_run_scraper)
    process.start()
    process.join()

def _run_scraper():
    # Create a new event loop for the subprocess
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_scrape_trrc())
    loop.close()