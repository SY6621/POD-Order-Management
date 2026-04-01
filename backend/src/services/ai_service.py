# -*- coding: utf-8 -*-
"""
AI服务模块 - 管理系统通用AI接口
当前功能: 邮件内容生成
后续扩展: 订单分析、智能推荐等

AI API 配置说明：
在 .env 文件中配置以下环境变量以启用AI生成功能：
- ZHIPU_API_KEY: 智谱AI API密钥（推荐，已在配置中）
- ZHIPU_MODEL: 智谱AI模型名称（默认 glm-4-flash）

如果未配置API密钥，将自动降级使用内置高质量模板。

支持的AI服务商（按优先级）：
1. 智谱AI (ZHIPU_API_KEY) - 已配置
2. OpenAI (OPENAI_API_KEY) - 可选配置
3. DeepSeek (DEEPSEEK_API_KEY) - 可选配置
"""

import requests
import json
from typing import Optional, Dict, Any, List
from src.config.settings import settings


class AIService:
    """AI服务 - 统一AI能力调用接口"""
    
    # 邮件场景定义
    SCENES = {
        "first_confirm": "首封确认邮件 - 效果图制作完成，请客户确认设计",
        "modify_confirm": "修改确认邮件 - 按客户要求修改后，请再次确认",
        "review_request": "追评邮件 - 订单完成后邀请客户留下好评"
    }
    
    # 语气风格定义
    TONES = {
        "friendly": "友好亲切",
        "professional": "专业正式",
        "warm": "温暖关怀"
    }
    
    def __init__(self):
        """初始化AI服务"""
        self.api_key = settings.ZHIPU_API_KEY
        self.model = settings.ZHIPU_MODEL
        self.api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        
        # 检测可用的AI服务
        self.available_provider = self._detect_provider()
        
    def _detect_provider(self) -> Optional[str]:
        """
        检测可用的AI服务商
        
        Returns:
            服务商名称: 'zhipu', 'openai', 'deepseek' 或 None
        """
        # 优先使用智谱AI（已在项目中配置）
        if self.api_key:
            print(f"✅ AI服务: 使用智谱AI ({self.model})")
            return "zhipu"
        
        # 可扩展其他服务商
        # TODO: 添加 OpenAI、DeepSeek 等支持
        
        print("ℹ️ AI服务: 未检测到API配置，将使用内置模板")
        return None
    
    def generate_email(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成邮件内容
        
        Args:
            params: 邮件参数字典
                - scene: 场景类型 (first_confirm/modify_confirm/review_request)
                - customer_name: 客户名称
                - product_name: 产品名称
                - front_text: 正面文字
                - back_text: 背面文字
                - shape: 形状
                - color: 颜色
                - size: 尺寸
                - tone: 语气风格 (friendly/professional/warm)
                - sender_name: 落款名称
                - modify_reason: 修改原因（仅modify_confirm场景）
                - effect_image_url: 效果图URL（可选）
        
        Returns:
            {
                "subject": "邮件主题",
                "body": "邮件正文",
                "scene": "场景类型",
                "generated_by": "ai/template"
            }
        """
        scene = params.get("scene", "first_confirm")
        
        # 参数校验
        if scene not in self.SCENES:
            scene = "first_confirm"
        
        # 优先使用AI生成
        if self.available_provider:
            result = self._generate_by_ai(params)
            if result:
                result["generated_by"] = "ai"
                return result
            # AI生成失败，降级到模板
            print("⚠️ AI生成失败，降级使用内置模板")
        
        # 使用内置模板
        result = self._generate_by_template(params)
        result["generated_by"] = "template"
        return result
    
    def _generate_by_ai(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        使用AI生成邮件内容
        
        Args:
            params: 邮件参数
            
        Returns:
            生成结果或None
        """
        if not self.api_key:
            return None
        
        scene = params.get("scene", "first_confirm")
        tone = params.get("tone", "friendly")
        
        # 构建系统提示词
        system_prompt = self._build_system_prompt(scene, tone)
        
        # 构建用户输入
        user_content = self._build_user_input(params)
        
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
                        "content": user_content
                    }
                ],
                "temperature": 0.7,  # 适中的创造性
                "max_tokens": 1024
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                
                # 解析AI返回的内容（期望JSON格式或邮件格式）
                parsed = self._parse_ai_response(content, scene)
                if parsed:
                    print(f"✅ AI邮件生成成功: {scene}")
                    return parsed
                else:
                    print(f"⚠️ AI响应解析失败")
                    return None
            else:
                print(f"❌ AI API错误: {response.status_code} - {response.text[:200]}")
                return None
                
        except requests.Timeout:
            print("❌ AI API超时")
            return None
        except Exception as e:
            print(f"❌ AI服务异常: {e}")
            return None
    
    def _build_system_prompt(self, scene: str, tone: str) -> str:
        """构建系统提示词"""
        tone_desc = self.TONES.get(tone, "友好亲切")
        scene_desc = self.SCENES.get(scene, "首封确认邮件")
        
        return f"""You are a professional e-commerce customer service email writer.
Your task: Write a {tone_desc} email for the following scenario: {scene_desc}

REQUIREMENTS:
1. Write in English only
2. Tone: {tone_desc}
3. Be professional but warm and personal
4. Include specific product details provided
5. Add appropriate emojis (1-3 emojis max)
6. Keep it concise but complete

OUTPUT FORMAT (must follow exactly):
SUBJECT: [email subject line]

BODY:
[email body text]

Do not include any explanations or additional text."""
    
    def _build_user_input(self, params: Dict[str, Any]) -> str:
        """构建用户输入"""
        lines = [
            "Please generate an email with the following details:",
            "",
            f"Customer Name: {params.get('customer_name', 'Valued Customer')}",
            f"Product: {params.get('product_name', 'Custom Pet Tag')}",
            f"Shape: {params.get('shape', 'Heart')}",
            f"Color: {params.get('color', 'Gold')}",
            f"Size: {params.get('size', 'Small')}",
        ]
        
        front_text = params.get('front_text', '')
        back_text = params.get('back_text', '')
        if front_text:
            lines.append(f"Front Text: \"{front_text}\"")
        if back_text:
            lines.append(f"Back Text: \"{back_text}\"")
        
        sender = params.get('sender_name', 'Customer Support Team')
        lines.append(f"Sender Name: {sender}")
        
        # 场景特定参数
        scene = params.get('scene', 'first_confirm')
        if scene == "modify_confirm" and params.get('modify_reason'):
            lines.append(f"Modification Request: {params.get('modify_reason')}")
        
        if params.get('effect_image_url'):
            lines.append(f"Effect Image URL: {params.get('effect_image_url')}")
        
        return "\n".join(lines)
    
    def _parse_ai_response(self, content: str, scene: str) -> Optional[Dict[str, Any]]:
        """解析AI响应内容"""
        try:
            # 尝试解析 SUBJECT 和 BODY 格式
            subject = ""
            body = ""
            
            lines = content.split('\n')
            in_body = False
            body_lines = []
            
            for line in lines:
                line_stripped = line.strip()
                if line_stripped.upper().startswith("SUBJECT:"):
                    subject = line_stripped[8:].strip()
                elif line_stripped.upper().startswith("BODY:"):
                    in_body = True
                elif in_body:
                    body_lines.append(line)
            
            body = '\n'.join(body_lines).strip()
            
            if subject and body:
                return {
                    "subject": subject,
                    "body": body,
                    "scene": scene
                }
            
            # 如果格式不匹配，尝试直接使用内容
            if content and len(content) > 50:
                # 找第一行作为subject
                first_line_end = content.find('\n')
                if first_line_end > 0:
                    subject = content[:first_line_end].strip()
                    body = content[first_line_end:].strip()
                    return {
                        "subject": subject,
                        "body": body,
                        "scene": scene
                    }
            
            return None
            
        except Exception as e:
            print(f"解析AI响应失败: {e}")
            return None
    
    def _generate_by_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        使用内置模板生成邮件
        
        Args:
            params: 邮件参数
            
        Returns:
            生成的邮件内容
        """
        scene = params.get("scene", "first_confirm")
        
        # 根据场景选择模板
        if scene == "first_confirm":
            return self._template_first_confirm(params)
        elif scene == "modify_confirm":
            return self._template_modify_confirm(params)
        elif scene == "review_request":
            return self._template_review_request(params)
        else:
            return self._template_first_confirm(params)
    
    def _template_first_confirm(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """首封确认邮件模板"""
        customer_name = params.get('customer_name', 'Valued Customer')
        product_name = params.get('product_name', 'Custom Pet Tag')
        shape = params.get('shape', 'Heart')
        color = params.get('color', 'Gold')
        size = params.get('size', 'Small')
        front_text = params.get('front_text', '')
        back_text = params.get('back_text', '')
        sender_name = params.get('sender_name', 'Customer Support Team')
        effect_url = params.get('effect_image_url', '')
        
        # 构建设计描述
        design_desc = f"{color} {shape} tag ({size})"
        if front_text:
            design_desc += f' with front text "{front_text}"'
        if back_text:
            design_desc += f' and back text "{back_text}"'
        
        subject = f"Your {product_name} Design is Ready! 🐾"
        
        body = f"""Dear {customer_name.split()[0] if customer_name else 'Customer'},

Thank you for your order! We're excited to share your custom design with you. 🎉

Your personalized {design_desc} has been crafted with care, and we'd love for you to take a look before we proceed with production.

📎 Please review your design preview{' at: ' + effect_url if effect_url else ' attached to this email.'}

**Design Details:**
- Product: {product_name}
- Shape: {shape}
- Color: {color}
- Size: {size}
{f'- Front Text: "{front_text}"' if front_text else ''}
{f'- Back Text: "{back_text}"' if back_text else ''}

If everything looks perfect, simply reply with "Confirmed" and we'll start production right away! 

If you'd like any changes, just let us know the details and we'll revise the design for you.

Thank you for choosing us! 💖

Warm regards,
{sender_name}"""
        
        return {
            "subject": subject,
            "body": body,
            "scene": "first_confirm"
        }
    
    def _template_modify_confirm(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """修改确认邮件模板"""
        customer_name = params.get('customer_name', 'Valued Customer')
        product_name = params.get('product_name', 'Custom Pet Tag')
        shape = params.get('shape', 'Heart')
        color = params.get('color', 'Gold')
        size = params.get('size', 'Small')
        front_text = params.get('front_text', '')
        back_text = params.get('back_text', '')
        sender_name = params.get('sender_name', 'Customer Support Team')
        modify_reason = params.get('modify_reason', 'your requested changes')
        effect_url = params.get('effect_image_url', '')
        
        subject = f"Your Updated {product_name} Design is Ready! ✨"
        
        body = f"""Dear {customer_name.split()[0] if customer_name else 'Customer'},

Great news! We've updated your design based on {modify_reason}. 🔄

Your revised {color} {shape} tag ({size}) is now ready for your review.

📎 Please check the updated design{' at: ' + effect_url if effect_url else ' attached to this email.'}

**Updated Design Details:**
- Product: {product_name}
- Shape: {shape}
- Color: {color}
- Size: {size}
{f'- Front Text: "{front_text}"' if front_text else ''}
{f'- Back Text: "{back_text}"' if back_text else ''}

If the updated design meets your expectations, reply with "Confirmed" and we'll begin production immediately!

Need more adjustments? No problem at all – just let us know what you'd like changed. 😊

Thank you for your patience!

Warm regards,
{sender_name}"""
        
        return {
            "subject": subject,
            "body": body,
            "scene": "modify_confirm"
        }
    
    def _template_review_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """追评邀请邮件模板"""
        customer_name = params.get('customer_name', 'Valued Customer')
        product_name = params.get('product_name', 'Custom Pet Tag')
        shape = params.get('shape', 'Heart')
        sender_name = params.get('sender_name', 'Customer Support Team')
        
        subject = f"How is your {product_name}? We'd Love to Hear from You! ⭐"
        
        body = f"""Dear {customer_name.split()[0] if customer_name else 'Customer'},

We hope you and your furry friend are enjoying your new {product_name}! 🐕🐱

Your custom {shape} tag was made with love, and we'd be thrilled to know how it's working out for you.

**Would you take a moment to share your experience?**

Your review helps other pet parents find the perfect personalized tag, and it means the world to our small business! 💝

🔗 Leave a review on Etsy: Just visit your order history and click "Leave a Review"

As a thank you, we'd like to offer you **10% off your next order**! Use code: LOYAL10 at checkout.

Thank you for being part of our community! 🌟

Warm regards,
{sender_name}"""
        
        return {
            "subject": subject,
            "body": body,
            "scene": "review_request"
        }
    
    def get_supported_scenes(self) -> Dict[str, str]:
        """获取支持的场景列表"""
        return self.SCENES.copy()
    
    def get_supported_tones(self) -> Dict[str, str]:
        """获取支持的语气风格列表"""
        return self.TONES.copy()
    
    def is_ai_available(self) -> bool:
        """检查AI服务是否可用"""
        return self.available_provider is not None


# 全局AI服务实例
ai_service = AIService()
