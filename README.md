# GUIC
making a GUI crawler

第一次練習爬蟲並建立一個GUI  (GPT教學)
安裝指令  :  pip install requests  (庫)
            pip install pyinstaller (將py轉exe)
            pyinstaller --onefile main.py  (產exe)

注意!!!
先去 requirements.txt 執行下載.venv(建立虛擬環境)

簡單說明 GUI類型  目前先使用【Tkinter】來實作
Tkinter:
Tkinter是Python标准库中自带的GUI库，因此不需要额外安装。
它提供了相对简单的接口，适合初学者。然而，它的外观相对较为简单，可能不如其他库提供的现代化外观。
Tkinter基于Tk GUI工具包，它是一个跨平台的工具包，但在某些平台上可能没有其他库那么好看。

PyQt:
PyQt是基于Qt库的Python绑定，Qt是一个强大且成熟的C++ GUI库。
PyQt提供了丰富的功能和现代化的外观，支持大量的组件和特性。
PyQt是一个相对重量级的库，但也因此提供了更多的灵活性和功能。

wxPython:
wxPython是基于wxWidgets库的Python绑定，wxWidgets是一个用C++编写的跨平台GUI库。
wxPython提供了良好的跨平台性能，并具有相对现代化的外观。
它是一个中等规模的库，介于Tkinter和PyQt之间，提供了足够的功能，同时也保持了一定的简单性。