# -*- coding: utf-8 -*-
"""
订单数据模型
功能：定义订单相关的数据库表结构
更新日期：2026-02-04
说明：与 Supabase 数据库结构保持一致，支持前端 UI 字段
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from src.config.settings import settings


# 创建基类
Base = declarative_base()


class Order(Base):
    """
    订单主表 - 存储Etsy订单主信息
    
    状态值 (status):
        - new: 新订单
        - pending: 待确认
        - confirmed: 已确认
        - producing: 生产中
        - completed: 已完成
        - shipped: 已发货
        - delivered: 已送达
        - cancelled: 已取消
    
    优先级 (priority):
        - normal: 普通
        - high: 高优先级
        - urgent: 紧急
    """
    
    __tablename__ = "orders"
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Etsy订单号（唯一）
    etsy_order_id = Column(String(50), unique=True, nullable=False, index=True)
    
    # 关联 SKU
    sku_id = Column(Integer, ForeignKey("sku_mapping.id"), nullable=True)
    
    # 客户信息
    customer_name = Column(String(100))
    customer_email = Column(String(100))
    
    # 收件人地址信息（从邮件解析，用于物流下单）
    shipping_name = Column(String(100))
    shipping_address_line1 = Column(Text)
    shipping_address_line2 = Column(Text)
    shipping_city = Column(String(50))
    shipping_state = Column(String(50))
    shipping_zip = Column(String(20))
    shipping_country = Column(String(50))
    
    # 定制内容（刻字）
    front_text = Column(Text)  # 正面刻字
    back_text = Column(Text)   # 背面刻字
    
    # 订单数量与金额
    quantity = Column(Integer, default=1)
    total_amount = Column(Numeric(10, 2), default=0)
    weight_g = Column(Integer, default=30)  # 重量（克），用于物流下单
    
    # 订单状态
    status = Column(String(20), default="new")
    
    # 生产进度 (0-100)
    progress = Column(Integer, default=0)
    
    # 优先级
    priority = Column(String(10), default="normal")
    
    # 时间字段
    estimated_delivery = Column(DateTime, nullable=True)      # 预计交付日期
    production_started_at = Column(DateTime, nullable=True)   # 生产开始时间
    completed_at = Column(DateTime, nullable=True)            # 完成时间
    created_at = Column(DateTime, default=datetime.now)       # 创建时间
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间
    
    # 约束
    __table_args__ = (
        CheckConstraint('progress >= 0 AND progress <= 100', name='check_progress_range'),
        CheckConstraint("priority IN ('normal', 'high', 'urgent')", name='check_priority_value'),
    )
    
    # 关联关系
    sku = relationship("SkuMapping", back_populates="orders")
    logistics = relationship("Logistics", back_populates="order", uselist=False)
    production_document = relationship("ProductionDocument", back_populates="order", uselist=False)
    email_logs = relationship("EmailLog", back_populates="order")
    
    def __repr__(self):
        return f"<Order(etsy_order_id='{self.etsy_order_id}', status='{self.status}')"


class Logistics(Base):
    """
    物流信息表 - 存储收货地址和物流跟踪信息
    
    物流状态 (delivery_status):
        - pending: 待发货
        - shipped: 已发货
        - in_transit: 运输中
        - delivered: 已送达
        - failed: 配送失败
    """
    
    __tablename__ = "logistics"
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 外键关联订单
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # 收件人信息
    recipient_name = Column(String(100))
    country = Column(String(50))
    city = Column(String(50))
    street_address = Column(Text)
    postal_code = Column(String(20))
    
    # 物流信息
    tracking_number = Column(String(100))
    label_url = Column(String(500))
    delivery_status = Column(String(20), default="pending")
    
    # 时间字段
    shipped_at = Column(DateTime, nullable=True)     # 发货日期
    delivered_at = Column(DateTime, nullable=True)   # 收货日期
    pickup_date = Column(DateTime, nullable=True)    # 取货日期
    
    # 约束
    __table_args__ = (
        CheckConstraint("delivery_status IN ('pending', 'shipped', 'in_transit', 'delivered', 'failed')", name='check_delivery_status'),
    )
    
    # 关联关系
    order = relationship("Order", back_populates="logistics")
    
    def __repr__(self):
        return f"<Logistics(order_id={self.order_id}, status='{self.delivery_status}')"


class ProductionDocument(Base):
    """生产文档表 - 存储效果图和生产PDF"""
    
    __tablename__ = "production_documents"
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 外键关联订单
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # 文档链接
    effect_jpg_url = Column(String(500))      # 效果图 JPG
    effect_svg_url = Column(String(500))      # 效果图 SVG
    production_pdf_url = Column(String(500))  # 生产 PDF
    real_photo_urls = Column(Text)            # 实拍图（JSON数组）
    
    # 时间字段
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联关系
    order = relationship("Order", back_populates="production_document")
    
    def __repr__(self):
        return f"<ProductionDocument(order_id={self.order_id})>"


class EmailLog(Base):
    """
    邮件发送记录表 - 跟踪邮件发送状态
    
    邮件类型 (email_type):
        - confirmation: 确认邮件
        - shipping: 发货通知
        - logistics_delay: 物流延迟
        - review_request: 追评请求
    """
    
    __tablename__ = "email_logs"
    
    # 主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 外键关联订单
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    
    # 邮件信息
    email_type = Column(String(30))          # 邮件类型
    recipient_email = Column(String(100))    # 收件人邮箱
    subject = Column(String(200))            # 邮件主题
    status = Column(String(20), default="pending")  # 发送状态
    
    # 时间字段
    sent_at = Column(DateTime, nullable=True)  # 发送时间
    
    # 关联关系
    order = relationship("Order", back_populates="email_logs")
    
    def __repr__(self):
        return f"<EmailLog(order_id={self.order_id}, type='{self.email_type}')"


class SkuMapping(Base):
    """
    SKU对照表 - 订单信息反推产品编号
    
    用于根据订单中的产品信息匹配到具体的工厂生产编码
    """
    
    __tablename__ = "sku_mapping"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # SKU编码
    sku_code = Column(String(50), unique=True, nullable=False, index=True)
    
    # 产品属性
    material = Column(String(50))   # 材质
    shape = Column(String(50))      # 形状
    color = Column(String(50))      # 颜色
    size = Column(String(50))       # 尺寸
    craft = Column(String(50))      # 工艺
    
    # 关联关系
    orders = relationship("Order", back_populates="sku")
    
    def __repr__(self):
        return f"<SkuMapping(sku_code='{self.sku_code}')>"


# ===== 数据库操作类 =====
class Database:
    """数据库操作类"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.engine = create_engine(settings.DATABASE_URL, echo=False)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """创建所有数据表"""
        Base.metadata.create_all(self.engine)
        print("✅ 数据库表创建成功")
    
    def get_session(self):
        """获取数据库会话"""
        return self.Session()
    
    def add_order(self, order_data: dict) -> Optional[Order]:
        """
        添加新订单
        
        Args:
            order_data: 订单数据字典
            
        Returns:
            Order: 创建的订单对象
        """
        session = self.get_session()
        try:
            order = Order(**order_data)
            session.add(order)
            session.commit()
            session.refresh(order)
            return order
        except Exception as e:
            session.rollback()
            print(f"❌ 添加订单失败: {e}")
            return None
        finally:
            session.close()
    
    def get_order_by_etsy_id(self, etsy_order_id: str) -> Optional[Order]:
        """根据Etsy订单号查询订单"""
        session = self.get_session()
        try:
            return session.query(Order).filter(
                Order.etsy_order_id == etsy_order_id
            ).first()
        finally:
            session.close()
    
    def get_pending_orders(self) -> List[Order]:
        """获取所有待处理订单"""
        session = self.get_session()
        try:
            return session.query(Order).filter(
                Order.status == "pending"
            ).all()
        finally:
            session.close()
    
    def update_order_status(self, etsy_order_id: str, status: str) -> bool:
        """更新订单状态"""
        session = self.get_session()
        try:
            order = session.query(Order).filter(
                Order.etsy_order_id == etsy_order_id
            ).first()
            
            if order:
                order.status = status
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            print(f"❌ 更新订单状态失败: {e}")
            return False
        finally:
            session.close()


# 创建全局数据库实例
db = Database()


# ===== 使用示例 =====
if __name__ == "__main__":
    # 创建数据库表
    db.create_tables()
    
    # 测试添加订单
    test_order = {
        "etsy_order_id": "TEST-001",
        "customer_name": "测试客户",
        "customer_email": "test@example.com",
        "front_text": "Hello",
        "back_text": "World",
        "quantity": 1,
        "total_amount": 99.99,
        "status": "new",
        "priority": "normal",
        "progress": 0
    }
    
    order = db.add_order(test_order)
    if order:
        print(f"✅ 测试订单创建成功: {order}")
