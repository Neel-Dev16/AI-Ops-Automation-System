import os


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODE = os.getenv("LLM_MODE", "mock")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aiops.db")
