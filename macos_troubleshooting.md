# macOS应用程序故障排查指南

## 常见的闪退原因与解决方案

### 1. 权限问题

macOS应用在首次运行时可能会被阻止，尤其是从互联网下载的应用。

**解决方案:**
- 右键点击应用程序，选择"打开"
- 在弹出的对话框中点击"打开"
- 或前往 系统偏好设置 > 安全性与隐私 > 通用，允许应用运行

### 2. 查看闪退日志

如果应用闪退，可以查看日志了解原因：

- 查看桌面上的 `md2epub_crash_log.txt` 文件
- 或打开"控制台"应用（Applications > Utilities > Console），在"用户报告"中查找崩溃日志

### 3. 确认系统要求

- 确保macOS版本不低于10.14 Mojave
- 确保已安装最新系统更新

### 4. 使用终端运行应用

通过终端运行应用可以看到详细错误信息：

```bash
/Applications/Markdown2EPUB.app/Contents/MacOS/Markdown2EPUB
```

### 5. 可能的依赖问题

某些情况下，应用可能缺少系统依赖。尝试安装以下工具：

```bash
brew install python-tk
```

### 6. 清除缓存

有时缓存文件会导致问题，清除缓存可能有所帮助：

```bash
rm -rf ~/Library/Caches/Markdown2EPUB
rm -rf ~/Library/Application\ Support/Markdown2EPUB
```

## 联系支持

如果上述方法无法解决问题，请提供以下信息联系开发者：

1. macOS版本（点击苹果图标 > 关于本机）
2. 错误日志文件
3. 问题复现步骤

## 从源码运行

如果打包版本持续出现问题，可以尝试从源码运行：

```bash
# 克隆仓库
git clone https://github.com/yourusername/md2epub.git
cd md2epub

# 安装依赖
pip install -r requirements.txt

# 运行程序
python app.py
```
