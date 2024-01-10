# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install requests  (庫)
#            pip install beautifulsoup4 (來解析 HTML，並找到相應的元素)
#             pip install pyinstaller (將py轉exe)
#             pyinstaller --onefile main.py  (產exe)
#             pip install selenium  (以訪客身分開啟 Edge 並加載當前網址)

# 簡單說明 GUI類型  目前先使用【Tkinter】來實作

import os
import tkinter as tk
from tkinter import Entry, Label, Button, StringVar, OptionMenu, Text, Scrollbar
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import threading
import re
import time
import webbrowser
from datetime import datetime

store_url = "https://www.goopi.co/categories/goopimade-goopi-%E5%AD%A4%E5%83%BB?sort_by=created_at&order_by=desc"
login_url = "https://www.goopi.co/users/sign_in"


class MainApplication:  # 模組化
    def __init__(self, master):
        # 設置變數
        # UI的row
        self.current_row = 1
        # 初始化 新增輸入關鍵字欄位 的次數
        self.add_ky_count = 0
        self.blank_px = 18
        self.px = 5
        self.py = 2
        # [檢查加入購物車]次數
        self.check_add_cart_count = 0
        # [檢查加入購物車]總次數
        self.check_add_cart_num = 5
        self.tip = ("使用此系統注意事項 : \n"
                    "1.請先註冊會員(勿用FB連動)\n"
                    "2.到會員資料先行綁定銀行卡與地址\n"
                    "務必勾選[同意記住信用卡資訊及<信用卡交易協議>，以便下次快速付款]\n"
                    "3.綁定手機碼跟地址\n"
                    "4.確認7-11店號(6位數)\n"
                    "5.[開始下單]前，請先點擊[登入]，並在右邊訊息中確認已顯示登入成功\n"
                    "6.[開始下單]前，也請先確認購物車是空的，否則會一起下單或是影響下單流程導致失敗\n"
                    "7.登入太頻繁，會登入失敗，請等待10分鐘後再登入。\n"
                    "8.付款方式皆為預設 : 7-11取貨不付款，線上刷卡")
        self.is_login = False
        self.open_browser_mode = tk.BooleanVar(value=False)  # 默认为非无头模式
        self.open_browser_status = False
        # 配置無頭模式
        edge_options = Options()
        edge_options.add_argument("--headless")  # 啟用無頭模式
        edge_options.add_argument("--disable-gpu")  # 在無頭模式下，禁用 GPU 加速有時是必要的
        self.driver = webdriver.Edge(options=edge_options)

        # 設置視窗
        self.master = master
        self.master.title("Goopi自動下單")
        # 寬度和高度
        self.master.geometry("920x550")
        # 禁止水平和垂直的視窗大小調整
        self.master.resizable(False, False)

        # 创建一个PanedWindow小部件作为主要容器
        self.master.paned_window = tk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.master.paned_window.pack(fill=tk.BOTH, expand=True)

        # 左边的框架，用于放置标签和输入框
        self.master.left_frame = tk.Frame(self.master.paned_window)
        self.master.paned_window.add(self.master.left_frame)

        # 右边的框架，用于放置操作消息文本框
        self.master.right_frame = tk.Frame(self.master.paned_window)
        self.master.paned_window.add(self.master.right_frame)

        self.n1_label = Label(self.master.left_frame, text=self.tip)
        self.n1_label.grid(row=self.current_row, column=0, sticky="we", padx=self.blank_px, pady=self.py, columnspan=8)
        self.current_row += 1

        # 輸入帳號 Str
        self.acc_label = Label(self.master.left_frame, text="帳號：")
        self.acc_label.grid(row=self.current_row, column=0, sticky="w", padx=self.px, pady=self.py)
        # 輸入帳號 input
        self.acc_entry = Entry(self.master.left_frame, width=30)
        self.acc_entry.grid(row=self.current_row, column=1, sticky="we", padx=self.px, pady=self.py, columnspan=5)
        self.acc_entry.insert(0, "love_8462564@yahoo.com.tw")
        self.current_row += 1

        # 輸入密碼 Str
        self.sec_label = Label(self.master.left_frame, text="密碼：")
        self.sec_label.grid(row=self.current_row, column=0, sticky="w", padx=self.px, pady=self.py)
        # 輸入密碼 input
        self.sec_entry = Entry(self.master.left_frame, width=30, show="*")
        self.sec_entry.grid(row=self.current_row, column=1, sticky="we", padx=self.px, pady=self.py, columnspan=5)
        self.sec_entry.insert(0, "mvmii1234")
        self.current_row += 1

        # 711-店號
        self.se_label = Label(self.master.left_frame, text="7-11 店號(6位數)，點擊我可查詢 : ", fg="blue",
                              cursor="hand2")
        self.se_label.grid(row=self.current_row, column=0, sticky="w", padx=self.px, pady=self.py, columnspan=4)
        self.se_label.bind("<Button-1>", lambda e: self.open_711_link("https://emap.pcsc.com.tw/"))
        # 711-店號 input
        self.se_entry = Entry(self.master.left_frame, width=15)
        self.se_entry.grid(row=self.current_row, column=4, sticky="we", padx=self.px, pady=self.py, columnspan=2)
        self.se_entry.insert(0, "239444")
        self.current_row += 1

        # 建立 [檢查購物車迴圈次數] 驗證器
        validate_command = root.register(self.validate_input), '%P'
        # 檢查購物車迴圈次數 Str
        self.check_add_cart_count_label = Label(self.master.left_frame, text="檢查購物車迴圈次數:")
        self.check_add_cart_count_label.grid(row=self.current_row, column=0, sticky="w", padx=self.px, pady=self.py,
                                             columnspan=2)
        # 輸入檢查購物車迴圈次數 input
        self.check_add_cart_count_entry = Entry(self.master.left_frame, validate='key',
                                                validatecommand=validate_command, width=10)
        self.check_add_cart_count_entry.grid(row=self.current_row, column=2, sticky="we", padx=self.px, pady=self.py,
                                             columnspan=2)
        self.check_add_cart_count_entry.insert(0, "100")
        # 檢查購物車迴圈次數 Str
        self.check_add_cart_count_tip_label = Label(self.master.left_frame, text="(輸入數字且最多三位數)")
        self.check_add_cart_count_tip_label.grid(row=self.current_row, column=4, sticky="w", padx=self.px, pady=self.py,
                                                 columnspan=2)
        self.current_row += 1

        # 是否開啟瀏覽器
        self.open_browser_checkbutton = tk.Checkbutton(self.master.left_frame, text="開啟Edge瀏覽器(不開啟RUN比較快唷)",
                                                       variable=self.open_browser_mode)
        self.open_browser_checkbutton.grid(row=self.current_row, column=0, sticky="w", padx=self.px, pady=self.py,
                                           columnspan=5)
        self.current_row += 1

        # 登入
        self.login_button = Button(self.master.left_frame, text="登入", command=self.url_login)
        self.login_button.grid(row=self.current_row, column=0, sticky="we", padx=self.px, pady=self.py)
        # 清除購物車
        self.clear_cart_button = Button(self.master.left_frame, text="清除購物車", command=self.clear_cart)
        self.clear_cart_button.grid(row=self.current_row, column=1, sticky="we", padx=self.px, pady=self.py,
                                    columnspan=3)
        # 開始下單
        self.start_button = Button(self.master.left_frame, text="開始下單", command=self.url_start)
        self.start_button.grid(row=self.current_row, column=4, sticky="we", padx=self.px, pady=self.py)
        # 清除右邊訊息
        self.clear_msg_button = Button(self.master.left_frame, text="清空右邊訊息", command=self.clear_message)
        self.clear_msg_button.grid(row=self.current_row, column=5, sticky="we", padx=self.px, pady=self.py,
                                   columnspan=1)
        self.current_row += 1

        self.input_ky_label = Label(self.master.left_frame, text="輸入要買的新品關鍵字(含顏色)")
        self.input_ky_label.grid(row=self.current_row, column=0, sticky="we", padx=self.px, pady=self.py, columnspan=6)
        self.input_size_label = Label(self.master.left_frame, text="尺寸")
        self.input_size_label.grid(row=self.current_row, column=6, sticky="we", padx=self.px, pady=self.py)
        self.current_row += 1

        # 欄位1
        self.ky1_entry = Entry(self.master.left_frame)
        self.ky1_entry.grid(row=self.current_row, column=0, padx=self.px, pady=self.py, columnspan=6, sticky="we")
        self.ky1_entry.insert(0, "Mid-H  Smock - L-Gray")
        self.size1_var = StringVar(self.master.left_frame)
        self.size1_var.set("無")
        self.size1_dropdown = OptionMenu(self.master.left_frame, self.size1_var, "1號", "2號", "3號", "無")
        self.size1_dropdown.grid(row=self.current_row, column=6, padx=self.px, pady=self.py, sticky="w")
        self.current_row += 1

        # 欄位2
        self.ky2_entry = Entry(self.master.left_frame)
        self.ky2_entry.grid(row=self.current_row, column=0, padx=self.px, pady=self.py, columnspan=6, sticky="we")
        self.ky2_entry.insert(0, "Mid-H  Smock - Black")
        self.size2_var = StringVar(self.master.left_frame)
        self.size2_var.set("無")
        self.size2_dropdown = OptionMenu(self.master.left_frame, self.size2_var, "1號", "2號", "3號", "無")
        self.size2_dropdown.grid(row=self.current_row, column=6, padx=self.px, pady=self.py, sticky="w")
        self.current_row += 1

        # 欄位3
        self.ky3_entry = Entry(self.master.left_frame)
        self.ky3_entry.grid(row=self.current_row, column=0, padx=self.px, pady=self.py, columnspan=6, sticky="we")
        self.size3_var = StringVar(self.master.left_frame)
        self.size3_var.set("無")
        self.size3_dropdown = OptionMenu(self.master.left_frame, self.size3_var, "1號", "2號", "3號", "無")
        self.size3_dropdown.grid(row=self.current_row, column=6, padx=self.px, pady=self.py, sticky="w")
        self.current_row += 1

        # 欄位4
        self.ky4_entry = Entry(self.master.left_frame)
        self.ky4_entry.grid(row=self.current_row, column=0, padx=self.px, pady=self.py, columnspan=6, sticky="we")
        self.size4_var = StringVar(self.master.left_frame)
        self.size4_var.set("無")
        self.size4_dropdown = OptionMenu(self.master.left_frame, self.size4_var, "1號", "2號", "3號", "無")
        self.size4_dropdown.grid(row=self.current_row, column=6, padx=self.px, pady=self.py, sticky="w")
        self.current_row += 1

        # 欄位5
        self.ky5_entry = Entry(self.master.left_frame)
        self.ky5_entry.grid(row=self.current_row, column=0, padx=self.px, pady=self.py, columnspan=6, sticky="we")
        self.size5_var = StringVar(self.master.left_frame)
        self.size5_var.set("無")
        self.size5_dropdown = OptionMenu(self.master.left_frame, self.size5_var, "1號", "2號", "3號", "無")
        self.size5_dropdown.grid(row=self.current_row, column=6, padx=self.px, pady=self.py, sticky="w")
        self.current_row += 1

        # scrollbar
        self.scrollbar = Scrollbar(self.master.right_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text
        self.msg_text = Text(self.master.right_frame, yscrollcommand=self.scrollbar.set)
        self.msg_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.msg_text.config(state=tk.DISABLED)  # 默认不可编辑
        self.scrollbar.config(command=self.msg_text.yview)

    def validate_input(self, P):
        """
        验证输入是否为最多三位的数字。
        :param P: 输入框中的文本。
        :return: 布尔值，表示输入是否有效。
        """
        # 检查输入是否只包含数字，并且长度不超过3
        if P.isdigit() and len(P) <= 3:
            return True
        elif P == "":
            return True  # 允许空字符串，以便清除输入
        else:
            return False

    def toggle_open_browser_mode(self):
        new_open_browser_status = self.open_browser_mode.get()
        if self.open_browser_status == new_open_browser_status:
            return
        self.is_login = False
        self.open_browser_status = new_open_browser_status
        self.driver.quit()
        if self.open_browser_mode.get():
            # 使用Selenium開啟Edge瀏覽器
            self.driver = webdriver.Edge()  # 請確保已下載並設定好Edge WebDriver的路徑
        else:
            # 配置無頭模式
            edge_options = Options()
            edge_options.add_argument("--headless")  # 啟用無頭模式
            edge_options.add_argument("--disable-gpu")  # 在無頭模式下，禁用 GPU 加速有時是必要的
            edge_options.add_argument("window-size=1920,1080")  # 设置窗口大小
            # 使用Selenium開啟Edge瀏覽器
            self.driver = webdriver.Edge(options=edge_options)  # 確保已下載並設定好Edge WebDriver的路徑

    @staticmethod
    def open_711_link(url):
        webbrowser.open_new(url)

    def toggle_ui_elements(self, state=tk.DISABLED):
        """ 切換UI元件的可用性 """
        elements = [self.acc_entry, self.sec_entry, self.se_entry,
                    self.start_button, self.login_button, self.clear_msg_button, self.clear_cart_button,
                    self.check_add_cart_count_entry,
                    self.open_browser_checkbutton,
                    self.ky1_entry, self.ky2_entry, self.ky3_entry, self.ky4_entry, self.ky5_entry,
                    self.size1_dropdown, self.size2_dropdown, self.size3_dropdown,
                    self.size4_dropdown, self.size5_dropdown]
        for element in elements:
            element.config(state=state)

    def check_input(self, is_start=True):
        if not self.acc_entry.get().strip():
            self.show_log("請輸入帳號")
            return False
        if not self.sec_entry.get().strip():
            self.show_log("請輸入密碼")
            return False
        if is_start:
            se_entry_value = self.se_entry.get().strip()
            if not se_entry_value:
                self.show_log("請輸入7-11店號")
                return False
            elif not se_entry_value.isdigit() or len(se_entry_value) != 6:
                self.show_log("7-11 店號必須是6位數字")
                return False
            buy_list = self.get_product_ky()
            if not buy_list:  # 列表是空的
                self.url_end("請輸入要買的產品關鍵字")
                return False
        return True  # 檢查輸入欄位皆有輸入

    def clear_cart(self):
        # 購物車不用檢查是否登入狀態 + 不用檢查欄位是否有無正確輸入。
        self.toggle_ui_elements()
        self.toggle_open_browser_mode()  # 切換是否開啟瀏覽器狀態
        threading.Thread(target=self.find_and_clear_cart, daemon=True).start()

    def find_and_clear_cart(self):
        self.show_log(f"檢查購物車中... isLogin:{self.is_login}")
        try:
            # 加載URL
            self.driver.get(store_url)
            # 點擊購物車清單
            self.driver.execute_script("$('a.sl-cart-toggle').click();")
            time.sleep(1)  # 待購物車完全加載
            # 定位到包含购物车状态的元素
            cart_status_element = self.driver.find_element(By.XPATH, "//div[@ng-show='currentCart.isCartEmpty()']")

            # 检查元素的class属性是否包含'ng-hide'
            if 'ng-hide' in cart_status_element.get_attribute('class'):
                self.show_log("購物車有商品，執行清空操作...")
                # 执行清空购物车操作
                delete_buttons = self.driver.find_elements(By.XPATH, "//a[contains(@ng-click, 'removeItemFromCart')]")
                self.show_log(f"購物車數量:{delete_buttons}", False)
                for button in delete_buttons:
                    self.driver.execute_script("arguments[0].click();", button)
                # 可能需要添加额外的等待时间或检查以确保操作完成
                self.url_end("已清空購物車。")
                self.driver.execute_script("document.getElementById('cart-panel').style.display='block';")
            else:
                self.url_end("購物車已為空。")

        except NoSuchElementException:
            self.url_end("找不到刪除按鈕，購物車可能已空。")
        except TimeoutException:
            self.url_end("操作超時，無法[清除購物車]狀態。")
        except Exception as e:
            self.show_log(f"無法確定[清除購物車]狀態：{e}", False)
            self.url_end("無法確定[清除購物車]狀態。")

    def url_start(self):
        if self.check_input():
            self.toggle_open_browser_mode()  # 切換是否開啟瀏覽器狀態
            self.toggle_ui_elements()
            # 在另一個線程中啟動長時間運行的操作，因為要確保show_log能及時在result_text中顯示，帥呆了 ><
            threading.Thread(target=self.thread_task_by_start, daemon=True).start()

    def thread_task_by_start(self):
        if self.is_login:
            self.start_ordering_process()
        else:
            check_is_login = self.check_login()
            if check_is_login:
                self.is_login = True
                self.start_ordering_process()
            elif check_is_login is False:
                if self.login():
                    self.is_login = True
                    self.show_log("[登入]成功")
                    self.start_ordering_process()

    def start_ordering_process(self):
        try:
            # 商品添加至購物車數量
            self.check_add_cart_num = self.get_add_cart_count_value()
            add_cart_num = self.add_product_to_shopping_cart()
            # 不管所有商品添加 失敗 還是 成功，只要有成功添加一件商品就走訂購流程
            if add_cart_num is not None and add_cart_num > 0:
                self.show_log(f"購物車共有 {add_cart_num} 筆商品。")
                self.show_log("進入下單流程...")
                time.sleep(0.5)
                # 開啟購物車
                self.driver.execute_script("document.getElementById('cart-panel').style.display='block';")
                car_dialog = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'cart-panel'))
                )
                # 點擊下單
                car_checkout_button = car_dialog.find_element(By.ID, "btn-checkout")
                car_checkout_button.click()
                # 待調整 : 需要檢查是否為登入狀態
                # 進入訂購畫面
                self.checkout_products()
            else:
                self.url_end("此次流程查無商品加入購物車，流程結束。")
        except TimeoutException:
            self.url_end("操作超時，無法取得[下單流程]狀態。")
        except Exception as e:
            self.show_log(f"無法確定[下單流程]狀態：{e}", False)
            self.url_end("無法確定[下單流程]狀態")

    def get_add_cart_count_value(self):
        try:
            # 尝试将字符串转换为整数
            return int(self.check_add_cart_count_entry.get())
        except ValueError:
            # 如果转换失败，则返回默认值 5
            return 5

    def check_login(self):
        self.show_log("檢查登入狀態中...")
        try:
            # 加載URL
            self.driver.get(store_url)

            # 取所有<a>
            a_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.NavigationBar-actionMenu-button.nav-color'))
            )

            href_value = None
            for item in a_list:
                href_value = item.get_attribute('href')
                self.show_log(f"href_value : {href_value}", False)
                if href_value is not None:
                    if "/users/sign_in" in href_value:
                        # 未登入，執行登入操作
                        self.show_log("未登入，轉向登入頁面並登入中...")
                        return False
                    else:
                        # 已登入
                        # 使用正则表达式提取编码
                        match = re.search(r'/users/(\w+)/edit', href_value)
                        if match:
                            code = match.group(1)
                            self.show_log(f"已登入。會員編號Url : {code}。")
                            return True
                        else:
                            href_value = None
            if href_value is None:
                self.url_end("無法獲取登入按鈕標籤，請求大美女工程師協助。")
                return None
        except TimeoutException:
            self.url_end("操作超時，無法[檢查登入]狀態。")
            return None
        except Exception as e:
            self.url_end(f"無法確定[檢查登入]狀態：{e}")
            return None

    def get_product_ky(self):
        # 初始化购买列表
        buy_list = []

        # 组合条目和尺寸变量
        entries_and_sizes = [
            (self.ky1_entry, self.size1_var),
            (self.ky2_entry, self.size2_var),
            (self.ky3_entry, self.size3_var),
            (self.ky4_entry, self.size4_var),
            (self.ky5_entry, self.size5_var)
        ]

        # 遍历组合，构建购买列表
        for entry, size_var in entries_and_sizes:
            ky = entry.get()
            if ky.strip():  # 檢查是否前後都空白
                buy_list.append({"pName": ky.strip(), "size": size_var.get()})

        self.show_log(f"buy_list:{len(buy_list)}", False)
        # 返回购买列表
        return buy_list

    @staticmethod
    def remove_spaces(string):
        # 轉小寫 + 去除空白空格
        return ''.join(string.lower().split())

    def find_product_by_keyword(self, keyword, buy_list):
        # 将关键词格式化为小写以实现大小写不敏感的搜索
        keyword = self.remove_spaces(keyword)
        for item in buy_list:
            item_name = self.remove_spaces(item["pName"])
            self.show_log(f"item name: {item_name}", False)
            # 检查商品名称是否包含关键词
            if item_name in keyword:
                return item
        # 如果没有找到匹配的商品，则返回None或相应的消息
        return None

    def add_product_to_shopping_cart(self, is_refresh=False):
        # 添加商品到購物車的數量
        add_cart_count = 0
        try:
            # 加載URL (因登入成公會導頁到首頁，所以這邊還是需要將頁面導到goopi中)
            if is_refresh:
                self.driver.refresh()
            else:
                self.driver.get(store_url)
            wait = WebDriverWait(self.driver, 10)

            # 確認要買的商品
            buy_list = self.get_product_ky()

            # 取前10個 product 元素
            product_list = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'productList__product'))
            )[:10]

            # 符合產品名比對成功次數，因商品可能售完無法加入購物車，只要比對成功，就算是商品已上架在官網
            matched_count = 0
            for item in product_list:
                product_id = item.get_attribute('product-id')
                product_name_element = item.find_element(By.CSS_SELECTOR, ".title.text-primary-color")
                product_name = product_name_element.text if product_name_element else "未知產品名稱"
                product_status_elements = item.find_elements(By.CSS_SELECTOR, ".sold-out-item")
                product_status = 1 if product_status_elements else 0  # 1:已售完，0:還有庫存

                self.show_log(f"product_id: {product_id}，product_name:{product_name}", False)
                matched_product = self.find_product_by_keyword(product_name, buy_list)
                # 检查是否找到匹配项
                if matched_product:
                    matched_count += 1
                    if product_status == 1:
                        self.show_log(f"{product_name} 該商品已售完")
                    else:
                        self.show_log(f"添加 {product_name} 到購物車中...")
                        add_car = item.find_element(
                            By.CSS_SELECTOR,
                            ".btn-add-to-cart.js-btn-add-to-cart.mobile-cart.visible-xs.visible-sm")
                        add_car.click()

                        # 選擇尺寸跟數量的視窗，這邊只點擊尺寸。定位到弹窗外层div
                        info_dialog = wait.until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[uib-modal-window="modal-window"]'))
                        )

                        size = matched_product.get('size')
                        self.show_log(f"size:{size}", False)
                        if size != "無":
                            select_element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "selectpicker")))
                            if select_element:
                                # 创建 Select 对象并选择尺寸
                                Select(select_element).select_by_value(f"string:{size}")
                            else:
                                # 有可能是帽子無尺寸，但使用者選擇尺寸了
                                self.show_log(f"找不到符合{size}尺寸的商品，這邊接續訂購流程...")

                        # 定位到 class 为 "txt-notify wrap-sold-out" 的元素
                        sold_out_elements = info_dialog.find_elements(By.CLASS_NAME, "txt-notify.wrap-sold-out")
                        # 检查元素是否存在并且是否含有 "ng-hide" 类
                        if sold_out_elements and "ng-hide" not in sold_out_elements[0].get_attribute("class"):
                            # 如果元素存在且不包含 "ng-hide"，则表示商品已售完
                            self.show_log("該商品尺寸已售完")
                            # 關閉[商品加入購物車]視窗
                            self.driver.execute_script("arguments[0].click();", info_dialog)
                        else:
                            add_to_cart_button = info_dialog.find_element(By.ID, "btn-add-to-cart")
                            add_to_cart_button.click()
                            pr_is_over = self.product_num_is_over()
                            if pr_is_over:
                                self.show_log("該商品購買上限為 1 件，購物車已有此商品。")
                                add_cart_count += 1
                                # 關閉[商品加入購物車]視窗
                                self.driver.execute_script("arguments[0].click();", info_dialog)
                            elif not pr_is_over:
                                # 關閉購物車清單視窗
                                modal_mask = WebDriverWait(self.driver, 10).until(
                                    EC.presence_of_element_located(
                                        (By.CSS_SELECTOR, ".Modal-mask.cart-mask.js-modal-mask"))
                                )
                                self.driver.execute_script("arguments[0].click();", modal_mask)
                                self.show_log("添加成功!")
                                add_cart_count += 1
                            else:
                                # pr_is_over Exception
                                pass
                # for迴圈結束 ^
            if matched_count == 0:
                if self.check_add_cart_count is self.check_add_cart_num:
                    self.check_add_cart_count = 0
                    return 0
                self.show_log("無商品添加至購物車，繼續檢查中...")
                self.check_add_cart_count += 1
                self.add_product_to_shopping_cart(True)
            else:
                return add_cart_count
        except TimeoutException:
            self.show_log("操作超時，添加失敗。")
            return add_cart_count
        except Exception as e:
            self.show_log(f"無法確定[商品加入購物車]狀態：{e}", False)
            self.show_log("添加失敗。")
            return add_cart_count

    def product_num_is_over(self):
        try:
            is_over = WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".reset-bottom-to-zero.ng-binding")))
            if is_over:
                return True
            else:
                return False
        except TimeoutException:
            return False
        except Exception as e:
            self.show_log(f"無法確定該商品數量問題：{e}", False)
            self.show_log("無法確定該商品數量問題")
            return None

    def checkout_products(self):
        self.show_log("訂購確認中...")
        try:
            wait = WebDriverWait(self.driver, 10)

            # 前往填寫資料頁面
            checkout_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn.btn-success.btn-block.btn-checkout'))
            )
            checkout_button.click()

            # 選擇門市
            search_store_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-pick-store"))
            )
            search_store_button.click()

            if self.search_711_store():
                self.show_log("選擇711門市已完成")
                # 勾選同意書
                if self.check_the_consent_form():
                    self.show_log("同意書已點擊正確，提交訂單中...")
                    # # 點擊[提交訂單]按鈕
                    # place_order_button = WebDriverWait(driver, 10).until(
                    #     EC.element_to_be_clickable((By.ID, "place-order-recaptcha"))
                    # )
                    # place_order_button.click()
                    self.url_end("下單完成，麻煩請至會員資料查收訂單是否有正常交易。")
                else:
                    self.url_end("同意書點擊異常，停止下單。")
                    return
            else:
                self.url_end("選擇711門市異常，停止下單。")

        except TimeoutException:
            self.url_end("操作超時，無法取得[訂購流程]狀態。")
        except Exception as e:
            self.show_log(f"無法確定[訂購流程]狀態：{e}", False)
            self.url_end("無法確定[訂購流程]狀態，麻煩檢查商品下單數量是否超過以及再次確認是否為登入中")

    def search_711_store(self):
        try:
            # 點擊 '門市店號'
            by_id_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "byID"))
            )
            by_id_button.click()

            self.driver.switch_to.frame("frmMain")

            store_number = self.se_entry.get()
            # 輸入門市號碼
            store_id_input = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "storeIDKey"))
            )
            store_id_input.send_keys(store_number)  # 239444

            # 點擊 '搜尋'
            search_button = self.driver.find_element(By.ID, "send")
            search_button.click()

            # 選擇門市
            select_store = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(@onclick, 'showMap({store_number})')]"))
            )
            select_store.click()

            self.driver.switch_to.default_content()
            # 確認門市
            confirm_button = self.driver.find_element(By.ID, "sevenDataBtn")
            confirm_button.click()

            # 同意選擇門市
            accept_button = self.driver.find_element(By.ID, "AcceptBtn")
            accept_button.click()

            # 確認提交
            submit_button = self.driver.find_element(By.ID, "submit_butn")
            submit_button.click()

            return True
        except TimeoutException:
            self.show_log("操作超時，無法取得[搜尋門市]狀態。")
            return False
        except Exception as e:
            self.show_log(f"無法確定[搜尋門市]狀態：{e}")
            return False

    def check_the_consent_form(self):
        try:
            label_list = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.control-label'))
            )
            consent_count = 0
            for label in label_list:
                try:
                    consent_form = label.find_element(By.NAME, 'policy')
                    self.driver.execute_script("arguments[0].click();", consent_form)
                    consent_count += 1
                except NoSuchElementException:
                    pass
                except Exception as e:
                    self.show_log(f"Error clicking on consent form: {e}")

                try:
                    recipient_info = label.find_element(
                        By.CSS_SELECTOR,
                        'input[type="checkbox"][data-e2e-id="order-delivery-recipient-is-customer_checkbox"]')
                    if recipient_info:
                        label.click()
                        consent_count += 1
                except NoSuchElementException:
                    # 處理元素未找到的情況
                    pass
            return consent_count == 2
        except TimeoutException:
            self.show_log("操作超時，無法取得[勾選同意書]狀態。")
            return False
        except Exception as e:
            self.show_log(f"無法確定[勾選同意書]狀態：{e}")
            return False

    def url_login(self):
        if self.check_input(False):
            self.toggle_open_browser_mode()  # 切換是否開啟瀏覽器狀態
            self.toggle_ui_elements()
            # 在另一個線程中啟動長時間運行的操作，因為要確保show_log能及時在result_text中顯示，帥呆了 ><
            threading.Thread(target=self.thread_task_by_login, daemon=True).start()

    def thread_task_by_login(self):
        self.is_login = False
        check_is_login = self.check_login()
        if check_is_login is False:
            if self.login():
                self.is_login = True
                self.url_end("[登入]成功!")
        else:
            self.url_end("-------------")

    def login(self):
        self.driver.get(login_url)
        acc = self.acc_entry.get()
        sec = self.sec_entry.get()
        try:
            wait = WebDriverWait(self.driver, 10)

            # 找到帳號輸入框並輸入帳號
            acc_input = wait.until(
                EC.visibility_of_element_located((By.NAME, 'mobile_phone_or_email'))
            )
            acc_input.clear()
            acc_input.send_keys(acc)

            # 找到密码输入框并输入密码
            sec_input = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-e2e-id='login-password_input']"))
            )
            sec_input.clear()
            sec_input.send_keys(sec)

            # 找到登入按鈕並點擊
            login_button = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-e2e-id='login-submit_button']"))
            )
            login_button.click()

            return self.login_is_success()
        except TimeoutException:
            self.url_end("[登入]失敗 : 操作超時，元素無法交互")
        except Exception as e:
            self.url_end(f"[登入]失敗 : 無法獲取亂碼：{e}")

    def login_is_success(self):
        try:
            error_message_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert.alert-danger:not(.ng-hide) .ng-binding'))
            )
            if error_message_element:
                error_message = error_message_element.text.strip()
                self.url_end(f"登入失敗 :{error_message}")
                return False
            else:
                return True
        except TimeoutException:
            return True
        except Exception as e:
            self.url_end(f"[登入]失敗 : 無法獲取亂碼：{e}")
            return False

    def show_log(self, msg, is_show=True):
        if is_show:
            self.msg_text.config(state=tk.NORMAL)
            # 在Text控件的末尾追加日志
            self.msg_text.insert(tk.END, msg + "\n")
            # 滚动到Text控件的末尾
            self.msg_text.see(tk.END)
            self.msg_text.config(state=tk.DISABLED)
        # 获取当前时间并格式化为字符串
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        # 将时间戳添加到消息前面
        formatted_message = f"[{timestamp}] {msg}"
        print(formatted_message)

    def url_end(self, msg):
        self.show_log(msg)
        self.show_log("-----------------------------")
        self.master.after(0, self.toggle_ui_elements, tk.NORMAL)

    def clear_message(self):
        self.msg_text.config(state=tk.NORMAL)
        self.msg_text.delete("1.0", tk.END)
        self.msg_text.config(state=tk.DISABLED)

    # def fetch_product_ids(self):
    #     file_path = 'info.json'
    #     new_product_items = []
    #     try:
    #
    #         # 獲取前10個 product-item 元素
    #         product_items = WebDriverWait(driver, 10).until(
    #             EC.presence_of_all_elements_located((By.TAG_NAME, 'product-item'))
    #         )[:10]
    #
    #         current_product_items = []
    #         for index, item in enumerate(product_items, start=1):
    #             product_id = item.get_attribute('product-id')
    #             product_name_element = item.find_element(By.CSS_SELECTOR, ".title.text-primary-color")
    #             product_name = product_name_element.text if product_name_element else "未知產品名稱"
    #             product_url = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
    #             product_status_elements = item.find_elements(By.CSS_SELECTOR, ".sold-out-item")
    #             product_status = 1 if product_status_elements else 0  # 如果列表不為空，則產品售罄
    #             current_product_items.append({
    #                 "index": index,
    #                 "pId": product_id,
    #                 "pName": product_name,
    #                 "pUrl": product_url,
    #                 "pStatus": product_status
    #             })
    #
    #         # 檢查是否存在 info.json 檔案
    #         if not os.path.exists(file_path):
    #             # 直接儲存到 JSON 中
    #             info = {"memberIdUrl": self.memberLoginIdUrl, "oldProductItems": current_product_items}
    #             with open(file_path, 'w') as file:
    #                 json.dump(info, file, indent=4)
    #             self.show_log("首次記錄產品ID。不下單")
    #         else:
    #             # 從檔案中讀取 oldProductItems 並進行比對
    #             with open(file_path, 'r') as file:
    #                 info = json.load(file)
    #             old_product_items = info.get("oldProductItems", [])
    #
    #             for current_product_item in current_product_items:
    #                 if not old_product_items or current_product_item["pId"] != old_product_items[0]["pId"]:
    #                     new_product_items.append(current_product_item)
    #                     self.show_log(f"發現新產品ID : {current_product_item['pName']}")
    #                 else:
    #                     break
    #             self.show_log("測試結束")
    #             self.master.after(0, self.toggle_ui_elements, tk.NORMAL)
    #     except TimeoutException:
    #         self.show_log("操作超時，無法[讀取商品ID]")
    #     except Exception as e:
    #         self.show_log(f"無法[讀取商品ID]：{e}")
    #
    # def update_member_login_id_url(self, new_member_login_id_url):
    #     if self.memberLoginIdUrl != new_member_login_id_url:
    #         self.memberLoginIdUrl = new_member_login_id_url
    #         self.save_info_to_json()
    #     else:
    #         self.show_log("memberLoginIdUrl已存在，暫不更新。")
    #
    # def save_info_to_json(self, new_product_items=None):
    #     info = {"memberIdUrl": self.memberLoginIdUrl, "oldProductItems": []}
    #     file_path = 'info.json'
    #     # 如果 info.json 文件存在，則讀取原有內容
    #     if os.path.exists(file_path):
    #         with open(file_path, 'r') as file:
    #             info = json.load(file)
    #
    #     # 如果有新的產品項目，則更新當前oldProductItems替換為new_product_items
    #     if new_product_items:
    #         info["oldProductItems"] = new_product_items
    #
    #     # 將更新後的資料儲存到 JSON 文件中
    #     with open(file_path, 'w') as file:
    #         json.dump(info, file, indent=4)
    #     self.show_log(f"存檔成功，商品數量：{len(info['oldProductItems'])}")

    # def add_product_ky(self):
    #     # 限制最大添加次數為5
    #     if self.add_ky_count < 5:
    #         index = self.add_ky_count  # 捕獲當前索引
    #         # 創建新的產品名稱輸入框
    #         ky_entry = Entry(self.master.left_frame)
    #         ky_entry.grid(row=self.current_row, column=0, padx=self.px, pady=self.py, columnspan=6, sticky="we")
    #
    #         # 創建新的尺寸下拉選單
    #         size_var = StringVar(self.master.left_frame)
    #         size_var.set("無")
    #         size_dropdown = OptionMenu(self.master.left_frame, size_var, "1號", "2號", "3號")
    #         size_dropdown.grid(row=self.current_row, column=6, padx=self.px, pady=self.py, sticky="w")
    #
    #         delete_button = Button(self.master.left_frame, text="刪除",
    #                                command=lambda: self.delete_ky_button(index))
    #         delete_button.grid(row=self.current_row, column=7, sticky="we", padx=self.px, pady=self.py)
    #
    #         # 使用索引作為字典鍵
    #         self.product_ky[index] = (ky_entry, (size_var, size_dropdown), delete_button)
    #         # 更新新增次數
    #         self.add_ky_count += 1
    #         self.current_row += 1  # 確保每次新增元素都在新的行
    #     else:
    #         self.add_ky_button.config(text='無法新增，我就爛')
    #         self.add_ky_button.config(state='disabled')

    # def delete_ky_button(self, index):
    #     # 刪除特定索引的元素
    #     ky_entry, size_dropdown_tuple, delete_btn = self.product_ky[index]
    #     ky_entry.destroy()
    #     size_dropdown_tuple[1].destroy()
    #     delete_btn.destroy()
    #     del self.product_ky[index]
    #
    #     # 重新安排剩餘元素的索引
    #     old_keys = sorted(self.product_ky.keys())
    #     for old_index in old_keys:
    #         if old_index > index:
    #             new_index = old_index - 1
    #             self.product_ky[new_index] = self.product_ky.pop(old_index)
    #             # 更新刪除按鈕的命令以反映新索引，将索引作为默认参数传递给 lambda 函数
    #             _, _, delete_btn = self.product_ky[new_index]
    #             delete_btn.config(command=lambda idx=new_index: self.delete_ky_button(idx))
    #
    #     # 更新 add_ky_count 的值
    #     self.add_ky_count -= 1
    #
    #     # 檢查條件並更新 add_ky_button 的狀態
    #     if self.add_ky_count < 5 and self.add_ky_button['state'] == 'disabled':
    #         self.add_ky_button.config(text='新增篩選商品')
    #         self.add_ky_button.config(state='normal')


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
