
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# LLM configuration
LLM_MODEL = os.getenv("LLM_MODEL")
