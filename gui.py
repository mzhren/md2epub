import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

class MarkdownToEpubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown转EPUB工具")
        self.root.geometry("700x700")
        self.root.resizable(True, True)
        
        self.create_widgets()
        self.layout_widgets()
    
    def create_widgets(self):
        # 输入文件/目录选择
        self.input_frame = ttk.LabelFrame(self.root, text="输入")
        self.input_path = tk.StringVar()
        self.input_entry = ttk.Entry(self.input_frame, textvariable=self.input_path, width=50)
        self.input_file_btn = ttk.Button(self.input_frame, text="选择文件", command=self.select_input_file)
        self.input_dir_btn = ttk.Button(self.input_frame, text="选择目录", command=self.select_input_dir)
        
        # 图片目录选择
        self.images_frame = ttk.LabelFrame(self.root, text="图片目录")
        self.images_path = tk.StringVar()
        self.images_entry = ttk.Entry(self.images_frame, textvariable=self.images_path, width=50)
        self.images_btn = ttk.Button(self.images_frame, text="选择图片目录", command=self.select_images_dir)
        self.default_images_btn = ttk.Button(self.images_frame, text="使用默认图片目录", command=self.use_default_images_dir)
        
        # 输出文件选择
        self.output_frame = ttk.LabelFrame(self.root, text="输出")
        self.output_path = tk.StringVar()
        self.output_entry = ttk.Entry(self.output_frame, textvariable=self.output_path, width=50)
        self.output_btn = ttk.Button(self.output_frame, text="选择位置", command=self.select_output_path)
        
        # 书籍信息
        self.book_info_frame = ttk.LabelFrame(self.root, text="书籍信息")
        
        # 标题
        self.title_label = ttk.Label(self.book_info_frame, text="标题:")
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(self.book_info_frame, textvariable=self.title_var, width=40)
        
        # 作者
        self.author_label = ttk.Label(self.book_info_frame, text="作者:")
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(self.book_info_frame, textvariable=self.author_var, width=40)
        
        # 封面
        self.cover_label = ttk.Label(self.book_info_frame, text="封面:")
        self.cover_path = tk.StringVar()
        self.cover_entry = ttk.Entry(self.book_info_frame, textvariable=self.cover_path, width=40)
        self.cover_btn = ttk.Button(self.book_info_frame, text="选择封面", command=self.select_cover)
        
        # 目录选项
        self.toc_frame = ttk.LabelFrame(self.root, text="目录选项")
        self.toc_type = tk.StringVar(value="auto")
        self.auto_toc_radio = ttk.Radiobutton(self.toc_frame, text="自动生成目录", variable=self.toc_type, value="auto", command=self.toggle_toc_type)
        self.custom_toc_radio = ttk.Radiobutton(self.toc_frame, text="自定义目录", variable=self.toc_type, value="custom", command=self.toggle_toc_type)
        
        # 自定义目录编辑区
        self.toc_editor_label = ttk.Label(self.toc_frame, text="每行一个目录项，格式: 标题|文件名")
        self.toc_editor = ScrolledText(self.toc_frame, height=10, width=50, state=tk.DISABLED)
        
        # 转换按钮
        self.convert_btn = ttk.Button(self.root, text="转换为EPUB", command=self.convert)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
    
    def layout_widgets(self):
        # 输入框布局
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)
        self.input_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.input_file_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.input_dir_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 图片目录布局
        self.images_frame.pack(fill=tk.X, padx=10, pady=5)
        self.images_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.images_btn.pack(side=tk.LEFT, padx=5, pady=5)
        self.default_images_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 输出框布局
        self.output_frame.pack(fill=tk.X, padx=10, pady=5)
        self.output_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.output_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 书籍信息布局
        self.book_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.title_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.author_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        self.cover_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.cover_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.cover_btn.grid(row=2, column=2, padx=5, pady=5)
        
        # 目录选项布局
        self.toc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.auto_toc_radio.pack(anchor=tk.W, padx=5, pady=2)
        self.custom_toc_radio.pack(anchor=tk.W, padx=5, pady=2)
        self.toc_editor_label.pack(anchor=tk.W, padx=5, pady=2)
        self.toc_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 转换按钮布局
        self.convert_btn.pack(pady=10)
        
        # 状态栏布局
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="选择Markdown文件",
            filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
        )
        if file_path:
            self.input_path.set(file_path)
            # 自动设置标题为文件名
            self.title_var.set(os.path.basename(file_path).replace('.md', ''))
    
    def select_input_dir(self):
        dir_path = filedialog.askdirectory(title="选择包含Markdown文件的目录")
        if dir_path:
            self.input_path.set(dir_path)
            # 自动设置标题为目录名
            self.title_var.set(os.path.basename(dir_path))
    
    def select_output_path(self):
        file_path = filedialog.asksaveasfilename(
            title="保存EPUB文件",
            defaultextension=".epub",
            filetypes=[("EPUB文件", "*.epub"), ("所有文件", "*.*")]
        )
        if file_path:
            self.output_path.set(file_path)
    
    def select_cover(self):
        file_path = filedialog.askopenfilename(
            title="选择封面图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png"), ("所有文件", "*.*")]
        )
        if file_path:
            self.cover_path.set(file_path)
    
    def select_images_dir(self):
        dir_path = filedialog.askdirectory(title="选择包含图片的目录")
        if dir_path:
            self.images_path.set(dir_path)
    
    def toggle_toc_type(self):
        if self.toc_type.get() == "auto":
            self.toc_editor.config(state=tk.DISABLED)
        else:
            self.toc_editor.config(state=tk.NORMAL)
    
    def parse_custom_toc(self):
        """解析自定义目录文本"""
        if self.toc_type.get() != "custom":
            return None
        
        toc_text = self.toc_editor.get(1.0, tk.END)
        if not toc_text.strip():
            return None
        
        toc_items = []
        for line in toc_text.splitlines():
            line = line.strip()
            if not line:
                continue
            
            parts = line.split('|', 1)
            if len(parts) == 2:
                title, file_name = parts
                toc_items.append({
                    'title': title.strip(),
                    'file': file_name.strip(),
                    'id': file_name.strip().replace('.', '_')
                })
        
        return toc_items if toc_items else None
    
    def convert(self):
        # 验证输入
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        title = self.title_var.get()
        author = self.author_var.get()
        cover_path = self.cover_path.get() if self.cover_path.get() else None
        images_dir = self.images_path.get() if self.images_path.get() else None
        
        if not input_path:
            messagebox.showerror("错误", "请选择输入文件或目录")
            return
        
        if not output_path:
            messagebox.showerror("错误", "请选择输出文件路径")
            return
        
        if not title:
            messagebox.showerror("错误", "请输入书籍标题")
            return
        
        if not author:
            messagebox.showerror("错误", "请输入作者名称")
            return
        
        # 解析自定义目录
        custom_toc = self.parse_custom_toc()
        
        # 更新状态
        self.status_var.set("正在转换...")
        self.root.update()
        
        from converter import EpubConverter
        converter = EpubConverter()
        output_file = converter.convert_markdown_to_epub(
            input_path, output_path, title, author, cover_path, custom_toc, images_dir
        )
        messagebox.showinfo("成功", f"转换完成！\n文件已保存到: {output_file}")
        self.status_var.set("转换完成")
    
    def use_default_images_dir(self):
        """设置默认图片目录（Markdown文档所在目录下的images子目录）"""
        input_path = self.input_path.get()
        
        if not input_path:
            messagebox.showerror("错误", "请先选择Markdown文件或目录")
            return
        
        if os.path.isfile(input_path):
            # 如果选择的是文件，使用其所在目录
            base_dir = os.path.dirname(input_path)
        else:
            # 如果选择的是目录，直接使用该目录
            base_dir = input_path
        
        # 构建默认图片目录路径
        default_images_dir = os.path.join(base_dir, "images")
        
        # 检查目录是否存在
        if not os.path.exists(default_images_dir):
            result = messagebox.askquestion("创建目录", 
                f"默认图片目录 '{default_images_dir}' 不存在，是否创建？")
            if result == 'yes':
                try:
                    os.makedirs(default_images_dir)
                except Exception as e:
                    messagebox.showerror("错误", f"无法创建目录: {str(e)}")
                    return
            else:
                return
        
        # 设置图片目录路径
        self.images_path.set(default_images_dir)
