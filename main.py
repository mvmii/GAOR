# 第一次練習爬蟲並建立一個GUI  (GPT教學)
# 安裝指令  :  pip install requests  (庫)
#            pip install beautifulsoup4 (來解析 HTML，並找到相應的元素)
#             pip install pyinstaller (將py轉exe)
#             pyinstaller --onefile main.py  (產exe)
#             pip install selenium  (以訪客身分開啟 Edge 並加載當前網址)

# 簡單說明 GUI類型  目前先使用【Tkinter】來實作

import os
import tkinter as tk
from tkinter import Entry, Label, Button, Text, Scrollbar, StringVar, OptionMenu
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import threading
import re

# 配置無頭模式
edge_options = Options()
edge_options.add_argument("--headless")  # 啟用無頭模式
edge_options.add_argument("--disable-gpu")  # 在無頭模式下，禁用 GPU 加速有時是必要的

# 使用Selenium開啟Edge瀏覽器
driver = webdriver.Edge(options=edge_options)  # 確保已下載並設定好Edge WebDriver的路徑


class MainApplication:  # 模組化
    def __init__(self, master):
        # 設置變數
        self.textMessageLog = ""
        self.cmdMessageLog = ""
        self.memberLoginIdUrl = "testMemberLoginId"
        self.current_row = 1
        # 使用字典來儲存產品條目和尺寸下拉選單
        self.product_ky = {}  # key為索引，value為(product_entry, size_dropdown)元組
        # 初始化新增次數
        self.add_ky_count = 0
        self.blank_px = 18
        self.px = 5
        self.py = 2

        # 設置視窗
        self.master = master
        self.master.title("測試登入")
        # 寬度和高度
        self.master.geometry("650x400")
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

        self.n1_label = Label(self.master.left_frame, text="  ")
        self.n1_label.grid(row=self.current_row, column=0, sticky="we", padx=self.blank_px, pady=self.py)
        self.n2_label = Label(self.master.left_frame, text="  ")
        self.n2_label.grid(row=self.current_row, column=1, sticky="we", padx=self.blank_px, pady=self.py)
        self.n3_label = Label(self.master.left_frame, text="  ")
        self.n3_label.grid(row=self.current_row, column=2, sticky="we", padx=self.blank_px, pady=self.py)
        self.n4_label = Label(self.master.left_frame, text="  ")
        self.n4_label.grid(row=self.current_row, column=3, sticky="we", padx=self.blank_px, pady=self.py)
        self.n5_label = Label(self.master.left_frame, text="  ")
        self.n5_label.grid(row=self.current_row, column=4, sticky="we", padx=self.blank_px, pady=self.py)
        self.n6_label = Label(self.master.left_frame, text="  ")
        self.n6_label.grid(row=self.current_row, column=5, sticky="we", padx=self.blank_px, pady=self.py)
        self.current_row += 1

        # 輸入帳號 Str
        self.acc_label = Label(self.master.left_frame, text="帳號：")
        self.acc_label.grid(row=self.current_row, column=0, sticky="w", padx=self.px, pady=self.py)
        # 輸入帳號 input
        self.acc_entry = Entry(self.master.left_frame, width=30)
        self.acc_entry.grid(row=self.current_row, column=1, sticky="we", padx=self.px, pady=self.py, columnspan=4)
        self.acc_entry.insert(0, "love_8462564@yahoo.com.tw")
        self.current_row += 1

        # 輸入密碼 Str
        self.sec_label = Label(self.master.left_frame, text="密碼：")
        self.sec_label.grid(row=self.current_row, column=0, sticky="w", padx=self.px, pady=self.py)
        # 輸入密碼 input
        self.sec_entry = Entry(self.master.left_frame, width=30)
        self.sec_entry.grid(row=self.current_row, column=1, sticky="we", padx=self.px, pady=self.py, columnspan=4)
        self.sec_entry.insert(0, "mvmii1234")
        self.current_row += 1

        # 新增
        self.add_ky_button = Button(self.master.left_frame, text="新增篩選商品", command=self.add_product_ky)
        self.add_ky_button.grid(row=self.current_row, column=0, columnspan=2, sticky="we", padx=self.px, pady=self.py)
        # 開始
        self.start_button = Button(self.master.left_frame, text="開始", command=self.url_start)
        self.start_button.grid(row=self.current_row, column=2, sticky="we", padx=self.px, pady=self.py)
        # 結束
        self.end_button = Button(self.master.left_frame, text="結束")
        self.end_button.grid(row=self.current_row, column=3, sticky="we", padx=self.px, pady=self.py)
        self.current_row += 1

        self.input_ky_label = Label(self.master.left_frame, text="輸入要買的新品關鍵字(含顏色)")
        self.input_ky_label.grid(row=self.current_row, column=0, sticky="we", padx=self.px, pady=self.py, columnspan=3)
        self.input_size_label = Label(self.master.left_frame, text="尺寸")
        self.input_size_label.grid(row=self.current_row, column=3, sticky="we", padx=self.px, pady=self.py)
        self.input_delete_label = Label(self.master.left_frame, text="刪除")
        self.input_delete_label.grid(row=self.current_row, column=4, sticky="we", padx=self.px, pady=self.py)
        self.current_row += 1

        # Scrollbar
        self.scrollbar = Scrollbar(self.master.right_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text
        self.message_box = Text(self.master.right_frame, yscrollcommand=self.scrollbar.set)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.message_box.config(state=tk.DISABLED)  # 默认不可编辑
        self.scrollbar.config(command=self.message_box.yview)

    def add_product_ky(self):
        # 限制最大添加次數為5
        if self.add_ky_count < 5:
            index = self.add_ky_count  # 捕獲當前索引
            # 創建新的產品名稱輸入框
            ky_entry = Entry(self.master.left_frame)
            ky_entry.grid(row=self.current_row, column=0, padx=self.px, pady=self.py, columnspan=3, sticky="we")

            # 創建新的尺寸下拉選單
            size_var = StringVar(self.master.left_frame)
            size_var.set("無")
            size_dropdown = OptionMenu(self.master.left_frame, size_var, "M", "L", "XL")
            size_dropdown.grid(row=self.current_row, column=3, padx=self.px, pady=self.py, sticky="w")

            delete_button = Button(self.master.left_frame, text="刪除",
                                   command=lambda: self.delete_ky_button(index))
            delete_button.grid(row=self.current_row, column=4, sticky="we", padx=self.px, pady=self.py)

            # 使用索引作為字典鍵
            self.product_ky[index] = (ky_entry, (size_var, size_dropdown), delete_button)
            # 更新新增次數
            self.add_ky_count += 1
            self.current_row += 1  # 確保每次新增元素都在新的行
        else:
            self.add_ky_button.config(text='無法新增，我就爛')
            self.add_ky_button.config(state='disabled')

    def delete_ky_button(self, index):
        # 刪除特定索引的元素
        ky_entry, size_dropdown_tuple, delete_btn = self.product_ky[index]
        ky_entry.destroy()
        size_dropdown_tuple[1].destroy()
        delete_btn.destroy()
        del self.product_ky[index]

        # 重新安排剩餘元素的索引
        old_keys = sorted(self.product_ky.keys())
        for old_index in old_keys:
            if old_index > index:
                new_index = old_index - 1
                self.product_ky[new_index] = self.product_ky.pop(old_index)
                # 更新刪除按鈕的命令以反映新索引，将索引作为默认参数传递给 lambda 函数
                _, _, delete_btn = self.product_ky[new_index]
                delete_btn.config(command=lambda idx=new_index: self.delete_ky_button(idx))

        # 更新 add_ky_count 的值
        self.add_ky_count = len(self.product_ky)

        # 檢查條件並更新 add_ky_button 的狀態
        if self.add_ky_count < 5 and self.add_ky_button['state'] == 'disabled':
            self.add_ky_button['state'] = 'normal'
            self.add_ky_button.config(text='新增篩選商品')

    def url_start(self):
        """
        開始流程流程 :
        檢查登入狀態 => 登入
        -- 跳轉連結[https://www.goopi.co/categories/goopimade-goopi-%E5%AD%A4%E5%83%BB?sort_by=created_at&order_by=desc]
           -- 檢查是否有新品
              -- 有新品 : 加入購物車
                 -- 訂單結帳
              -- 無新品 : 跳提示語[暫無新品]
        :return:
        """
        self.clear_msg()
        self.toggle_ui_elements()
        # 在另一個線程中啟動長時間運行的操作，因為要確保show_log能及時在result_text中顯示，帥呆了 ><
        threading.Thread(target=self.check_login, daemon=True).start()
    def get_product_ky(self):
        # 檢索產品條目和尺寸下拉選單的值
        for index, (ky_entry, size_dropdown_tuple, _) in self.product_ky.items():
            product = ky_entry.get()
            size = size_dropdown_tuple[0].get()
            # 使用產品和尺寸資料
            # 這裡可以添加您需要的邏輯來處理這些資料
            self.show_log(f"產品:{product}，尺寸:{size}")

    def toggle_ui_elements(self, state=tk.DISABLED):
        """ 切換UI元件的可用性 """
        elements = [self.acc_entry, self.sec_entry, self.start_button, self.add_ky_button]
        for element in elements:
            element.config(state=state)

    def check_login(self):
        self.show_log("檢查登入狀態中...")
        url = "https://www.goopi.co/categories/goopimade-goopi-%E5%AD%A4%E5%83%BB?sort_by=created_at&order_by=desc"
        try:
            # 加載URL
            driver.get(url)

            # 取所有<a>
            a_list = WebDriverWait(driver, 10).until(
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
                        driver.get(href_value)
                        self.login()
                        # self.show_log("暫時假裝登入成功!!")
                        # self.fetch_product_ids()
                        break  # 中斷迴圈
                    else:
                        # 已登入
                        self.update_member_login_id_url(href_value)
                        # 使用正则表达式提取编码
                        match = re.search(r'/users/(\w+)/edit', href_value)
                        if match:
                            code = match.group(1)
                            self.show_log(f"已登入。會員編號Url : {code}。導頁至GOOPI-GOOPIMADE頁面。")
                            self.fetch_product_ids()
                            break  # 中斷迴圈
                        else:
                            href_value = None
            if href_value is None:
                self.show_log("無法獲取登入按鈕標籤，請求大美女工程師協助。")
        except TimeoutException:
            self.show_log("操作超時，無法[檢查登入]狀態。")
        except Exception as e:
            self.show_log(f"無法確定[檢查登入]狀態：{e}")

    def fetch_product_ids(self):
        file_path = 'info.json'
        new_product_items = []
        try:
            selected_value = int(self.productCount_dropdown.get())  # 獲取當前選擇的值

            # 獲取前10個 product-item 元素
            product_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, 'product-item'))
            )[:selected_value]

            current_product_items = []
            for index, item in enumerate(product_items, start=1):
                product_id = item.get_attribute('product-id')
                product_name_element = item.find_element(By.CSS_SELECTOR, ".title.text-primary-color")
                product_name = product_name_element.text if product_name_element else "未知產品名稱"
                product_url = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
                product_status_elements = item.find_elements(By.CSS_SELECTOR, ".sold-out-item")
                product_status = 1 if product_status_elements else 0  # 如果列表不為空，則產品售罄
                current_product_items.append({
                    "index": index,
                    "pId": product_id,
                    "pName": product_name,
                    "pUrl": product_url,
                    "pStatus": product_status
                })

            # 檢查是否存在 info.json 檔案
            if not os.path.exists(file_path):
                # 直接儲存到 JSON 中
                info = {"memberIdUrl": self.memberLoginIdUrl, "oldProductItems": current_product_items}
                with open(file_path, 'w') as file:
                    json.dump(info, file, indent=4)
                self.show_log("首次記錄產品ID。不下單")
            else:
                # 從檔案中讀取 oldProductItems 並進行比對
                with open(file_path, 'r') as file:
                    info = json.load(file)
                old_product_items = info.get("oldProductItems", [])

                for current_product_item in current_product_items:
                    if not old_product_items or current_product_item["pId"] != old_product_items[0]["pId"]:
                        new_product_items.append(current_product_item)
                        self.show_log(f"發現新產品ID : {current_product_item['pName']}")
                    else:
                        break
                self.show_log("測試結束")
                self.master.after(0, self.toggle_ui_elements, tk.NORMAL)
        except TimeoutException:
            self.show_log("操作超時，無法[讀取商品ID]")
        except Exception as e:
            self.show_log(f"無法[讀取商品ID]：{e}")

    def update_member_login_id_url(self, new_member_login_id_url):
        if self.memberLoginIdUrl != new_member_login_id_url:
            self.memberLoginIdUrl = new_member_login_id_url
            self.save_info_to_json()
        else:
            self.show_log("memberLoginIdUrl已存在，暫不更新。")

    def save_info_to_json(self, new_product_items=None):
        info = {"memberIdUrl": self.memberLoginIdUrl, "oldProductItems": []}
        file_path = 'info.json'
        # 如果 info.json 文件存在，則讀取原有內容
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                info = json.load(file)

        # 如果有新的產品項目，則更新當前oldProductItems替換為new_product_items
        if new_product_items:
            info["oldProductItems"] = new_product_items

        # 將更新後的資料儲存到 JSON 文件中
        with open(file_path, 'w') as file:
            json.dump(info, file, indent=4)
        self.show_log(f"存檔成功，商品數量：{len(info['oldProductItems'])}")

    def login(self):
        acc = self.acc_entry.get()
        sec = self.sec_entry.get()
        try:
            # 帳號輸入
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, 'mobile_phone_or_email'))
            )
            # 找到帳號輸入框並輸入帳號
            acc_input = driver.find_element(By.NAME, 'mobile_phone_or_email')
            acc_input.clear()
            acc_input.send_keys(acc)

            # 密码输入
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "input[data-e2e-id='login-password_input']"))
            )
            # 找到密码输入框并输入密码
            sec_input = driver.find_element(By.CSS_SELECTOR, "input[data-e2e-id='login-password_input']")
            sec_input.clear()
            sec_input.send_keys(sec)

            # 登入
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-e2e-id='login-submit_button']"))
            )
            # 找到登入按鈕並點擊
            login_button = driver.find_element(By.CSS_SELECTOR, "button[data-e2e-id='login-submit_button']")
            login_button.click()
            self.show_log("[登入]成功!")
            self.fetch_product_ids()
        except TimeoutException:
            self.show_log("[登入]失敗 : 操作超時，元素無法交互")
        except Exception as e:
            self.show_log(f"[登入]失敗 : 無法獲取亂碼：{e}")

    def show_log(self, msg, show_on_text=True):
        if show_on_text:
            self.textMessageLog += (msg + "\n")
            self.message_box.config(state=tk.NORMAL)  # 允许写入
            self.message_box.delete(1.0, "end")
            self.message_box.insert("end", self.textMessageLog)
            self.message_box.config(state=tk.DISABLED)  # 禁止写入
        self.cmdMessageLog += (msg + "\n")
        print(self.cmdMessageLog)

    def clear_msg(self):
        self.textMessageLog = ""
        self.message_box.insert("end", self.textMessageLog)


if __name__ == "__main__":
    # 创建主窗口
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()
