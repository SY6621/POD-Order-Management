"""分析 CommonRequestParam 类"""
import os

sdk_path = r'C:\Users\Administrator\Downloads\Edge浏览器下载\fpx-sdk-extracted'

def extract_all_strings(filepath):
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

# 分析 CommonRequestParam.class
common_param_path = os.path.join(sdk_path, 'com', 'fpx', 'api', 'model', 'CommonRequestParam.class')

print("=" * 60)
print("CommonRequestParam.class 中的所有字符串")
print("=" * 60)

strings = extract_all_strings(common_param_path)
for i, s in enumerate(strings):
    print(f"{i:3d}: {s}")

print("\n" + "=" * 60)
