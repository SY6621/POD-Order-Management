# -*- coding: utf-8 -*-
"""
翻译服务模块
使用智谱AI (GLM-4) 进行中英文翻译
"""

import requests
import json
from typing import Optional
from src.config.settings import settings


class TranslationService:
    """翻译服务"""
    
    def __init__(self):
        self.api_key = settings.ZHIPU_API_KEY
        self.model = settings.ZHIPU_MODEL
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    def translate(self, text: str, source_lang: str = "zh", target_lang: str = "en") -> Optional[str]:
        """
        翻译文本
        
        Args:
            text: 要翻译的文本
            source_lang: 源语言 (zh/en)
            target_lang: 目标语言 (zh/en)
        
        Returns:
            翻译后的文本，失败返回 None
        """
        if not self.api_key:
            print("❌ 智谱AI API Key 未配置")
            return None
        
        # 构建提示词
        if source_lang == "zh" and target_lang == "en":
            system_prompt = "You are a professional translator. Translate the following Chinese text to natural, fluent English. Maintain the tone and style of the original text. Only return the translated text without any explanations."
        elif source_lang == "en" and target_lang == "zh":
            system_prompt = "You are a professional translator. Translate the following English text to natural, fluent Chinese. Maintain the tone and style of the original text. Only return the translated text without any explanations."
        else:
            system_prompt = "You are a professional translator. Translate the text accurately while maintaining the original tone and style. Only return the translated text without any explanations."
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                "temperature": 0.3,  # 低温度，更稳定
                "max_tokens": 2048
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result["choices"][0]["message"]["content"].strip()
                print(f"✅ 翻译成功: {len(text)} 字符 -> {len(translated_text)} 字符")
                return translated_text
            else:
                print(f"❌ 翻译API错误: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 翻译服务异常: {e}")
            return None
    
    def translate_email(self, chinese_content: str) -> Optional[str]:
        """
        专门用于翻译邮件内容（中文 -> 英文）
        
        Args:
            chinese_content: 中文邮件内容
        
        Returns:
            英文邮件内容
        """
        system_prompt = """You are a professional email translator specializing in e-commerce customer service.
Translate the following Chinese email to English with these requirements:
1. Maintain a polite, professional tone suitable for customer service
2. Keep email formatting (greetings, signatures, line breaks)
3. Use natural English expressions common in e-commerce
4. Preserve emojis and special characters
5. Only return the translated email content without explanations

Translation style guidelines:
- "亲爱的" -> "Dear" or "Hi" depending on context
- "祝好" -> "Kind regards" or "Best regards"
- "客服团队" -> "Customer Support Team" or similar
- Keep order numbers, product names, and URLs unchanged"""
        
        if not self.api_key:
            print("❌ 智谱AI API Key 未配置")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": chinese_content
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 2048
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result["choices"][0]["message"]["content"].strip()
                print(f"✅ 邮件翻译成功")
                return translated_text
            else:
                print(f"❌ 翻译API错误: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 翻译服务异常: {e}")
            return None


# 全局翻译服务实例
translation_service = TranslationService()
