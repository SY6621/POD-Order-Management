"""Services module"""

# Lazy imports to avoid circular dependencies
def get_db():
    from src.services.database_service import db
    return db

def get_email_service():
    from src.services.email_service import EmailService
    return EmailService

def get_email_parser():
    from src.services.email_parser import email_parser
    return email_parser

def get_order_service():
    from src.services.order_service import order_service
    return order_service

def get_template_service():
    from src.services.template_service import template_service
    return template_service

def get_effect_image_service():
    from src.services.effect_image_service import effect_image_service
    return effect_image_service

def get_pdf_service():
    from src.services.pdf_service import pdf_service
    return pdf_service

def get_shipping_service():
    from src.services.shipping_service import shipping_service
    return shipping_service

def get_svg_pdf_service():
    from src.services.svg_pdf_service import svg_pdf_service
    return svg_pdf_service