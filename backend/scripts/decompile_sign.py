"""尝试反编译 SignUtil.class 查看签名算法"""
import os
import subprocess

# 路径
sdk_path = r'C:\Users\Administrator\Downloads\Edge浏览器下载\fpx-sdk-extracted'
sign_util_class = os.path.join(sdk_path, 'com', 'fpx', 'api', 'utils', 'SignUtil.class')
md5_util_class = os.path.join(sdk_path, 'com', 'fpx', 'api', 'utils', 'MD5Util.class')

print("=" * 60)
print("4PX SDK 签名算法分析")
print("=" * 60)

# 检查文件
if os.path.exists(sign_util_class):
    print(f"\n✅ 找到 SignUtil.class: {sign_util_class}")
    print(f"   文件大小: {os.path.getsize(sign_util_class)} bytes")
else:
    print(f"\n❌ 未找到 SignUtil.class")

if os.path.exists(md5_util_class):
    print(f"✅ 找到 MD5Util.class: {md5_util_class}")
    print(f"   文件大小: {os.path.getsize(md5_util_class)} bytes")
else:
    print(f"❌ 未找到 MD5Util.class")

# 尝试用 javap 反编译（如果有 Java 的话）
print("\n" + "=" * 60)
print("尝试反编译...")
print("=" * 60)

try:
    # 尝试使用 javap
    result = subprocess.run(
        ['javap', '-c', '-p', sign_util_class],
        capture_output=True,
        text=True,
        timeout=10
    )
    if result.returncode == 0:
        print("\nSignUtil 字节码:")
        print(result.stdout[:2000])  # 只显示前2000字符
    else:
        print(f"javap 失败: {result.stderr}")
except FileNotFoundError:
    print("❌ 未找到 javap，Java 未安装")
except Exception as e:
    print(f"❌ 反编译失败: {e}")

# 尝试读取类文件的字符串
print("\n" + "=" * 60)
print("从类文件提取字符串...")
print("=" * 60)

def extract_strings(filepath):
    """从二进制文件中提取可打印字符串"""
    with open(filepath, 'rb') as f:
        content = f.read()
    
    # 提取 ASCII 字符串
    strings = []
    current = b''
    for byte in content:
        if 32 <= byte < 127:  # 可打印 ASCII
            current += bytes([byte])
        else:
            if len(current) >= 4:  # 至少4个字符
                strings.append(current.decode('ascii', errors='ignore'))
            current = b''
    
    return strings

try:
    strings = extract_strings(sign_util_class)
    print(f"\nSignUtil 中的字符串 ({len(strings)} 个):")
    for s in strings[:30]:  # 只显示前30个
        if any(keyword in s.lower() for keyword in ['sign', 'md5', 'secret', 'app', 'key', 'param']):
            print(f"  🔑 {s}")
        else:
            print(f"     {s}")
except Exception as e:
    print(f"❌ 提取失败: {e}")
