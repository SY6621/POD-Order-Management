# -*- coding: utf-8 -*-
"""配置管理模块"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    IMAP_SERVER: str = os.getenv("IMAP_SERVER", "imap.qq.com")
    IMAP_PORT: int = int(os.getenv("IMAP_PORT", "993"))
    EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS", "")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")
    
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    ASSETS_DIR: Path = BASE_DIR / "assets"
    TEMPLATES_DIR: Path = ASSETS_DIR / "templates"
    FONTS_DIR: Path = ASSETS_DIR / "fonts"
    OUTPUT_DIR: Path = BASE_DIR / "output"
    
    @classmethod
    def validate(cls) -> bool:
        errors = []
        if not cls.EMAIL_ADDRESS:
            errors.append("EMAIL_ADDRESS 未配置")
        if not cls.EMAIL_PASSWORD:
            errors.append("EMAIL_PASSWORD 未配置")
        if not cls.SUPABASE_URL:
            errors.append("SUPABASE_URL 未配置")
        if not cls.SUPABASE_KEY:
            errors.append("SUPABASE_KEY 未配置")
        if errors:
            for e in errors:
                print(f"❌ {e}")
            return False
        print("✅ 配置验证通过")
        return True
    
    @classmethod
    def validate_supabase(cls) -> bool:
        return bool(cls.SUPABASE_URL and cls.SUPABASE_KEY)
    
    @classmethod
    def ensure_output_dir(cls):
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        return cls.OUTPUT_DIR


settings = Settings()