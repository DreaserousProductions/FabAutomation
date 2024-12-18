import os
from dotenv import load_dotenv

load_dotenv()

USER_DATA_DIR = os.getenv("USER_DATA_DIR")
USER_AGENT = os.getenv("USER_AGENT")
WEBSITE_URL = "https://fab.com/portal/listings"
# CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH") or "chromedriver"  # Default to 'chromedriver' if not set
