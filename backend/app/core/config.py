from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT / "backend" / ".env", extra="ignore")

    secret_key: str = "change-me"
    access_token_minutes: int = 60 * 8
    admin_emails: list[str] = []
    database_url: str = f"sqlite:///{ROOT / 'backend' / 'policymind.db'}"
    policies_dir: Path = ROOT / "documents" / "policies"
    vectorstore_dir: Path = ROOT / "vectorstore"
    frontend_dir: Path = ROOT / "frontend"
    cors_origins: list[str] = ["http://127.0.0.1:5500", "http://localhost:5500"]
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    top_k: int = 4
    min_score: float = 0.35  # below this similarity -> "not found"
    gemini_api_key: str = ""
    llm_model: str = "gemini-2.5-flash"


settings = Settings()
