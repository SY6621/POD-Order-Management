# -*- coding: utf-8 -*-
"""Supabase 数据库服务"""

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


db = DatabaseService()