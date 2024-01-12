from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib


class AESCipher:
    def __init__(self, key):
        # 將密鑰填充到適合AES的長度（16, 24, 32字節）
        # 這個key若遇到剛好16字節會擴充到32
        self.key = pad(key.encode(), AES.block_size)

    def encrypt(self, data):
        # 為加密準備數據
        data = pad(data.encode(), AES.block_size)
        # 使用密鑰和初始化向量（IV）創建密碼物件
        cipher = AES.new(self.key, AES.MODE_CBC)
        # 加密數據
        encrypted_data = cipher.encrypt(data)
        # 將IV和加密後的數據連接，然後進行編碼
        return base64.b64encode(cipher.iv + encrypted_data).decode()

    def decrypt(self, encrypted_data):
        # 從base64解碼數據
        encrypted_data = base64.b64decode(encrypted_data)
        # 提取IV
        iv = encrypted_data[:AES.block_size]
        # 提取加密數據
        encrypted_data = encrypted_data[AES.block_size:]
        # 使用密鑰和提取的IV創建密碼物件
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        # 解密數據並去除填充
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted_data.decode()
