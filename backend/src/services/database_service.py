# -*- coding: utf-8 -*-
"""Supabase 数据库服务 + Storage 上传"""

from pathlib import Path
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from src.config.settings import settings


class DatabaseService:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            if not settings.validate_supabase():
                raise ValueError("Supabase 配置无效")
            self._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    # ---- 数据库 CRUD ----

    def insert(self, table: str, data: Dict) -> Optional[Dict]:
        try:
            resp = self._client.table(table).insert(data).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            print(f"❌ 插入失败 [{table}]: {e}")
            return None

    def select(self, table: str, filters: Dict = None, limit: int = None) -> List[Dict]:
        try:
            q = self._client.table(table).select("*")
            if filters:
                for k, v in filters.items():
                    q = q.eq(k, v)
            if limit:
                q = q.limit(limit)
            return q.execute().data or []
        except Exception as e:
            print(f"❌ 查询失败 [{table}]: {e}")
            return []

    def select_one(self, table: str, filters: Dict) -> Optional[Dict]:
        r = self.select(table, filters, limit=1)
        return r[0] if r else None

    def update(self, table: str, filters: Dict, data: Dict) -> Optional[Dict]:
        """Update rows matching filters with data, return first updated row."""
        try:
            q = self._client.table(table).update(data)
            for k, v in filters.items():
                q = q.eq(k, v)
            resp = q.execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            print(f"❌ 更新失败 [{table}]: {e}")
            return None

    def get_order_by_etsy_id(self, etsy_order_id: str) -> Optional[Dict]:
        return self.select_one("orders", {"etsy_order_id": etsy_order_id})

    def get_pending_orders(self) -> List[Dict]:
        return self.select("orders", {"status": "pending"})

    def create_order(self, data: Dict) -> Optional[Dict]:
        return self.insert("orders", data)

    def get_all_sku_mappings(self) -> List[Dict]:
        return self.select("sku_mapping")

    def get_all_fonts(self) -> List[Dict]:
        return self.select("fonts")

    # ---- Supabase Storage 上传 ----

    def upload_file(self, bucket: str, file_path: Path, dest_name: str = None) -> Optional[str]:
        """
        上传文件到 Supabase Storage bucket。
        返回公开可访问 URL，失败返回 None。
        """
        try:
            dest = dest_name or file_path.name
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            suffix = file_path.suffix.lower()
            mime_map = {
                ".svg": "image/svg+xml",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".pdf": "application/pdf",
            }
            mime = mime_map.get(suffix, "application/octet-stream")
            self._client.storage.from_(bucket).upload(
                dest, file_bytes,
                file_options={"content-type": mime, "upsert": "true"}
            )
            url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket}/{dest}"
            print(f"✅ 已上传到 Storage: {url}")
            return url
        except Exception as e:
            print(f"❌ 上传失败 [{bucket}/{dest_name}]: {e}")
            return None


db = DatabaseService()
