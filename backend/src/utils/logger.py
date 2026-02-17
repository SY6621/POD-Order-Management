# -*- coding: utf-8 -*-
"""
日志工具模块
功能：统一的日志记录，支持控制台和文件输出
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

from src.config.settings import settings


def setup_logger(name: str = "etsy_automation") -> logging.Logger:
    """
    配置并返回日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # ===== 控制台处理器 =====
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # ===== 文件处理器 =====
    try:
        log_file = Path(settings.LOG_FILE)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_file, 
            mode="a", 
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"无法创建日志文件: {e}")
    
    return logger


# 创建全局日志实例
logger = setup_logger()


# ===== 便捷日志函数 =====
def log_info(message: str):
    """记录INFO级别日志"""
    logger.info(message)


def log_error(message: str):
    """记录ERROR级别日志"""
    logger.error(message)


def log_warning(message: str):
    """记录WARNING级别日志"""
    logger.warning(message)


def log_debug(message: str):
    """记录DEBUG级别日志"""
    logger.debug(message)


# ===== 使用示例 =====
if __name__ == "__main__":
    log_info("系统启动")
    log_debug("调试信息")
    log_warning("警告信息")
    log_error("错误信息")
    print("✅ 日志模块测试完成")
