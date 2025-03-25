import PyInstaller.__main__
import os
import shutil
import platform

def build_mac_app():
    # 检查是否在macOS系统上运行
    if platform.system() != "Darwin":
        print("警告：此脚本应在macOS系统上运行，当前系统是", platform.system())
    
    # 清理之前的构建文件
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # 打包参数 - 注意macOS上路径分隔符是冒号(:)而不是分号(;)
    args = [
        'app.py',                          # 主脚本
        '--name=Markdown2EPUB',            # 应用程序名称
        '--windowed',                      # GUI模式
        '--clean',                         # 清理临时文件
        '--add-data=requirements.txt:.',   # 包含额外文件，注意macOS使用:作为分隔符
        '--osx-bundle-identifier=com.md2epub.app'  # macOS包标识符
    ]
    
    # 如果有macOS格式的图标文件(.icns)，添加图标
    icon_path = 'icon.icns'
    if os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
    
    # 运行PyInstaller
    PyInstaller.__main__.run(args)
    
    print("打包完成，macOS应用程序在dist目录中。")

if __name__ == "__main__":
    build_mac_app()
