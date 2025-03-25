import os
import markdown
import ebooklib
from ebooklib import epub
from pathlib import Path
import re
import mimetypes
from bs4 import BeautifulSoup

class EpubConverter:
    def __init__(self):
        self.book = None
        self.images_dir = None
    
    def create_book(self, title, author, cover_path=None):
        """创建新的EPUB书籍"""
        self.book = epub.EpubBook()
        self.book.set_title(title)
        self.book.set_language('zh-CN')
        self.book.add_author(author)
        
        if cover_path and os.path.exists(cover_path):
            self.book.set_cover('cover.jpg', open(cover_path, 'rb').read())
    
    def add_markdown_file(self, md_path, custom_toc=None):
        """添加Markdown文件到EPUB"""
        if not self.book:
            raise ValueError("请先创建书籍")
        
        # 读取Markdown内容
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 转换Markdown为HTML，添加toc扩展以生成ID
        html_content = markdown.markdown(md_content, extensions=['extra', 'toc'])
        
        # 如果存在图片，处理图片（先从文档目录查找，再从指定图片目录查找）
        md_dir = os.path.dirname(md_path)  # 保存Markdown文档所在目录
        html_content = self.process_images(html_content, md_dir)
        
        # 创建章节
        file_name = os.path.basename(md_path).replace('.md', '')
        chapter = epub.EpubHtml(
            title=str(file_name),  # 确保标题是字符串
            file_name=f'{file_name}.xhtml'
        )
        chapter.content = html_content
        
        # 存储原始内容，用于后续提取标题
        chapter.original_content = html_content
        chapter.file_path = md_path
        
        # 添加章节到书籍
        self.book.add_item(chapter)
        return chapter
    
    def process_images(self, html_content, md_dir=None):
        """处理HTML中的图片引用，优先从Markdown文档目录查找，再从指定图片目录查找"""
        img_pattern = re.compile(r'<img[^>]+src="([^"]+)"[^>]*>')
        
        def replace_img(match):
            img_src = match.group(1)
            
            # 如果是网络URL，直接保留
            if img_src.startswith(('http://', 'https://')):
                return match.group(0)
            
            # 检查是否为绝对路径
            if os.path.isabs(img_src):
                # 如果是绝对路径且文件存在，添加到EPUB
                if os.path.exists(img_src):
                    return self.add_image_to_epub(img_src, match.group(0))
                return match.group(0)
            
            # 如果是相对路径，先尝试从Markdown文档目录查找
            img_found = False
            
            if md_dir:
                md_img_path = os.path.normpath(os.path.join(md_dir, img_src))
                if os.path.exists(md_img_path):
                    return self.add_image_to_epub(md_img_path, match.group(0))
            
            # 如果在文档目录没找到，再尝试从指定图片目录查找
            if self.images_dir:
                img_path = os.path.normpath(os.path.join(self.images_dir, img_src))
                if os.path.exists(img_path):
                    return self.add_image_to_epub(img_path, match.group(0))
                
                # 尝试直接在images_dir根目录查找图片文件名（不考虑子目录）
                img_filename = os.path.basename(img_src)
                img_path = os.path.normpath(os.path.join(self.images_dir, img_filename))
                if os.path.exists(img_path):
                    return self.add_image_to_epub(img_path, match.group(0))
            
            # 如果都找不到，返回原始标签
            return match.group(0)
        
        return re.sub(img_pattern, replace_img, html_content)
    
    def add_image_to_epub(self, img_path, img_tag):
        """将图片添加到EPUB并返回更新后的img标签"""
        img_name = os.path.basename(img_path)
        try:
            with open(img_path, 'rb') as f:
                img_file = f.read()
                
            img_item = epub.EpubItem(
                uid=img_name.replace('.', '_').replace('-', '_'),
                file_name=f'images/{img_name}',
                media_type=self.get_mimetype(img_path),
                content=img_file
            )
            self.book.add_item(img_item)
            
            # 返回更新后的img标签
            return img_tag.replace(f'src="{img_path}"', f'src="images/{img_name}"').replace(f"src='{img_path}'", f"src='images/{img_name}'")
        except Exception as e:
            print(f"添加图片出错: {str(e)}")
            return img_tag
    
    def get_mimetype(self, file_path):
        """获取文件的MIME类型"""
        mime_type, _ = mimetypes.guess_type(file_path)
        if (mime_type):
            return mime_type
        
        # 默认图片类型
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.jpg' or ext == '.jpeg':
            return 'image/jpeg'
        elif ext == '.png':
            return 'image/png'
        elif ext == '.gif':
            return 'image/gif'
        elif ext == '.svg':
            return 'image/svg+xml'
        
        return 'application/octet-stream'
    
    def add_markdown_directory(self, dir_path, custom_toc=None):
        """添加目录中的所有Markdown文件到EPUB"""
        if not self.book:
            raise ValueError("请先创建书籍")
        
        chapters = []
        md_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.md')])
        
        for md_file in md_files:
            md_path = os.path.join(dir_path, md_file)
            chapter = self.add_markdown_file(md_path, custom_toc)
            chapters.append(chapter)
        
        return chapters
    
    def generate_toc(self, chapters, custom_toc=None):
        """生成目录，提取Markdown文档中的前三级标题并保持层级关系"""
        if custom_toc:
            # 使用自定义目录
            toc = []
            for item in custom_toc:
                toc.append(epub.Link(item['file'], item['title'], item['id']))
            self.book.toc = toc
        else:
            # 从Markdown内容中提取标题生成目录
            toc = []
            
            for chapter in chapters:
                # 确保章节标题是字符串
                chapter_title = str(chapter.title)
                chapter_filename = chapter.file_name
                
                # 为章节创建一个Link对象
                chapter_link = epub.Link(chapter_filename, chapter_title, chapter_filename.replace('.', '_'))
                
                # 检查章节是否有原始内容，如果没有则仅添加章节标题
                if not hasattr(chapter, 'original_content'):
                    toc.append(chapter_link)
                    continue
                
                # 解析HTML提取标题
                soup = BeautifulSoup(chapter.original_content, 'html.parser')
                
                # 提取h1, h2, h3标题
                headings = soup.find_all(['h1', 'h2', 'h3'])
                
                if not headings:
                    # 如果没有找到标题，仅添加章节本身
                    toc.append(chapter_link)
                    continue
                
                # 记录当前的标题层级结构
                h1_sections = {}  # 存储h1标题和其对应的Section对象
                h2_sections = {}  # 存储h2标题和其对应的Section对象
                
                chapter_items = []  # 用于存储章节下的所有目录项
                
                for heading in headings:
                    level = int(heading.name[1])  # 1, 2, 或 3
                    heading_text = str(heading.get_text())
                    heading_id = heading.get('id', '')
                    
                    if not heading_id:
                        # 如果没有ID，使用文本创建一个
                        heading_id = 'heading_' + re.sub(r'\W+', '_', heading_text.lower())
                    
                    heading_link = f"{chapter_filename}#{heading_id}"
                    link_id = heading_link.replace('.', '_').replace('#', '_')
                    
                    # 创建Link对象
                    link = epub.Link(heading_link, heading_text, link_id)
                    
                    # 基于标题级别构建层级结构
                    if level == 1:
                        # 为h1标题创建Section
                        section = epub.Section(heading_text)
                        h1_sections[heading_text] = {
                            'section': section,
                            'link': link,
                            'items': []
                        }
                        chapter_items.append((section, [link]))
                        current_h1 = heading_text
                    elif level == 2 and current_h1 in h1_sections:
                        # 为h2标题创建Section
                        section = epub.Section(heading_text)
                        h2_sections[heading_text] = {
                            'section': section,
                            'link': link,
                            'items': [],
                            'parent': current_h1
                        }
                        h1_sections[current_h1]['items'].append((section, [link]))
                        current_h2 = heading_text
                    elif level == 3 and current_h2 in h2_sections:
                        # h3标题直接添加到对应h2下
                        h2_sections[current_h2]['items'].append(link)
                    elif level == 3 and current_h1 in h1_sections:
                        # h3标题，但没有h2父级，直接附加到h1
                        h1_sections[current_h1]['items'].append(link)
                    elif level == 2:
                        # h2标题，但没有h1父级，直接添加到章节
                        section = epub.Section(heading_text)
                        chapter_items.append((section, [link]))
                        h2_sections[heading_text] = {
                            'section': section,
                            'link': link,
                            'items': []
                        }
                        current_h2 = heading_text
                        current_h1 = None
                    else:
                        # 孤立的h3，直接添加到章节
                        chapter_items.append(link)
                
                # 如果有标题项，使用这些作为章节的子项
                if chapter_items:
                    # 创建章节Section
                    chapter_section = epub.Section(chapter_title)
                    toc.append((chapter_section, chapter_items))
                else:
                    # 没有标题，只添加章节链接
                    toc.append(chapter_link)
            
            # 设置目录
            self.book.toc = toc
        
        # 添加默认NCX和NAV
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        
        # 定义CSS样式
        style = 'body { font-family: Times, Times New Roman, serif; }'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        self.book.add_item(nav_css)
        
        # 定义书脊
        self.book.spine = ['nav'] + chapters
    
    def save_epub(self, output_path):
        """保存EPUB文件"""
        if not self.book:
            raise ValueError("请先创建书籍")
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 写入EPUB文件
        epub.write_epub(output_path, self.book, {})
        return output_path
    
    def convert_markdown_to_epub(self, input_path, output_path, title, author, cover_path=None, custom_toc=None, images_dir=None):
        """将Markdown转换为EPUB的主函数"""
        # 创建书籍
        self.create_book(title, author, cover_path)
        
        # 设置图片目录
        self.images_dir = images_dir
        
        # 处理输入路径（文件或目录）
        if os.path.isfile(input_path) and input_path.endswith('.md'):
            chapters = [self.add_markdown_file(input_path)]
        elif os.path.isdir(input_path):
            chapters = self.add_markdown_directory(input_path)
        else:
            raise ValueError("输入路径必须是Markdown文件或包含Markdown文件的目录")
        
        # 生成目录
        self.generate_toc(chapters, custom_toc)
        
        # 保存EPUB
        return self.save_epub(output_path)
