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

        # 設置視窗
        self.master = master
        self.master.title("測試登入")
        # 寬度和高度
        self.master.geometry("600x350")
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

        # 輸入帳號 Str
        self.acc_label = Label(self.master.left_frame, text="帳號：")
        self.acc_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)
        # 輸入帳號 input
        self.acc_entry = Entry(self.master.left_frame, width=30)
        self.acc_entry.grid(row=1, column=1, sticky="we", padx=10, pady=2)
        self.acc_entry.insert(0, "love_8462564@yahoo.com.tw")

        # 輸入密碼 Str
        self.sec_label = Label(self.master.left_frame, text="密碼：")
        self.sec_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)
        # 輸入密碼 input
        self.sec_entry = Entry(self.master.left_frame, width=30)
        self.sec_entry.grid(row=2, column=1, sticky="we", padx=10, pady=2)
        self.sec_entry.insert(0, "mvmii1234")

        # 要讀取前幾個商品 的下拉選單
        self.getProductCount_frame = tk.Frame(self.master.left_frame)
        self.getProductCount_frame.grid(row=3, column=0, columnspan=2, sticky="we", padx=10, pady=10)

        self.productCount_label = Label(self.getProductCount_frame, text="讀取")
        self.productCount_label.pack(side="left")

        self.productCount_dropdown = StringVar(self.getProductCount_frame)  # 創建變數來存儲選擇的值
        self.productCount_dropdown.set("10")  # 設定預設值
        self.productCount_dropdownMenu = OptionMenu(self.getProductCount_frame, self.productCount_dropdown, "10", "15",
                                                    "20")
        self.productCount_dropdownMenu.pack(side="left")
        self.productCount_label2 = Label(self.getProductCount_frame, text="個商品")
        self.productCount_label2.pack(side="left")

        # 按鈕
        self.fetch_button = Button(self.master.left_frame, text="開始", command=self.url_start)
        self.fetch_button.grid(row=4, column=0, columnspan=2, sticky="we", padx=10, pady=10)

        # Scrollbar
        self.scrollbar = Scrollbar(self.master.right_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text
        self.message_box = Text(self.master.right_frame, yscrollcommand=self.scrollbar.set)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.message_box.config(state=tk.DISABLED)  # 默认不可编辑
        self.scrollbar.config(command=self.message_box.yview)

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

    def toggle_ui_elements(self, state=tk.DISABLED):
        """ 切換UI元件的可用性 """
        elements = [self.acc_entry, self.sec_entry, self.fetch_button,
                    self.productCount_dropdownMenu]
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
