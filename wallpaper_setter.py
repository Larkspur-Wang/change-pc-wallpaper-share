import ctypes
import os
import winreg
import win32con

class WallpaperSetter:
    @staticmethod
    def set_wallpaper(image_path):
        # 确保文件路径是绝对路径
        abs_image_path = os.path.abspath(image_path)
        
        # 检查文件是否存在
        if not os.path.exists(abs_image_path):
            print(f"错误: 文件 {abs_image_path} 不存在")
            return False

        # 设置壁纸样式为适应
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "6")  # 6 表示适应
        winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        winreg.CloseKey(key)

        # 设置壁纸
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, abs_image_path, win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE)

        return True
