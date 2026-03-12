"""提取 SDK 中所有关键字符串"""
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

# 分析 SignUtil.class
sign_util_path = os.path.join(sdk_path, 'com', 'fpx', 'api', 'utils', 'SignUtil.class')
md5_util_path = os.path.join(sdk_path, 'com', 'fpx', 'api', 'utils', 'MD5Util.class')

print("=" * 60)
print("SignUtil.class 中的所有字符串")
print("=" * 60)

strings = extract_all_strings(sign_util_path)
for i, s in enumerate(strings):
    print(f"{i:3d}: {s}")

print("\n" + "=" * 60)
print("MD5Util.class 中的所有字符串")
print("=" * 60)

strings = extract_all_strings(md5_util_path)
for i, s in enumerate(strings):
    print(f"{i:3d}: {s}")
