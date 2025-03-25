import PyInstaller.__main__
import os
import shutil

def build_exe():
    # 清理之前的构建文件
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')
    
    # 打包参数
    args = [
        'app.py',                          # 主脚本
        '--name=Markdown2EPUB',            # 可执行文件名称
        '--onefile',                       # 打包成单个exe文件
        '--windowed',                      # 无控制台窗口
        '--clean',                         # 清理临时文件
        '--add-data=requirements.txt;.',   # 包含额外文件
    ]
    
    # 如果有图标文件，添加图标
    icon_path = 'icon.ico'
    if os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
    
    # 运行PyInstaller
    PyInstaller.__main__.run(args)
    
    print("打包完成，可执行文件在dist目录中。")

if __name__ == "__main__":
    build_exe()
