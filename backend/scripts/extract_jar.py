"""解压 JAR 文件查看 SDK 源码"""
import zipfile
import os

jar_path = r'C:\Users\Administrator\Downloads\Edge浏览器下载\fpx-api-sdk-1.0.0-SNAPSHOT.jar'
extract_path = r'C:\Users\Administrator\Downloads\Edge浏览器下载\fpx-sdk-extracted'

print(f"JAR 文件: {jar_path}")
print(f"解压路径: {extract_path}")

if not os.path.exists(jar_path):
    print(f"❌ JAR 文件不存在: {jar_path}")
    exit(1)

os.makedirs(extract_path, exist_ok=True)

try:
    with zipfile.ZipFile(jar_path, 'r') as jar:
        print(f"\n📦 JAR 内容 ({len(jar.namelist())} 个文件):")
        
        # 只列出 .class 和 .java 文件
        source_files = [n for n in jar.namelist() if n.endswith(('.class', '.java')) and 'sign' in n.lower()]
        
        if source_files:
            print("\n🔍 可能包含签名算法的文件:")
            for name in source_files[:10]:
                print(f"  - {name}")
        
        # 解压所有文件
        jar.extractall(extract_path)
        print(f"\n✅ 已解压到: {extract_path}")
        
        # 列出目录结构
        print("\n📁 目录结构:")
        for root, dirs, files in os.walk(extract_path):
            level = root.replace(extract_path, '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = '  ' * (level + 1)
            for file in files[:5]:
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")
                
except Exception as e:
    print(f"❌ 解压失败: {e}")
