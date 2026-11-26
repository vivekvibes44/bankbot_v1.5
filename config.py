import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")

# Openrouter configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
TEST_EMBEDDING_MODEL = os.getenv("TEST_EMBEDDING_MODEL")