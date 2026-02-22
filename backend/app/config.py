import os


class Settings:
	def __init__(self) -> None:
		self.environment = os.getenv("ENVIRONMENT", "local")

		origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000")
		self.cors_allow_origins = [o.strip() for o in origins.split(",") if o.strip()]

		self.database_url = os.getenv("DATABASE_URL", "")

		self.log_level = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
