import ttkbootstrap as tb
from ttkbootstrap.constants import *
import array as array
from gui.serial_test import SerialGUI

def center_window(win, width=400, height=300):
    # Lấy kích thước màn hình
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Tính toán vị trí giữa
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Cố định kích thước và vị trí cửa sổ
    win.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    # "cosmo", "darkly", "superhero", "flatly", "cyborg", "solar"
    root = tb.Window(themename="flatly")  # Bạn có thể chọn theme khác
    center_window(root, 750, 500)  # Căn giữa cửa sổ với kích thước 750x500
    app = SerialGUI(root)
    root.resizable(False, False)
    # Gán hàm xử lý cho sự kiện đóng cửa sổ
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()