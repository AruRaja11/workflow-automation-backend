from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_key: str = Field(
        validation_alias=AliasChoices("OPENAI_API_KEY", "OPENAI_KEY")
    )
    apify_key: str = Field(
        validation_alias=AliasChoices("APIFY_API_TOKEN", "APIFY_TOKEN", "APIFY_KEY")
    )

    db_url: str = Field(
        validation_alias=AliasChoices("SUPABASE_DB_URL", "DATABASE_URL")
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


setting = Settings()
