import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import sys

if getattr(sys, 'frozen', False):
    # 如果程式是被凍結的（打包成exe）
    basedir = sys._MEIPASS
else:
    # 如果程式是正常執行的
    basedir = os.path.dirname(__file__)

credential_path = os.path.join(basedir, 'credentials.json')

# 使用服务账号密钥初始化 Firebase
cred = credentials.Certificate(credential_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://goopirobot-default-rtdb.firebaseio.com/'
})


def get_data_by_key(key):
    print("------------")
    # 创建数据库引用
    ref = db.reference('/')
    key_ref = ref.child(key)
    # 读取 key_ref 的数据
    key_data = key_ref.get()
    print(key_data)
    # key_ref.set({'cNum': 456})   # 重置
    # key_ref.update({'cNum': 7777})  # 更新
    # key_ref.delete()  # 刪除
    print("------------")
