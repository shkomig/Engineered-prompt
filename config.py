"""Configuration settings for the Engineered Prompt system."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prompts.db")

# Templates directory
TEMPLATES_DIR = BASE_DIR / "src" / "templates"

# Application settings
APP_NAME = "Engineered Prompt"
APP_VERSION = "0.1.0"
