"""
Configuration management for AI Agent Tools Lab.
Loads environment variables and provides centralized configuration access.

配置管理模块
集中管理环境变量、API配置和路径设置
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()


class Config:
    """Central configuration for the application"""

    # ========================================
    # API Keys
    # ========================================
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # ========================================
    # API Endpoints
    # ========================================
    WEATHER_API_URL = os.getenv(
        "WEATHER_API_URL",
        "https://api.open-meteo.com/v1/forecast"
    )
    IPINFO_URL = os.getenv("IPINFO_URL", "https://ipinfo.io/json")

    # ========================================
    # Application Settings
    # ========================================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "auto")
    TEMPERATURE_UNIT = os.getenv("TEMPERATURE_UNIT", "fahrenheit")

    # ========================================
    # Paths
    # ========================================
    PROJECT_ROOT = Path(__file__).parent
    ASSETS_DIR = PROJECT_ROOT / "assets"
    OUTPUT_DIR = PROJECT_ROOT / "output"
    EXAMPLES_DIR = PROJECT_ROOT / "examples"

    @classmethod
    def validate(cls):
        """
        Validate required configuration.

        Raises:
            ValueError: If required configuration is missing
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "❌ OPENAI_API_KEY not found!\n"
                "Please follow these steps:\n"
                "1. Copy .env.example to .env\n"
                "2. Add your OpenAI API key to the .env file\n"
                "3. Get your API key from: https://platform.openai.com/api-keys"
            )

        print("✅ Configuration validated successfully!")

    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.ASSETS_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.EXAMPLES_DIR.mkdir(exist_ok=True)
        print(f"📁 Directory structure ready:")
        print(f"   - {cls.ASSETS_DIR}")
        print(f"   - {cls.OUTPUT_DIR}")
        print(f"   - {cls.EXAMPLES_DIR}")

    @classmethod
    def get_info(cls):
        """Print current configuration (without sensitive data)"""
        print("=" * 60)
        print("Current Configuration")
        print("=" * 60)
        print(f"API Key: {'✅ Set' if cls.OPENAI_API_KEY else '❌ Not Set'}")
        print(f"Weather API: {cls.WEATHER_API_URL}")
        print(f"IP Info URL: {cls.IPINFO_URL}")
        print(f"Temperature Unit: {cls.TEMPERATURE_UNIT}")
        print(f"Timezone: {cls.DEFAULT_TIMEZONE}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print("=" * 60)


# Validate configuration and ensure directories on import
# This runs when the module is first imported
try:
    Config.validate()
    Config.ensure_directories()
except ValueError as e:
    print(f"\n⚠️  Configuration Error:\n{e}\n")
    # Don't raise exception, allow import to succeed
    # but tools may fail when actually used
