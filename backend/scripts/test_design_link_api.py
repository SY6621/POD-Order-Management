# -*- coding: utf-8 -*-
"""
测试设计链接 API
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_get_design_token():
    """测试获取设计链接信息"""
    print('=== 测试1: 获取设计链接信息 ===')
    # 使用 us 店铺的 UUID
    resp = requests.get(f'{BASE_URL}/service-link/design-link/shops/0c85cdfb-d75f-4516-9a28-da81c1d1e2b1/token')
    print(f'Status: {resp.status_code}')
    if resp.status_code == 200:
        print(f'Response: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}')
    else:
        print(f'Error: {resp.text}')
    print()
    return resp.status_code == 200

def test_generate_design_token():
    """测试生成设计链接Token"""
    print('=== 测试2: 生成设计链接Token ===')
    # 使用 eu 店铺的 UUID（当前没有设计链接）
    resp = requests.post(
        f'{BASE_URL}/service-link/design-link/generate-token',
        json={'shop_id': '7e43fb37-cc32-42c4-9eea-07233cbb7d5e', 'enabled': True}
    )
    print(f'Status: {resp.status_code}')
    if resp.status_code == 200:
        data = resp.json()
        print(f'Response: {json.dumps(data, indent=2, ensure_ascii=False)}')
        return data.get('design_token'), data.get('design_link_url')
    else:
        print(f'Error: {resp.text}')
        return None, None
    print()

def test_validate_design_token(shop_code, token):
    """测试验证设计链接Token"""
    print('=== 测试3: 验证设计链接Token ===')
    resp = requests.post(
        f'{BASE_URL}/service-link/design-link/validate',
        json={'shop_code': shop_code, 'token': token}
    )
    print(f'Status: {resp.status_code}')
    if resp.status_code == 200:
        print(f'Response: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}')
    else:
        print(f'Error: {resp.text}')
    print()
    return resp.status_code == 200

def test_toggle_design_link(shop_id, enabled):
    """测试启用/禁用设计链接"""
    print(f'=== 测试4: {"禁用" if enabled else "启用"}设计链接 ===')
    resp = requests.post(
        f'{BASE_URL}/service-link/design-link/shops/{shop_id}/toggle?enabled={not enabled}'
    )
    print(f'Status: {resp.status_code}')
    if resp.status_code == 200:
        print(f'Response: {json.dumps(resp.json(), indent=2, ensure_ascii=False)}')
    else:
        print(f'Error: {resp.text}')
    print()
    return resp.status_code == 200

if __name__ == '__main__':
    print('=' * 60)
    print('设计链接 API 测试')
    print('=' * 60)
    print()
    
    # 测试1: 获取设计链接信息
    test_get_design_token()
    
    # 测试2: 生成设计链接Token
    token, url = test_generate_design_token()
    
    if token:
        # 测试3: 验证Token（使用新生成的token验证eu店铺）
        test_validate_design_token('eu', token)
        
        # 测试4: 禁用设计链接
        test_toggle_design_link('7e43fb37-cc32-42c4-9eea-07233cbb7d5e', True)
    
    print('=' * 60)
    print('测试完成')
    print('=' * 60)
