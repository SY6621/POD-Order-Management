"""分析 AffterentParam 和 ApiHttpClientUtils 类"""
import os

sdk_path = r'C:\Users\Administrator\Downloads\Edge浏览器下载\fpx-sdk-extracted'

def extract_all_strings(filepath):
    """从二进制文件中提取所有可打印字符串"""
    with open(filepath, 'rb') as f:
        content = f.read()
    
    strings = []
    current = b''
    for byte in content:
        if 32 <= byte < 127:
            current += bytes([byte])
        else:
            if len(current) >= 3:
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    return strings

# 分析 AffterentParam.class
affterent_param_path = os.path.join(sdk_path, 'com', 'fpx', 'api', 'model', 'AffterentParam.class')
api_http_client_path = os.path.join(sdk_path, 'com', 'fpx', 'api', 'utils', 'ApiHttpClientUtils.class')

print("=" * 60)
print("AffterentParam.class 中的所有字符串")
print("=" * 60)

strings = extract_all_strings(affterent_param_path)
for i, s in enumerate(strings):
    if 'get' in s.lower() or 'set' in s.lower() or 'app' in s.lower() or 'sign' in s.lower():
        print(f"{i:3d}: {s}")

print("\n" + "=" * 60)
print("ApiHttpClientUtils.class 中的所有字符串")
print("=" * 60)

strings = extract_all_strings(api_http_client_path)
for i, s in enumerate(strings):
    if any(keyword in s.lower() for keyword in ['sign', 'app', 'key', 'secret', 'param', 'format', 'method']):
        print(f"{i:3d}: {s}")
