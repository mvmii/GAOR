import tkinter as tk


class VerifyWindow:
    def __init__(self, root, decrypt_key):
        self.root = root
        self.input_key = decrypt_key
        self.popup = tk.Toplevel(self.root)
        self.window_w = 320
        self.window_h = 150
        # 創建一個新的彈出窗口，作為主窗口的子窗口。Top-level :“頂層的”或“最上層的”
        self.popup.title("Verification")
        self.popup.transient(self.root)  # 设置popup为模态窗口，使得主窗口在popup开启时不可交互
        self.popup.grab_set()  # 限制用户只能和popup交互
        self.popup.protocol("WM_DELETE_WINDOW", self.on_popup_close)  # 设置当popup被关闭时执行的操作
        self.popup.resizable(False, False)  # 禁止視窗變動大小

        # 使用 frame 来容纳所有的小部件
        frame = tk.Frame(self.popup)
        frame.pack(expand=True, anchor=tk.CENTER)

        # 在彈出窗口中添加一個標籤和輸入框，用於輸入驗證碼
        tk.Label(frame, text="請輸入購買金鑰: ").pack()

        # 在彈出窗口中添加一個標籤和輸入框，用於輸入驗證碼
        self.error_tip = tk.Label(frame, text="")
        self.error_tip.pack()

        self.entry = tk.Entry(frame, width=40)
        self.entry.pack()

        tk.Label(frame, text="").pack()

        ok_button = tk.Button(frame, text="Enter", command=self.on_ok)
        ok_button.pack()

        # 设置 verify_window 在主窗口中心显示
        self.set_position()

    def set_position(self):
        # 获取主窗口尺寸和位置
        self.root.update_idletasks()
        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        root_height = self.root.winfo_height()

        # 计算 verify_window 的位置
        x = root_x + (root_width - self.window_w) // 2
        y = root_y + (root_height - self.window_h) // 2
        self.popup.geometry(f'{self.window_w}x{self.window_h}+{x}+{y}')

    def on_ok(self):
        if self.entry.get() == self.input_key:
            self.popup.destroy()
        else:
            self.error_tip.pack()
            self.error_tip.config(text="輸入錯誤")
            print("input key is error")

    def on_popup_close(self):
        self.root.destroy()  # 当verify_window关闭时，也关闭主窗口




