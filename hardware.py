import platform
import uuid
import subprocess
import os


def get_system():
    system = platform.system()
    return system


def get_win_motherboard_serial():
    """
    Windows - 主板序號
    :return:
    """
    try:
        result = subprocess.check_output("wmic baseboard get serialnumber", shell=True).decode()
        serial = result.split("\n")[1].strip()
        return serial
    except subprocess.CalledProcessError as e:
        print("Error: ", e.output)


def get_win_product_key():
    """
    Windows - 產品序號
    :return:
    """
    try:
        result = subprocess.check_output("wmic path softwarelicensingservice get OA3xOriginalProductKey", shell=True).decode()
        product_key = result.split("\n")[1].strip()
        return product_key
    except subprocess.CalledProcessError as e:
        print("Error: ", e.output)


def get_mac_serial_number():
    """
     Mac - 上獲取電腦序號的示例代碼
    :return:
    """
    try:
        result = subprocess.check_output("system_profiler SPHardwareDataType | grep 'Serial Number (system)'", shell=True).decode()
        n = result.split(": ")[1].strip()
        return n
    except subprocess.CalledProcessError as e:
        print("Error:", e.output)


def get_mac_hardware_info():
    """
    Mac - 主機板序號
    :return:
    """
    try:
        result = subprocess.check_output("system_profiler SPHardwareDataType", shell=True).decode()
        return result
    except subprocess.CalledProcessError as e:
        print("Error:", e.output)


def get_computer_num():
    c = get_system()
    print(f"System: {c}")
    if c == "Windows":
        return get_win_motherboard_serial()
    elif c == "Mac Os":
        return get_mac_hardware_info()

    else:
        return "Unknown"