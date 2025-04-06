import tkinter as tk
from tkinter import ttk, messagebox
import random
from tkinterdnd2 import TkinterDnD, DND_FILES

class RandomPickerApp:
    def __init__(self, root):
        self.root = root
        self.names = []
        self.selected_num = 1
        self.running = False
        self.current_selection = []
        
        # 界面布局
        self.create_widgets()
        self.setup_drag_drop()

    def create_widgets(self):
        """创建所有界面组件"""
        # 文件拖放区域
        self.frame_drop = ttk.LabelFrame(self.root, text="拖放名字文件到这里（.txt）")
        self.frame_drop.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 控制面板
        control_frame = ttk.Frame(self.root)
        control_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # 人数选择
        ttk.Label(control_frame, text="选择人数:").pack(side=tk.LEFT)
        self.spin_num = ttk.Spinbox(control_frame, from_=1, to=1, width=5)
        self.spin_num.pack(side=tk.LEFT, padx=5)
        self.spin_num.set(1)

        # 按钮
        self.btn_start = ttk.Button(control_frame, text="开始", command=self.start)
        self.btn_start.pack(side=tk.LEFT, padx=5)
        self.btn_stop = ttk.Button(control_frame, text="停止", 
                                 command=self.stop, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        # 结果显示区域
        self.result_frame = ttk.LabelFrame(self.root, text="当前选择")
        self.result_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.result_text = tk.StringVar()
        self.lbl_result = ttk.Label(self.result_frame, 
                                  textvariable=self.result_text,
                                  font=('Arial', 14),
                                  wraplength=380)
        self.lbl_result.pack(expand=True)

    def setup_drag_drop(self):
        """设置文件拖放功能"""
        self.drop_label = ttk.Label(self.frame_drop, text="将文件拖放到此区域")
        self.drop_label.pack(expand=True)
        self.frame_drop.drop_target_register(DND_FILES)
        self.frame_drop.dnd_bind('<<Drop>>', self.process_dropped_file)

    def process_dropped_file(self, event):
        """处理拖放文件事件"""
        file_path = event.data.strip('{}')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.names = [line.strip() for line in f if line.strip()]
                
            if not self.names:
                messagebox.showerror("错误", "文件为空或格式不正确")
                return
                
            self.drop_label.config(text=f"已加载文件：{file_path}")
            max_num = len(self.names)
            self.spin_num.config(to=max_num)
            self.spin_num.set(1 if max_num >=1 else 0)
            
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败：{str(e)}")

    def start(self):
        """启动随机选择"""
        if not self.names:
            messagebox.showwarning("警告", "请先拖放包含名字的文件")
            return
            
        try:
            self.selected_num = int(self.spin_num.get())
            if not 1 <= self.selected_num <= len(self.names):
                raise ValueError
        except:
            messagebox.showerror("错误", "请输入有效的选择人数")
            return

        self.running = True
        self.btn_start.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.animate_selection()

    def stop(self):
        """停止选择"""
        self.running = False
        self.btn_start.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)
        self.lbl_result.config(foreground='black')  # 恢复默认颜色

    def animate_selection(self):
        """执行随机选择动画"""
        if self.running:
            self.current_selection = random.sample(self.names, self.selected_num)
            self.result_text.set("\n".join(self.current_selection))
            
            # 颜色闪烁效果
            current_color = 'red' if self.lbl_result.cget('foreground') == 'black' else 'black'
            self.lbl_result.config(foreground=current_color)
            
            # 调整速度（100-200毫秒）
            self.root.after(10, self.animate_selection)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("随机点名程序 v1.0")
    root.geometry("500x400")
    
    # 设置窗口图标（可选）
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    app = RandomPickerApp(root)
    root.mainloop()