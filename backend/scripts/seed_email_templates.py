# -*- coding: utf-8 -*-
"""
邮件模板数据补充脚本
插入缺失的2条模板数据：
- redo_confirm: 重做确认回复（modification类型）
- thanks_review: 感谢追评（follow_up类型）

运行方式:
    cd d:\ETSY_Order_Automation\backend
    poetry run python scripts/seed_email_templates.py
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from supabase import create_client, Client
from src.config.settings import settings


def get_supabase_client() -> Client:
    """获取Supabase客户端"""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def get_missing_templates():
    """获取需要补充的模板数据"""
    
    # 模板1: 重做确认回复 (modification类型)
    redo_confirm_template = {
        "type": "modification",
        "template_key": "redo_confirm",
        "name": "重做确认回复",
        "icon": "🔄",
        "description": "需要重新制作的订单，诚恳回复客户",
        "subject_zh": "您的订单已重新制作完成，请查看新效果图",
        "subject_en": "Your Order Has Been Remade - Please Review the New Design",
        "content": {
            "formal": {
                "short": {
                    "en": "Dear {firstName}, your order #{orderId} has been remade. View: {effectImageUrl}",
                    "zh": "亲爱的{firstName}，订单#{orderId}已重新制作。查看：{effectImageUrl}"
                },
                "standard": {
                    "en": "Dear {firstName}, regarding your order #{orderId}, we have completely remade your design based on your feedback. Please review the new preview: {effectImageUrl}. Reply 'Confirmed' to proceed.",
                    "zh": "亲爱的{firstName}，关于您的订单#{orderId}，我们已经按照您的要求重新制作了设计。请查看新的效果图：{effectImageUrl}。回复'确认'即可安排生产。"
                },
                "detailed": {
                    "en": "Dear {firstName},\n\nRegarding your order #{orderId}, we sincerely apologize for the inconvenience caused. We have completely remade your design based on your detailed feedback.\n\nPlease review the updated design preview here: {effectImageUrl}\n\nWe have carefully checked every detail to ensure it meets your requirements this time. If everything looks perfect, simply reply with 'Confirmed' and we'll start production immediately.\n\nIf you need any further adjustments, please let us know before {confirmationDeadline}.\n\nThank you for your patience and understanding.\n\nBest regards,\n{senderName}",
                    "zh": "亲爱的{firstName}，\n\n关于您的订单#{orderId}，对于之前给您带来的不便，我们深表歉意。我们已经根据您的详细反馈完全重新制作了设计。\n\n请在此查看更新的设计预览：{effectImageUrl}\n\n我们仔细检查了每个细节，确保这次完全符合您的要求。如果一切看起来都完美，只需回复'确认'，我们将立即开始生产。\n\n如果您需要任何进一步调整，请在{confirmationDeadline}前告知我们。\n\n感谢您的耐心与理解。\n\n此致敬礼，\n{senderName}"
                }
            },
            "casual": {
                "short": {
                    "en": "Hi {firstName}! Your order #{orderId} is remade ✨ Check it out: {effectImageUrl}",
                    "zh": "嗨{firstName}！订单#{orderId}已重做完成✨ 快来看：{effectImageUrl}"
                },
                "standard": {
                    "en": "Hi {firstName}! Great news! We've remade your order #{orderId} based on your feedback. Here's the new design: {effectImageUrl}. Let us know what you think!",
                    "zh": "嗨{firstName}！好消息！我们根据您的反馈重新制作了订单#{orderId}。这是新设计：{effectImageUrl}。告诉我们您的想法！"
                },
                "detailed": {
                    "en": "Hi {firstName}!\n\nWe've completely remade your order #{orderId} based on your feedback! 🎉\n\nHere's your fresh design: {effectImageUrl}\n\nWe really want to get this perfect for you, so please take a look and let us know if it's exactly what you envisioned. We've paid special attention to the details you mentioned.\n\nIf it looks good, just say 'Confirmed' and we'll get it into production right away! Need changes? No worries, just tell us before {confirmationDeadline}.\n\nThanks for working with us on this! 😊\n\nCheers,\n{senderName}",
                    "zh": "嗨{firstName}！\n\n我们根据您的反馈完全重新制作了订单#{orderId}！🎉\n\n这是您的新设计：{effectImageUrl}\n\n我们真的希望为您做到完美，所以请查看一下，告诉我们这是否正是您想要的。我们特别注意了您提到的细节。\n\n如果看起来不错，只需说'确认'，我们就会立即安排生产！需要修改？没问题，请在{confirmationDeadline}前告诉我们。\n\n感谢您与我们的配合！😊\n\n祝好，\n{senderName}"
                }
            },
            "lively": {
                "short": {
                    "en": "🎉 {firstName}, your order #{orderId} got a makeover! Check: {effectImageUrl}",
                    "zh": "🎉 {firstName}，订单#{orderId}焕然一新！查看：{effectImageUrl}"
                },
                "standard": {
                    "en": "🌟 Hey {firstName}! Your order #{orderId} has been completely remade with love! Take a peek: {effectImageUrl} We're so excited for you to see it! 💖",
                    "zh": "🌟 嘿{firstName}！您的订单#{orderId}已用心完全重做！来看看：{effectImageUrl} 我们好期待您看到它！💖"
                },
                "detailed": {
                    "en": "🎨✨ Hey there {firstName}!\n\nAmazing news! Your order #{orderId} just got a complete makeover! 🌈\n\nFeast your eyes on this: {effectImageUrl}\n\nWe started fresh and created something special just for you! Every detail has been crafted with extra care and attention. This version captures exactly what you were looking for!\n\nLove it? Just shout 'Confirmed' and we'll rush it to production! 🚀 Want tweaks? We're on it - just holler before {confirmationDeadline}!\n\nCan't wait to hear what you think! 🥰\n\nHugs,\n{senderName}",
                    "zh": "🎨✨ 嘿{firstName}！\n\n太棒的消息！您的订单#{orderId}刚刚完成全面改造！🌈\n\n尽情欣赏：{effectImageUrl}\n\n我们重新开始，专门为您打造了特别的作品！每一个细节都经过格外精心的处理。这个版本完全符合您的期望！\n\n喜欢吗？只需大喊'确认'，我们就会立即投入生产！🚀 想要调整？我们在——请在{confirmationDeadline}前喊我们！\n\n迫不及待想听听您的想法！🥰\n\n抱抱，\n{senderName}"
                }
            }
        },
        "ai_prompt": "Write a sincere apology and remake confirmation email. Acknowledge the inconvenience caused and emphasize that the design has been completely remade based on customer's specific feedback.",
        "sender_name": "Customer Support Team",
        "sort_order": 20
    }
    
    # 模板2: 感谢追评 (follow_up类型)
    thanks_review_template = {
        "type": "follow_up",
        "template_key": "thanks_review",
        "name": "感谢追评",
        "icon": "🙏",
        "description": "强调感谢的追评邮件",
        "subject_zh": "衷心感谢您的选择，期待您的宝贵评价",
        "subject_en": "Thank You for Choosing Us - We'd Love Your Review!",
        "content": {
            "formal": {
                "short": {
                    "en": "Dear {firstName}, thank you for choosing our custom pet tags. We'd appreciate your review!",
                    "zh": "亲爱的{firstName}，感谢您选择我们的定制宠物牌。期待您的评价！"
                },
                "standard": {
                    "en": "Dear {firstName}, we truly appreciate you choosing our custom pet tags for order #{orderId}. Your satisfaction means everything to us. If you have a moment, we'd be grateful for your review.",
                    "zh": "亲爱的{firstName}，非常感谢您选择我们的定制宠物牌，订单号#{orderId}。您的满意对我们意义重大。如果您有时间，我们将非常感激您的评价。"
                },
                "detailed": {
                    "en": "Dear {firstName},\n\nWe truly appreciate you choosing our custom pet tags for your order #{orderId}. It has been our pleasure to create something special for your beloved pet.\n\nYour satisfaction means everything to us, and we hope the tag has exceeded your expectations. We put our heart into every piece we create, knowing how much your furry friend means to you.\n\nIf you have been happy with our product and service, would you consider leaving us a review? Your feedback helps other pet parents discover our handcrafted tags and supports our small business more than you know.\n\nYou can leave a review by visiting your order history on Etsy and clicking 'Leave a Review'.\n\nThank you again for trusting us with something so personal. We wish you and {firstName}'s pet many happy adventures together!\n\nWith gratitude,\n{senderName}",
                    "zh": "亲爱的{firstName}，\n\n非常感谢您为订单#{orderId}选择我们的定制宠物牌。能为您的爱宠创造特别的物品是我们的荣幸。\n\n您的满意对我们意义重大，我们希望这个宠物牌超出了您的期望。我们用心制作每一件作品，深知您的毛孩子对您的意义。\n\n如果您对我们的产品和服务感到满意，您愿意给我们留个评价吗？您的反馈能帮助其他宠物主人发现我们的手工宠物牌，对我们小企业的支持超乎您的想象。\n\n您可以通过访问Etsy上的订单历史并点击'留下评价'来评价。\n\n再次感谢您信任我们处理如此私人的物品。祝您和{firstName}的宠物一起度过许多快乐的冒险时光！\n\n满怀感激，\n{senderName}"
                }
            },
            "casual": {
                "short": {
                    "en": "Hi {firstName}! Thanks so much for choosing us! A quick review would mean the world 🌟",
                    "zh": "嗨{firstName}！非常感谢选择我们！一个简短评价对我们意义重大🌟"
                },
                "standard": {
                    "en": "Hi {firstName}! We really appreciate you choosing our custom pet tags for order #{orderId}. If you're happy with everything, would you mind leaving us a review? It helps us so much!",
                    "zh": "嗨{firstName}！非常感谢您为订单#{orderId}选择我们的定制宠物牌。如果您对一切满意，您介意给我们留个评价吗？这对我们帮助很大！"
                },
                "detailed": {
                    "en": "Hi {firstName}!\n\nWe just wanted to say a huge THANK YOU for choosing our custom pet tags for order #{orderId}! 🐾\n\nWe really hope you and your furry friend are loving the tag we created. We had so much fun personalizing it just for you!\n\nIf everything arrived great and you're happy with your purchase, we'd absolutely love it if you could take a moment to leave us a review. Your words help other pet parents find us, and honestly, they make our whole day!\n\nLeaving a review is super easy - just head to your Etsy order history and click 'Leave a Review'.\n\nThanks again for supporting our small business. It really means the world to us! 🌍💕\n\nWarmly,\n{senderName}",
                    "zh": "嗨{firstName}！\n\n我们只想对您为订单#{orderId}选择我们的定制宠物牌表示大大的感谢！🐾\n\n我们真的希望您和您的毛孩子都喜欢我们制作的宠物牌。我们非常享受为您个性化定制的过程！\n\n如果一切到货完好，您对购买感到满意，如果您能花点时间给我们留个评价，我们会非常感激。您的话语能帮助其他宠物主人找到我们，说实话，它们能让我们开心一整天！\n\n留评价非常简单——只需前往您的Etsy订单历史，点击'留下评价'。\n\n再次感谢您支持我们的小企业。这对我们意义重大！🌍💕\n\n热情问候，\n{senderName}"
                }
            },
            "lively": {
                "short": {
                    "en": "🌟 {firstName}, you're amazing! Thanks for choosing us! Quick favor - a review? 🙏",
                    "zh": "🌟 {firstName}，您太棒了！感谢选择我们！帮个小忙——留个评价？🙏"
                },
                "standard": {
                    "en": "🎉 Hey {firstName}! We can't thank you enough for choosing our custom pet tags for order #{orderId}! You rock! 🌟 If you loved your tag, would you pretty please leave us a review? It would make our day!",
                    "zh": "🎉 嘿{firstName}！我们对您为订单#{orderId}选择我们的定制宠物牌感激不尽！您太棒了！🌟 如果您喜欢您的宠物牌，您愿意给我们留个评价吗？这会让我们开心一整天！"
                },
                "detailed": {
                    "en": "🌈✨ Hey {firstName}!\n\nOMG, we just have to say THANK YOU THANK YOU THANK YOU for choosing our custom pet tags for order #{orderId}! 🎉🐾\n\nWe are literally doing happy dances over here thinking about your adorable pet wearing our tag! We put so much love into every piece, and it makes our hearts burst knowing it's found a good home with you. 💖\n\nSoooo... if you're absolutely loving your tag (and we really hope you are!), would you do us the biggest favor ever and leave us a review? Your kind words are like sunshine to our small business - they help other pet parents find us and keep us motivated to create more beautiful tags!\n\nJust pop over to your Etsy order history and hit 'Leave a Review' - it's super quick and easy!\n\nThank you from the bottom of our hearts for supporting our dream! You're the best! 🌟\n\nBig hugs and puppy kisses,\n{senderName}",
                    "zh": "🌈✨ 嘿{firstName}！\n\n天哪，我们必须说感谢您感谢您感谢您为订单#{orderId}选择我们的定制宠物牌！🎉🐾\n\n想到您可爱的宠物戴着我们的宠物牌，我们在这里 literally 跳起了欢快的舞蹈！我们在每件作品中都倾注了很多爱，知道它找到了您这个好归宿，我们的心都要融化了。💖\n\n所以所以所以... 如果您绝对喜欢您的宠物牌（我们真的希望您喜欢！），您愿意帮我们这个最大的忙，给我们留个评价吗？您善意的言语就像阳光照耀着我们的小企业——它们帮助其他宠物主人找到我们，激励我们创作更多美丽的宠物牌！\n\n只需前往您的Etsy订单历史，点击'留下评价'——超级快速简单！\n\n从心底感谢您支持我们的梦想！您是最棒的！🌟\n\n大大的拥抱和 puppy 亲吻，\n{senderName}"
                }
            }
        },
        "ai_prompt": "Write a warm and grateful review request email. Express sincere appreciation for the customer's choice and gently encourage them to leave a review to help other pet parents.",
        "sender_name": "Customer Support Team",
        "sort_order": 30
    }
    
    return [redo_confirm_template, thanks_review_template]


def insert_templates():
    """插入缺失的模板数据"""
    print("=" * 60)
    print("邮件模板数据补充脚本")
    print("=" * 60)
    
    try:
        # 获取Supabase客户端
        supabase = get_supabase_client()
        print("✅ 已连接到Supabase")
        
        # 获取缺失的模板
        templates = get_missing_templates()
        print(f"\n准备插入 {len(templates)} 条模板数据:\n")
        
        inserted_count = 0
        skipped_count = 0
        
        for template in templates:
            template_key = template["template_key"]
            template_type = template["type"]
            name = template["name"]
            
            # 检查是否已存在（按type和template_key组合检查）
            existing = supabase.table("email_templates") \
                .select("id") \
                .eq("type", template_type) \
                .eq("template_key", template_key) \
                .execute()
            
            if existing.data and len(existing.data) > 0:
                print(f"  ⏭️  {name} ({template_type}/{template_key}) - 已存在，跳过")
                skipped_count += 1
                continue
            
            # 插入新模板
            result = supabase.table("email_templates").insert(template).execute()
            
            if result.data:
                print(f"  ✅ {name} ({template_type}/{template_key}) - 插入成功")
                inserted_count += 1
            else:
                print(f"  ❌ {name} ({template_type}/{template_key}) - 插入失败")
        
        print("\n" + "=" * 60)
        print(f"执行结果: 成功插入 {inserted_count} 条，跳过 {skipped_count} 条")
        print("=" * 60)
        
        # 显示当前所有模板
        print("\n当前email_templates表中的所有模板:")
        all_templates = supabase.table("email_templates") \
            .select("type, template_key, name") \
            .order("type") \
            .execute()
        
        if all_templates.data:
            current_type = None
            for t in all_templates.data:
                if t["type"] != current_type:
                    current_type = t["type"]
                    print(f"\n  【{current_type}类型】")
                print(f"    - {t['name']} ({t['template_key']})")
        
        print("\n✅ 脚本执行完成!")
        return True
        
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = insert_templates()
    sys.exit(0 if success else 1)
