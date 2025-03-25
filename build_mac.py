import PyInstaller.__main__
import os
import shutil
import platform
import subprocess

def build_mac_app():
    # 检查是否在macOS系统上运行
    if platform.system() != "Darwin":
        print("警告：此脚本应在macOS系统上运行，当前系统是", platform.system())
    
    # 清理之前的构建文件
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # 创建调试版本的spec文件
    debug_wrapper = 'debug_macos_app.py'
    
    # 打包参数 - 使用更完整的配置
    args = [
        debug_wrapper,                     # 使用调试包装器替代主脚本
        '--name=Markdown2EPUB',            # 应用程序名称
        '--windowed',                      # GUI模式
        '--clean',                         # 清理临时文件
        '--noconfirm',                     # 不询问确认
        '--add-data=requirements.txt:.',   # 包含额外文件
        '--add-data=app.py:.',             # 包含主程序
        '--collect-all=markdownify',       # 确保收集完整的markdownify包
        '--collect-all=ebooklib',          # 确保收集完整的ebooklib包
        '--collect-all=PIL',               # 确保收集PIL/Pillow
        '--osx-bundle-identifier=com.md2epub.app',  # macOS包标识符
        '--hidden-import=PIL._tkinter_finder',  # 添加可能缺失的隐藏导入
        '--hidden-import=tkinter',         # 添加tkinter依赖
        '--hidden-import=tkinter.filedialog',  # 添加可能的tkinter组件
    ]
    
    # 如果有macOS格式的图标文件(.icns)，添加图标
    icon_path = 'icon.icns'
    if os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
    
    # 运行PyInstaller
    PyInstaller.__main__.run(args)
    
    # 拷贝可能缺失的资源文件到应用程序包中
    app_path = os.path.join('dist', 'Markdown2EPUB.app')
    resources_dir = os.path.join(app_path, 'Contents', 'Resources')
    
    print("打包完成，macOS应用程序在dist目录中。")
    
    # 修复权限
    print("修复应用程序权限...")
    subprocess.run(['chmod', '-R', '+x', app_path])

if __name__ == "__main__":
    build_mac_app()
