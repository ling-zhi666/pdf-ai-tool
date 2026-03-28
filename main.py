import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import subprocess
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    HAS_TKINTERDND2 = True
except ImportError:
    HAS_TKINTERDND2 = False
from typing import List, Dict
from datetime import datetime
from theme import get_colors, toggle_theme, is_dark

# 统一配色体系（色彩丰富但不杂乱，有统一调性）
# 主色调（品牌色）：#165DFF （深邃科技蓝，用于主按钮、选中态、高亮边框）
# 强调色（操作色）：#FF7D00 （活力橙，用于次要强调、加载状态、提醒）
# 功能状态色：
#   成功态：#00B42A （用于成功提示、已完成状态）
#   警告态：#FF9A2E （用于进行中、提醒状态）
#   错误态：#F53F3F （用于错误提示、失败状态）
# 中性色体系（保证层次感与可读性）：
#   窗口背景色：#F5F7FA
#   卡片/内容区背景：#FFFFFF
#   列表隔行背景：#F9FAFC
#   hover态背景：#E8F3FF
#   正文文本色：#1D2129
#   次要文本色：#4E5969
#   辅助文本色：#86909C
#   边框色：#E5E6EB

# 从主题系统获取颜色常量
COLORS = get_colors()
COLOR_PRIMARY = COLORS["PRIMARY"]
COLOR_ACCENT = COLORS["ACCENT"]
COLOR_SUCCESS = COLORS["SUCCESS"]
COLOR_WARNING = COLORS["WARNING"]
COLOR_ERROR = COLORS["ERROR"]
COLOR_BG_WINDOW = COLORS["BG_WINDOW"]
COLOR_BG_CARD = COLORS["BG_CARD"]
COLOR_BG_LIST_EVEN = COLORS["BG_LIST_EVEN"]
COLOR_BG_HOVER = COLORS["BG_HOVER"]
COLOR_TEXT_PRIMARY = COLORS["TEXT_PRIMARY"]
COLOR_TEXT_SECONDARY = COLORS["TEXT_SECONDARY"]
COLOR_TEXT_TERTIARY = COLORS["TEXT_TERTIARY"]
COLOR_BORDER = COLORS["BORDER"]

# 导入自定义模块
from db_manager import (
    init_db, add_record, get_all_records, search_records,
    get_record_by_id, delete_record, update_summary, update_tags, update_content,
    search_by_tag, full_text_search, get_all_tags, get_records_by_tags,
    search_by_title, search_by_content, reset_record_ids
)
from document_processor import extract_text_from_document, validate_document, get_file_type
from ai_summarizer import generate_summary, parse_summary_to_dict


class PDFAITool:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF AI 智能摘要工具 v2.0")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # 初始化数据库
        try:
            init_db()
        except Exception as e:
            messagebox.showerror("数据库初始化失败", f"无法初始化数据库: {e}")
            self.root.destroy()
            return

        # 创建界面
        self.create_ui()

        # 设置拖拽导入支持
        if HAS_TKINTERDND2:
            self._setup_drag_drop()
        else:
            print("提示: tkinterdnd2未安装，拖拽功能不可用。请运行: pip install tkinterdnd2")

        # 加载已有记录
        self.load_records()

        # 窗口居中
        self.center_window()

    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_theme_mode(self):
        """Toggle between light and dark theme."""
        global COLOR_PRIMARY, COLOR_ACCENT, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR
        global COLOR_BG_WINDOW, COLOR_BG_CARD, COLOR_BG_LIST_EVEN, COLOR_BG_HOVER
        global COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY, COLOR_TEXT_TERTIARY, COLOR_BORDER

        toggle_theme()
        COLORS = get_colors()

        COLOR_PRIMARY = COLORS["PRIMARY"]
        COLOR_ACCENT = COLORS["ACCENT"]
        COLOR_SUCCESS = COLORS["SUCCESS"]
        COLOR_WARNING = COLORS["WARNING"]
        COLOR_ERROR = COLORS["ERROR"]
        COLOR_BG_WINDOW = COLORS["BG_WINDOW"]
        COLOR_BG_CARD = COLORS["BG_CARD"]
        COLOR_BG_LIST_EVEN = COLORS["BG_LIST_EVEN"]
        COLOR_BG_HOVER = COLORS["BG_HOVER"]
        COLOR_TEXT_PRIMARY = COLORS["TEXT_PRIMARY"]
        COLOR_TEXT_SECONDARY = COLORS["TEXT_SECONDARY"]
        COLOR_TEXT_TERTIARY = COLORS["TEXT_TERTIARY"]
        COLOR_BORDER = COLORS["BORDER"]

        # Update UI colors
        self._refresh_ui_colors()

        self.status_label.config(
            text=f"主题已切换为{'深色' if is_dark() else '浅色'}模式",
            fg=COLOR_TEXT_SECONDARY
        )

    def _refresh_ui_colors(self):
        """Refresh UI colors after theme change."""
        # Update root background
        self.root.config(bg=COLOR_BG_WINDOW)

        # Update treeview colors
        style = ttk.Style()
        style.configure('Treeview',
                        background=COLOR_BG_CARD,
                        foreground=COLOR_TEXT_PRIMARY,
                        fieldbackground=COLOR_BG_CARD)
        style.configure('Treeview.Heading',
                        background=COLOR_BG_CARD,
                        foreground=COLOR_TEXT_SECONDARY)
        style.map('Treeview',
                  background=[('selected', COLOR_PRIMARY)],
                  foreground=[('selected', 'white')])
        style.map('Treeview',
                  background=[('selected', COLOR_PRIMARY)],
                  foreground=[('selected', 'white')])

        # Update button colors
        if hasattr(self, 'select_btn'):
            self.select_btn.config(bg=COLOR_PRIMARY, fg="white")
        if hasattr(self, 'generate_btn'):
            self.generate_btn.config(bg=COLOR_PRIMARY, fg="white")
        if hasattr(self, 'open_btn'):
            self.open_btn.config(bg=COLOR_BG_CARD, fg=COLOR_PRIMARY)
        if hasattr(self, 'delete_btn'):
            self.delete_btn.config(bg=COLOR_BG_CARD, fg=COLOR_ERROR)
        if hasattr(self, 'theme_btn'):
            self.theme_btn.config(bg=COLOR_BG_CARD, fg=COLOR_TEXT_PRIMARY)
        if hasattr(self, 'search_entry'):
            self.search_entry.config(
                bg="white",
                fg=COLOR_TEXT_PRIMARY,
                highlightbackground=COLOR_BORDER
            )

        # Update frame backgrounds
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=COLOR_BG_WINDOW)

        # Reload records to refresh list colors
        if hasattr(self, 'tree'):
            self.load_records()

    def _setup_drag_drop(self):
        """设置拖拽文件导入"""
        # 使用顶层窗口作为drop target
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_file_drop)

    def on_file_drop(self, event):
        """处理拖拽的文件"""
        if not event.data:
            return

        # 解析拖拽的文件路径
        files = self.root.tk.splitlist(event.data)

        # 过滤出支持的文件类型
        supported_extensions = ('.pdf', '.txt', '.doc', '.docx', '.xls', '.xlsx')
        valid_files = [f for f in files if any(f.lower().endswith(ext) for ext in supported_extensions)]

        if not valid_files:
            messagebox.showwarning("提示", "不支持的文件格式\n请拖拽 PDF、TXT、Word 或 Excel 文件")
            return

        # 处理拖拽的文件
        self.set_status(f"正在导入 {len(valid_files)} 个文件...", loading=True)
        self.select_btn.config(state=tk.DISABLED)
        self.generate_btn.config(state=tk.DISABLED)

        thread = threading.Thread(target=self._process_document_files, args=(valid_files,))
        thread.daemon = True
        thread.start()

    def show_shortcut_hints(self):
        """显示快捷键提示"""
        hints = "快捷键: Ctrl+N导入 | Ctrl+G生成摘要 | Ctrl+O打开 | Delete删除 | Ctrl+F搜索 | F5刷新 | F1帮助"
        self.status_label.config(text=hints, fg=COLOR_TEXT_TERTIARY)
        # 5秒后恢复状态文本
        if hasattr(self, '_status_restore_id'):
            self.root.after_cancel(self._status_restore_id)
        self._status_restore_id = self.root.after(5000, lambda: self.status_label.config(text="就绪", fg=COLOR_TEXT_SECONDARY))

    def show_context_menu(self, event):
        """显示右键菜单"""
        # 选中右键点击的项
        item = self.tree.identify_row(event.y)
        if item:
            if item not in self.tree.selection():
                self.tree.selection_set(item)
            self.tree.focus(item)
        else:
            return  # 点击空白区域不显示菜单

        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def regenerate_summary(self):
        """重新生成摘要（先清空再生成）"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选择要重新生成摘要的记录")
            return

        item = selected_items[0]
        record_id = self.tree.item(item)['values'][0]

        # 确认操作
        result = messagebox.askyesno(
            "确认重新生成",
            "将清空现有摘要并重新生成，确定继续？"
        )
        if not result:
            return

        # 清空摘要
        update_summary(record_id, "")
        self.load_records()
        self.status_label.config(text="摘要已清空，请重新选择生成", fg=COLOR_WARNING)

    def copy_file_path(self):
        """复制文件路径到剪贴板"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        record_id = self.tree.item(item)['values'][0]
        record = get_record_by_id(record_id)

        if record:
            self.root.clipboard_clear()
            self.root.clipboard_append(record['file_path'])
            self.status_label.config(text="文件路径已复制到剪贴板", fg=COLOR_SUCCESS)

    def copy_summary(self):
        """复制摘要到剪贴板"""
        selected_items = self.tree.selection()
        if not selected_items:
            return

        item = selected_items[0]
        record_id = self.tree.item(item)['values'][0]
        record = get_record_by_id(record_id)

        if record and record.get('summary'):
            self.root.clipboard_clear()
            self.root.clipboard_append(record['summary'])
            self.status_label.config(text="摘要已复制到剪贴板", fg=COLOR_SUCCESS)
        else:
            self.status_label.config(text="无摘要可复制", fg=COLOR_WARNING)

    def edit_tags(self):
        """编辑标签对话框"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("提示", "请先选择要编辑标签的记录")
            return

        item = selected_items[0]
        record_id = self.tree.item(item)['values'][0]
        record = get_record_by_id(record_id)

        if not record:
            return

        # 创建标签编辑对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑标签")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()

        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f'+{x}+{y}')

        tk.Label(dialog, text="标签（用逗号分隔）：", font=("微软雅黑", 10)).pack(pady=(20, 5))

        entry = tk.Entry(dialog, font=("微软雅黑", 10), width=40)
        entry.pack(pady=10)
        entry.insert(0, record.get('tags') or "")
        entry.select_range(0, tk.END)
        entry.focus_set()

        def save_tags():
            tags = entry.get().strip()
            if update_tags(record_id, tags):
                self.load_records()
                self.status_label.config(text="标签已更新", fg=COLOR_SUCCESS)
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="保存", command=save_tags, bg=COLOR_PRIMARY, fg="white",
                  font=("微软雅黑", 10), relief="flat", padx=20).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="取消", command=dialog.destroy,
                  font=("微软雅黑", 10), relief="flat", padx=20).pack(side=tk.LEFT, padx=10)

    def export_to_excel(self):
        """导出记录到Excel"""
        from exporter import export_to_excel, can_export_excel

        if not can_export_excel():
            messagebox.showerror("导出失败", "请先安装openpyxl: pip install openpyxl")
            return

        # 获取要导出的记录
        records = get_all_records()
        if not records:
            messagebox.showwarning("提示", "没有可导出的记录")
            return

        # 选择保存位置
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            title="导出Excel文件",
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx")],
            initialfile=f"PDF摘要导出_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        if not file_path:
            return

        try:
            export_to_excel(records, file_path)
            messagebox.showinfo("导出成功", f"已导出 {len(records)} 条记录到:\n{file_path}")
            self.status_label.config(text=f"已导出到: {os.path.basename(file_path)}", fg=COLOR_SUCCESS)
        except Exception as e:
            messagebox.showerror("导出失败", f"导出时出错:\n{e}")

    def export_to_word(self):
        """导出记录到Word"""
        from exporter import export_to_word, can_export_word

        if not can_export_word():
            messagebox.showerror("导出失败", "请先安装python-docx: pip install python-docx")
            return

        # 获取要导出的记录
        records = get_all_records()
        if not records:
            messagebox.showwarning("提示", "没有可导出的记录")
            return

        # 选择保存位置
        from tkinter import filedialog
        file_path = filedialog.asksaveasfilename(
            title="导出Word文件",
            defaultextension=".docx",
            filetypes=[("Word文件", "*.docx")],
            initialfile=f"PDF摘要导出_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )

        if not file_path:
            return

        try:
            export_to_word(records, file_path)
            messagebox.showinfo("导出成功", f"已导出 {len(records)} 条记录到:\n{file_path}")
            self.status_label.config(text=f"已导出到: {os.path.basename(file_path)}", fg=COLOR_SUCCESS)
        except Exception as e:
            messagebox.showerror("导出失败", f"导出时出错:\n{e}")

    def create_ui(self):
        """创建用户界面"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # ========== 顶部操作栏 ==========
        top_bar = tk.Frame(main_frame, bg=COLOR_BG_CARD, height=60)
        top_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 16))
        top_bar.grid_propagate(False)
        top_bar.columnconfigure(0, weight=1)
        top_bar.columnconfigure(1, weight=0)

        # 顶部边框
        top_bar.config(highlightbackground=COLOR_BORDER, highlightthickness=1)

        # 左侧按钮区
        button_container = tk.Frame(top_bar, bg=COLOR_BG_CARD)
        button_container.grid(row=0, column=0, padx=(0, 20), pady=12)

        # 主按钮
        self.select_btn = tk.Button(
            button_container,
            text="批量选择PDF文件",
            command=self.select_pdf_files,
            bg=COLOR_PRIMARY,
            fg="white",
            font=("微软雅黑", 10, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            bd=0,
            cursor="hand2"
        )
        self.select_btn.pack(side=tk.LEFT, padx=10)

        self.generate_btn = tk.Button(
            button_container,
            text="生成结构化摘要",
            command=self.batch_generate_summary,
            bg=COLOR_PRIMARY,
            fg="white",
            font=("微软雅黑", 10, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            bd=0,
            cursor="hand2"
        )
        self.generate_btn.pack(side=tk.LEFT, padx=10)

        # 次按钮
        self.open_btn = tk.Button(
            button_container,
            text="打开原文件",
            command=self.open_selected_file,
            bg=COLOR_BG_CARD,
            fg=COLOR_PRIMARY,
            font=("微软雅黑", 10, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            bd=1,
            highlightthickness=1,
            highlightbackground=COLOR_PRIMARY,
            cursor="hand2"
        )
        self.open_btn.pack(side=tk.LEFT, padx=10)

        # 删除按钮
        self.delete_btn = tk.Button(
            button_container,
            text="删除文件",
            command=self.delete_selected_file,
            bg=COLOR_BG_CARD,
            fg=COLOR_ERROR,
            font=("微软雅黑", 10, "bold"),
            relief="flat",
            padx=16,
            pady=8,
            bd=1,
            highlightthickness=1,
            highlightbackground=COLOR_ERROR,
            cursor="hand2"
        )
        self.delete_btn.pack(side=tk.LEFT, padx=10)

        # 按钮hover效果
        def on_enter(e, btn):
            if btn == self.select_btn or btn == self.generate_btn:
                btn.config(bg=COLOR_PRIMARY, fg="white", relief="flat")
            elif btn == self.delete_btn:
                btn.config(bg=COLOR_ERROR, fg="white")
            else:
                btn.config(bg=COLOR_BG_HOVER, fg=COLOR_PRIMARY)

        def on_leave(e, btn):
            if btn == self.select_btn or btn == self.generate_btn:
                btn.config(bg=COLOR_PRIMARY, fg="white", relief="flat")
            elif btn == self.delete_btn:
                btn.config(bg=COLOR_BG_CARD, fg=COLOR_ERROR)
            else:
                btn.config(bg=COLOR_BG_CARD, fg=COLOR_PRIMARY)

        self.select_btn.bind("<Enter>", lambda e: on_enter(e, self.select_btn))
        self.select_btn.bind("<Leave>", lambda e: on_leave(e, self.select_btn))
        self.generate_btn.bind("<Enter>", lambda e: on_enter(e, self.generate_btn))
        self.generate_btn.bind("<Leave>", lambda e: on_leave(e, self.generate_btn))
        self.open_btn.bind("<Enter>", lambda e: on_enter(e, self.open_btn))
        self.open_btn.bind("<Leave>", lambda e: on_leave(e, self.open_btn))
        self.delete_btn.bind("<Enter>", lambda e: on_enter(e, self.delete_btn))
        self.delete_btn.bind("<Leave>", lambda e: on_leave(e, self.delete_btn))

        # 右侧检索区
        search_container = tk.Frame(top_bar, bg=COLOR_BG_CARD)
        search_container.grid(row=0, column=1, sticky=(tk.E))
        search_container.columnconfigure(0, weight=0)
        search_container.columnconfigure(1, weight=0)

        # 标签筛选下拉框
        self.tag_filter_var = tk.StringVar(value="全部标签")
        self.tag_filter = ttk.Combobox(
            search_container,
            textvariable=self.tag_filter_var,
            values=["全部标签"],
            state="readonly",
            width=10,
            font=("微软雅黑", 9)
        )
        self.tag_filter.grid(row=0, column=0, padx=(0, 5))
        self.tag_filter.bind('<<ComboboxSelected>>', self.on_tag_filter_changed)

        # 搜索框
        self.search_entry = tk.Entry(
            search_container,
            font=("微软雅黑", 10),
            fg=COLOR_TEXT_TERTIARY,
            bg="white",
            relief="flat",
            bd=1,
            highlightthickness=1,
            highlightbackground=COLOR_BORDER,
            insertbackground=COLOR_TEXT_PRIMARY,
            width=20
        )
        self.search_entry.grid(row=0, column=1, padx=(0, 5))
        self.search_entry.insert(0, "输入关键词检索")
        self.search_entry.bind("<FocusIn>", self.on_search_focus_in)
        self.search_entry.bind("<FocusOut>", self.on_search_focus_out)
        self.search_entry.bind("<Return>", lambda e: self.search_records())

        # Theme toggle button
        self.theme_btn = tk.Button(
            search_container,
            text="🌓",
            command=self.toggle_theme_mode,
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT_PRIMARY,
            font=("Segoe UI Emoji", 10),
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=8
        )
        self.theme_btn.grid(row=0, column=2, padx=(5, 0))

        # 导出按钮
        self.export_var = tk.StringVar(value="导出")
        export_btn = tk.Menubutton(
            search_container,
            text="📤 导出",
            font=("微软雅黑", 9),
            bg=COLOR_BG_CARD,
            fg=COLOR_PRIMARY,
            relief="flat",
            padx=10,
            cursor="hand2"
        )
        export_btn.grid(row=0, column=3, padx=(5, 0))

        export_menu = tk.Menu(export_btn, tearoff=0)
        export_menu.add_command(label="导出到 Excel (.xlsx)", command=self.export_to_excel)
        export_menu.add_command(label="导出到 Word (.docx)", command=self.export_to_word)
        export_btn['menu'] = export_menu

        # 搜索框hover效果
        def on_search_enter(e):
            self.search_entry.config(highlightbackground=COLOR_PRIMARY)

        def on_search_leave(e):
            self.search_entry.config(highlightbackground=COLOR_BORDER)

        self.search_entry.bind("<Enter>", on_search_enter)
        self.search_entry.bind("<Leave>", on_search_leave)

        # ========== 中间内容区 ==========
        content_frame = tk.Frame(main_frame, bg=COLOR_BG_WINDOW)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        content_frame.columnconfigure(0, weight=1)  # 左侧自适应
        content_frame.columnconfigure(1, weight=1)  # 右侧也自适应
        content_frame.rowconfigure(0, weight=1)

        # 左侧：PDF列表
        list_frame = tk.Frame(content_frame, bg=COLOR_BG_WINDOW, padx=20, pady=16)
        list_frame.grid(row=0, column=0, sticky=(tk.N, tk.S), padx=(0, 10))

        # 区域标题
        list_title = tk.Label(
            list_frame,
            text="已导入文件列表",
            font=("微软雅黑", 12, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_BG_WINDOW
        )
        list_title.pack(anchor=tk.W, pady=(0, 10))

        # 创建Treeview
        columns = ('id', 'file_name', 'create_time', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        # 设置列
        self.tree.heading('id', text='ID', anchor=tk.W)
        self.tree.heading('file_name', text='文件名', anchor=tk.W)
        self.tree.heading('create_time', text='导入时间', anchor=tk.CENTER)
        self.tree.heading('status', text='状态', anchor=tk.CENTER)

        self.tree.column('id', width=50, anchor=tk.CENTER)
        self.tree.column('file_name', width=250, anchor=tk.W)
        self.tree.column('create_time', width=150, anchor=tk.CENTER)
        self.tree.column('status', width=80, anchor=tk.CENTER)

        # 滚动条
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # 布局
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview样式
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Treeview',
                      font=("微软雅黑", 10),
                      rowheight=28,
                      background=COLOR_BG_CARD,
                      foreground=COLOR_TEXT_PRIMARY,
                      fieldbackground=COLOR_BG_CARD)

        style.configure('Treeview.Heading',
                      font=("微软雅黑", 11, "bold"),
                      background=COLOR_BG_CARD,
                      foreground=COLOR_TEXT_SECONDARY,
                      padding=(5, 5))

        style.map('Treeview',
                  background=[('selected', COLOR_PRIMARY)],
                  foreground=[('selected', 'white')])

        # 绑定选择事件
        self.tree.bind('<<TreeviewSelect>>', self.on_record_select)

        # ========== 右键菜单 ==========
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="打开文件", command=self.open_selected_file, accelerator="Ctrl+O")
        self.context_menu.add_command(label="生成摘要", command=self.batch_generate_summary, accelerator="Ctrl+G")
        self.context_menu.add_command(label="重新生成摘要", command=self.regenerate_summary)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="复制文件路径", command=self.copy_file_path)
        self.context_menu.add_command(label="复制摘要", command=self.copy_summary)
        self.context_menu.add_command(label="编辑标签", command=self.edit_tags)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="删除记录", command=self.delete_selected_file, accelerator="Delete", fg=COLOR_ERROR)

        # 绑定右键菜单
        self.tree.bind('<Button-3>', self.show_context_menu)

        # 右侧：摘要详情区
        summary_frame = tk.Frame(content_frame, bg=COLOR_BG_WINDOW, padx=20, pady=16)
        summary_frame.grid(row=0, column=1, sticky=(tk.N, tk.S))  # 只垂直拉伸，水平固定
        content_frame.columnconfigure(1, minsize=500)  # 设置右侧面板最小宽度

        # 卡片式设计
        card_frame = tk.Frame(summary_frame, bg=COLOR_BG_CARD, relief="flat", bd=0)
        card_frame.pack(fill=tk.BOTH, expand=False)
        card_frame.config(highlightbackground=COLOR_BORDER, highlightthickness=1, highlightcolor=COLOR_BORDER)

        # 卡片内边距
        card_inner = tk.Frame(card_frame, bg=COLOR_BG_CARD, padx=20, pady=20)
        card_inner.pack(fill=tk.BOTH, expand=False)

        # 文件名标题
        self.file_name_label = tk.Label(
            card_inner,
            text="",
            font=("微软雅黑", 14, "bold"),
            fg=COLOR_TEXT_PRIMARY,
            bg=COLOR_BG_CARD,
            anchor=tk.W,
            wraplength=500  # 标题换行宽度
        )
        self.file_name_label.pack(fill=tk.X, pady=(0, 16))

        # 摘要内容
        self.summary_text = scrolledtext.ScrolledText(
            card_inner,
            font=("微软雅黑", 10),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=COLOR_BG_CARD,
            fg=COLOR_TEXT_PRIMARY,
            relief="flat",
            bd=0
        )
        self.summary_text.pack(fill=tk.BOTH, expand=False)

        # ========== 底部状态栏 ==========
        status_bar = tk.Frame(main_frame, bg=COLOR_BG_CARD, height=40)
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(16, 0))
        status_bar.grid_propagate(False)
        status_bar.columnconfigure(0, weight=1)
        status_bar.columnconfigure(1, weight=0)

        # 底部边框
        status_bar.config(highlightbackground=COLOR_BORDER, highlightthickness=1)

        # 左侧统计信息
        self.stats_label = tk.Label(
            status_bar,
            text="当前共 0 个文件 | 检索到 0 条结果",
            font=("微软雅黑", 9),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_CARD
        )
        self.stats_label.pack(side=tk.LEFT, padx=20, pady=8)

        # 右侧状态提示
        self.status_label = tk.Label(
            status_bar,
            text="就绪",
            font=("微软雅黑", 9),
            fg=COLOR_TEXT_SECONDARY,
            bg=COLOR_BG_CARD
        )
        self.status_label.pack(side=tk.RIGHT, padx=20, pady=8)

        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=200)
        self.progress.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))

        # ========== 键盘快捷键绑定 ==========
        self.root.bind('<Control-n>', lambda e: self.select_pdf_files())
        self.root.bind('<Control-g>', lambda e: self.batch_generate_summary())
        self.root.bind('<Control-o>', lambda e: self.open_selected_file())
        self.root.bind('<Control-d>', lambda e: self.delete_selected_file())
        self.root.bind('<Control-f>', lambda e: self.search_entry.focus_set())
        self.root.bind('<Delete>', lambda e: self.delete_selected_file())
        self.root.bind('<F5>', lambda e: self.load_records())
        self.root.bind('<F1>', lambda e: self.show_shortcut_hints())
        self.root.bind('<Escape>', lambda e: self.tree.selection_remove(self.tree.selection()) if self.tree.selection() else None)

    def on_search_focus_in(self, e):
        """搜索框聚焦时清空placeholder"""
        if self.search_entry.get() == "输入关键词检索":
            self.search_entry.delete(0, tk.END)
            self.search_entry.config(fg=COLOR_TEXT_PRIMARY)

    def on_search_focus_out(self, e):
        """搜索框失焦时显示placeholder"""
        if not self.search_entry.get().strip():
            self.search_entry.insert(0, "输入关键词检索")
            self.search_entry.config(fg=COLOR_TEXT_TERTIARY)

    def on_tag_filter_changed(self, event):
        """标签筛选变化时刷新列表"""
        selected_tag = self.tag_filter_var.get()
        if selected_tag == "全部标签":
            self.load_records()
        else:
            records = get_records_by_tags([selected_tag])
            self.load_records(records)
        self.status_label.config(text=f"标签筛选: {selected_tag}", fg=COLOR_TEXT_SECONDARY)

    def refresh_tag_filter(self):
        """刷新标签筛选下拉框"""
        all_tags = get_all_tags()
        if all_tags:
            self.tag_filter['values'] = ["全部标签"] + all_tags
        else:
            self.tag_filter['values'] = ["全部标签"]

    def load_records(self, records=None):
        """加载记录到列表"""
        # 清空列表
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 加载记录
        if records is None:
            records = get_all_records()

        for record in records:
            # 获取状态
            status = "未生成"

            if record.get('summary') and record['summary'].strip():
                status = "已生成"
            elif record.get('content') and record['content'].strip():
                status = "生成中"

            self.tree.insert('', tk.END, values=(
                record['id'],
                record['file_name'],
                record['create_time'],
                status
            ))

        # 更新状态栏
        self.stats_label.config(text=f"当前共 {len(records)} 个文件 | 检索到 {len(records)} 条结果")

        # 刷新标签筛选下拉框
        self.refresh_tag_filter()

    def select_pdf_files(self):
        """选择文档文件（支持PDF、TXT、Word、Excel等）"""
        files = filedialog.askopenfilenames(
            title="选择文档文件",
            filetypes=[
                ("所有支持的文档", "*.pdf;*.txt;*.doc;*.docx;*.xls;*.xlsx"),
                ("PDF文件", "*.pdf"),
                ("TXT文件", "*.txt"),
                ("Word文件", "*.doc;*.docx"),
                ("Excel文件", "*.xls;*.xlsx"),
                ("所有文件", "*.*")
            ],
            initialdir=os.path.expanduser("~/Desktop")
        )

        if not files:
            return

        self.set_status("正在读取文件...", loading=True)
        self.select_btn.config(state=tk.DISABLED)
        self.generate_btn.config(state=tk.DISABLED)

        # 在后台线程中处理
        thread = threading.Thread(target=self._process_document_files, args=(files,))
        thread.daemon = True
        thread.start()

    def _process_document_files(self, files):
        """处理文档文件（后台线程）"""
        success_count = 0
        fail_count = 0
        total = len(files)

        for idx, file_path in enumerate(files, 1):
            try:
                file_name = os.path.basename(file_path)
                # 更新总体进度
                self.root.after(0, lambda i=idx, t=total, f=file_name:
                    self.set_status(f"[{i}/{t}] 正在处理: {f}", loading=True))

                # 验证文档
                is_valid, error_msg, file_type = validate_document(file_path)
                if not is_valid:
                    print(f"跳过: {file_name} - {error_msg}")
                    fail_count += 1
                    continue

                # 定义页面进度回调
                def page_progress(page_num, total_pages, current_len, max_len):
                    progress_pct = min(100, int((page_num / total_pages) * 100))
                    length_pct = min(100, int((current_len / max_len) * 100))
                    self.root.after(0, lambda i=idx, t=total, f=file_name, p=page_num, tp=total_pages, pp=progress_pct, lp=length_pct:
                        self.set_status(f"[{i}/{t}] {f} - 页面 {p}/{tp} ({pp}%) - 文本 {lp}%", loading=True))

                # 提取文本
                text, extracted_type = extract_text_from_document(file_path, None)

                # 添加到数据库（同时保存全文内容）
                success = add_record(file_name, file_path)
                if success:
                    # 获取刚添加的记录ID并更新内容
                    records = get_all_records()
                    if records:
                        last_record = records[0]
                        update_content(last_record['id'], text)
                    success_count += 1
                else:
                    fail_count += 1

            except Exception as e:
                print(f"处理失败: {os.path.basename(file_path)} - {e}")
                fail_count += 1

        # 在主线程中更新UI
        self.root.after(0, lambda: self._after_process_files(success_count, fail_count))

    def _after_process_files(self, success_count, fail_count):
        """处理完成后更新UI"""
        self.set_status("就绪", loading=False)
        self.load_records()
        self.refresh_tag_filter()
        self.select_btn.config(state=tk.NORMAL)
        self.generate_btn.config(state=tk.NORMAL)

        if fail_count == 0:
            messagebox.showinfo("导入完成", f"成功导入 {success_count} 个PDF文件")
        else:
            messagebox.showwarning("导入完成", f"成功: {success_count} 个, 失败: {fail_count} 个")

    def batch_generate_summary(self):
        """批量生成摘要"""
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("提示", "请先选择要生成摘要的PDF记录")
            return

        self.set_status("正在生成摘要...", loading=True)
        self.generate_btn.config(state=tk.DISABLED)

        # 在后台线程中处理
        thread = threading.Thread(target=self._generate_summaries, args=(selected_items,))
        thread.daemon = True
        thread.start()

    def _generate_summaries(self, selected_items):
        """生成摘要（后台线程）"""
        success_count = 0
        fail_count = 0
        skip_count = 0
        total = len(selected_items)

        for idx, item in enumerate(selected_items, 1):
            try:
                record_id = self.tree.item(item)['values'][0]
                record = get_record_by_id(record_id)

                if not record:
                    fail_count += 1
                    print(f"记录不存在: ID={record_id}")
                    continue

                file_name = record['file_name']

                # 如果已有摘要，跳过
                if record.get('summary') and record['summary'].strip():
                    self.root.after(0, lambda i=idx, t=total, f=file_name:
                        self.set_status(f"[{i}/{t}] 跳过 {f} (已有摘要)", loading=False))
                    skip_count += 1
                    continue

                # 更新进度
                self.root.after(0, lambda i=idx, t=total, f=file_name:
                    self.set_status(f"[{i}/{t}] 正在提取文本: {f}", loading=True))

                # 提取文本
                text, file_type = extract_text_from_document(record['file_path'], None)

                # 生成摘要
                self.root.after(0, lambda i=idx, t=total, f=file_name:
                    self.set_status(f"[{i}/{t}] 正在生成摘要: {f}", loading=True))

                result = generate_summary(text)

                if result['success']:
                    # 更新数据库
                    if update_summary(record_id, result['summary']):
                        success_count += 1
                        print(f"摘要生成成功: {file_name}")
                    else:
                        fail_count += 1
                        print(f"数据库更新失败: {file_name}")
                else:
                    fail_count += 1
                    print(f"摘要生成失败: {file_name} - 错误: {result['error']}")

            except Exception as e:
                fail_count += 1
                print(f"生成摘要异常: {file_name} - 错误: {str(e)}")

        # 在主线程中更新UI
        self.root.after(0, lambda: self._after_generate_summaries(success_count, fail_count, skip_count))

    def _after_generate_summaries(self, success_count, fail_count, skip_count):
        """生成摘要完成后更新UI"""
        self.set_status("就绪", loading=False)
        self.load_records()
        self.generate_btn.config(state=tk.NORMAL)

        message = f"成功: {success_count} 个"
        if skip_count > 0:
            message += f", 跳过(已有摘要): {skip_count} 个"
        if fail_count > 0:
            message += f", 失败: {fail_count} 个"

        if fail_count == 0:
            messagebox.showinfo("生成完成", message)
        else:
            messagebox.showwarning("生成完成", message)

    def search_records(self):
        """搜索记录（支持关键词搜索）"""
        keyword = self.search_entry.get().strip()

        if not keyword or keyword == "输入关键词检索":
            self.load_records()
            return

        # 关键词搜索（搜索文件名和摘要）
        records = search_by_title(keyword)
        self.load_records(records)
        self.status_label.config(text=f"关键词「{keyword}」找到 {len(records)} 条记录", fg=COLOR_TEXT_SECONDARY)

    def on_record_select(self, event):
        """记录选择事件"""
        selected_items = self.tree.selection()

        if not selected_items:
            return

        item = selected_items[0]
        record_id = self.tree.item(item)['values'][0]
        record = get_record_by_id(record_id)

        if record:
            # 更新文件名标题
            self.file_name_label.config(text=record['file_name'])

            # 显示摘要
            summary = record.get('summary', '暂无摘要')
            self.display_summary(summary)
        else:
            self.display_summary("无法加载记录信息")

    def display_summary(self, text):
        """显示摘要"""
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)

        if text and text.strip():
            try:
                # 解析摘要并格式化显示
                summary_dict = parse_summary_to_dict(text)
                formatted_text = self.format_summary(summary_dict)
                self.summary_text.insert(tk.END, formatted_text)
            except Exception as e:
                print(f"摘要解析失败: {e}")
                self.summary_text.insert(tk.END, "摘要解析失败，请重新生成\n\n原始内容:\n\n" + text)
        else:
            self.summary_text.insert(tk.END, "暂无摘要\n\n请点击【生成结构化摘要】按钮为选中的PDF生成AI摘要。")

        self.summary_text.config(state=tk.DISABLED)

    def format_summary(self, summary_dict):
        """格式化摘要显示"""
        formatted = ""

        # 核心主题
        if summary_dict.get('核心主题'):
            formatted += f"📌 核心主题\n{summary_dict['核心主题']}\n\n"

        # 关键数据
        if summary_dict.get('关键数据'):
            formatted += f"📊 关键数据\n{summary_dict['关键数据']}\n\n"

        # 适用场景
        if summary_dict.get('适用场景'):
            formatted += f"📍 适用场景\n{summary_dict['适用场景']}\n\n"

        # 核心结论
        if summary_dict.get('核心结论'):
            formatted += f"💡 核心结论\n{summary_dict['核心结论']}\n\n"

        # 其他内容
        for key, value in summary_dict.items():
            if key not in ['核心主题', '关键数据', '适用场景', '核心结论']:
                formatted += f"📝 {key}\n{value}\n\n"

        return formatted

    def open_selected_file(self):
        """打开选中的PDF文件"""
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("提示", "请先选择要打开的PDF记录")
            return

        item = selected_items[0]
        record_id = self.tree.item(item)['values'][0]
        record = get_record_by_id(record_id)

        if not record:
            messagebox.showerror("错误", "无法找到记录信息")
            return

        file_path = record['file_path']

        # 检查文件是否存在
        if not os.path.exists(file_path):
            messagebox.showerror("错误", f"文件不存在:\n{file_path}")
            return

        try:
            # 优先使用系统默认程序打开文件
            if os.name == 'nt':  # Windows
                # 直接用 startfile，速度最快
                os.startfile(file_path)
            elif os.name == 'posix':  # Linux/Mac
                subprocess.call(['xdg-open', file_path])
            else:
                messagebox.showerror("错误", "不支持的操作系统")

            self.status_label.config(text=f"已打开: {record['file_name']}", fg=COLOR_SUCCESS)

        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件:\n{e}")
            self.status_label.config(text=f"打开失败: {record['file_name']}", fg=COLOR_ERROR)

    def delete_selected_file(self):
        """删除选中的文件记录"""
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("提示", "请先选择要删除的文件记录")
            return

        item = selected_items[0]
        record_id = self.tree.item(item)['values'][0]
        record = get_record_by_id(record_id)

        if not record:
            messagebox.showerror("错误", "无法找到记录信息")
            return

        # 确认删除
        result = messagebox.askyesno(
            "确认删除",
            f"确定要删除文件 '{record['file_name']}' 吗？\n\n注意：只会删除数据库中的记录，不会删除实际文件。",
            icon='warning'
        )

        if not result:
            return

        # 执行删除
        if delete_record(record_id):
            # 重排ID使保持连续
            reset_record_ids()
            self.set_status(f"已删除: {record['file_name']}", loading=False)
            self.load_records()
            # 清空摘要显示
            self.file_name_label.config(text="")
            self.display_summary("")
            messagebox.showinfo("删除成功", f"文件 '{record['file_name']}' 已从列表中移除")
        else:
            messagebox.showerror("删除失败", "无法删除记录，请重试")

    def set_status(self, message, loading=False):
        """设置状态栏"""
        if loading:
            self.progress.start()
        else:
            self.progress.stop()
        self.status_label.config(text=message)

    def show_about(self):
        """显示关于信息"""
        about_text = """
PDF AI 智能摘要工具 v2.0

功能特性：
• 支持PDF、Word、Excel、TXT等多种文档格式
• AI智能生成结构化摘要
• 标签分类管理
• 全文检索功能
• 批量重命名（按摘要主题）
• 导出Excel/Word格式
• 暗黑/明亮主题切换

技术栈：
• GUI框架: tkinter
• AI服务: 智谱AI (GLM-4)
• 文档处理: PyPDF2, python-docx, openpyxl
• 数据库: SQLite3

开发者: 海盐荔枝
"""

        messagebox.showinfo("关于", about_text)


def main():
    """主函数"""
    if HAS_TKINTERDND2:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = PDFAITool(root)

    # 设置窗口图标（可选）
    # root.iconbitmap('icon.ico')

    root.mainloop()


if __name__ == '__main__':
    main()