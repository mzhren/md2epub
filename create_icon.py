from PIL import Image, ImageDraw, ImageFont
import os
import platform
import subprocess

def create_icon():
    # 创建一个512x512的图像，带有透明背景
    img = Image.new('RGBA', (512, 512), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景圆形
    draw.ellipse((50, 50, 462, 462), fill=(65, 105, 225))
    
    # 尝试加载字体，如果找不到则使用默认字体
    try:
        if platform.system() == "Windows":
            font = ImageFont.truetype("arial.ttf", 200)
        elif platform.system() == "Darwin":  # macOS
            font = ImageFont.truetype("/System/Library/Fonts/SFNSDisplay.ttf", 200)
        else:  # Linux及其他系统
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 200)
    except IOError:
        font = ImageFont.load_default()
    
    # 在中间绘制文本
    draw.text((170, 150), "M→E", fill="white", font=font)
    
    # 保存为PNG
    img.save("icon.png")
    
    # 创建各种尺寸的图标
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    icons = []
    
    for size in sizes:
        resized_img = img.resize((size, size), Image.LANCZOS)
        icon_filename = f"icon_{size}x{size}.png"
        resized_img.save(icon_filename)
        icons.append(icon_filename)
    
    # 保存为Windows ICO文件
    img.save("icon.ico", format="ICO", sizes=[(size, size) for size in sizes if size <= 256])
    
    # 创建macOS ICNS文件
    if platform.system() == "Darwin":  # 如果在macOS上运行
        try:
            # 创建临时iconset目录
            if not os.path.exists("icon.iconset"):
                os.makedirs("icon.iconset")
            
            # 拷贝图标到iconset目录
            for size in [16, 32, 128, 256, 512]:
                # 1x 分辨率
                shutil.copyfile(f"icon_{size}x{size}.png", f"icon.iconset/icon_{size}x{size}.png")
                # 2x 分辨率 (Retina)
                if size*2 in sizes:
                    shutil.copyfile(f"icon_{size*2}x{size*2}.png", f"icon.iconset/icon_{size}x{size}@2x.png")
            
            # 使用iconutil命令将iconset转换为icns
            subprocess.run(["iconutil", "-c", "icns", "icon.iconset"])
            
            # 清理临时文件
            shutil.rmtree("icon.iconset")
            print("已创建macOS图标文件: icon.icns")
        except Exception as e:
            print(f"创建macOS图标时出错: {str(e)}")
            print("您可以手动安装libicns工具并转换，或使用在线转换服务。")
    else:
        print("未在macOS上运行，跳过创建.icns文件。如需macOS图标，请在macOS系统上运行此脚本或使用在线转换服务。")
    
    # 清理临时文件
    for icon in icons:
        if os.path.exists(icon):
            os.remove(icon)
    
    print("图标文件已创建完成")

if __name__ == "__main__":
    create_icon()
