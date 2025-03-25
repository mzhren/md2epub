#!/usr/bin/env python3
"""
验证打包的macOS应用程序是否包含所有必要组件
"""
import os
import sys
import platform
import subprocess
import shutil

def verify_app_package(app_path):
    if not os.path.exists(app_path):
        print(f"错误: 找不到应用程序包 {app_path}")
        return False
    
    print(f"验证应用程序包: {app_path}")
    
    # 验证基本结构
    required_dirs = [
        os.path.join(app_path, "Contents"),
        os.path.join(app_path, "Contents", "MacOS"),
        os.path.join(app_path, "Contents", "Resources")
    ]
    
    for directory in required_dirs:
        if not os.path.isdir(directory):
            print(f"错误: 缺少目录 {directory}")
            return False
    
    # 验证Info.plist文件
    info_plist = os.path.join(app_path, "Contents", "Info.plist")
    if not os.path.isfile(info_plist):
        print(f"错误: 缺少Info.plist文件")
        return False
    
    # 验证可执行文件
    executable = os.path.join(app_path, "Contents", "MacOS", "Markdown2EPUB")
    if not os.path.isfile(executable):
        print(f"错误: 缺少可执行文件")
        return False
    
    # 检查可执行文件权限
    if not os.access(executable, os.X_OK):
        print(f"警告: 可执行文件缺少执行权限，尝试修复...")
        try:
            os.chmod(executable, 0o755)
            print("权限已修复")
        except Exception as e:
            print(f"无法修复权限: {e}")
    
    # 验证依赖库
    try:
        if platform.system() == "Darwin":
            result = subprocess.run(['otool', '-L', executable], 
                                    capture_output=True, text=True)
            print("\n依赖库检查:")
            print(result.stdout)
    except Exception as e:
        print(f"无法检查依赖库: {e}")
    
    print("应用程序包结构验证完成")
    return True

def main():
    app_path = os.path.join('dist', 'Markdown2EPUB.app')
    if not os.path.exists(app_path):
        print(f"找不到应用程序: {app_path}")
        print("请先运行 build_mac.py 构建应用程序")
        return
    
    if verify_app_package(app_path):
        print("\n应用程序验证通过！")
        
        # 提供启动命令行以获取错误输出
        print("\n要在终端中运行应用以查看错误输出，请使用以下命令:")
        print(f"  {os.path.join(os.path.abspath(app_path), 'Contents', 'MacOS', 'Markdown2EPUB')}")
    else:
        print("\n应用程序验证失败，请检查构建过程")

if __name__ == "__main__":
    main()
