import sys
import os
import random
from PyQt6.QtWidgets import QApplication, QMenu
from PyQt6.QtCore import QTimer, QThread, pyqtSignal, QPoint
from floating_window import FloatingWindow
from wallpaper_generator import WallpaperGenerator
from wallpaper_setter import WallpaperSetter
from config import CHANGE_INTERVAL, WALLPAPER_DIR, PROMPTS, DEFAULT_PROMPT_TYPE

class WallpaperThread(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, wallpaper_generator, wallpaper_setter, prompt):
        super().__init__()
        self.wallpaper_generator = wallpaper_generator
        self.wallpaper_setter = wallpaper_setter
        self.prompt = prompt

    def run(self):
        print("开始更换壁纸...")
        print(f"使用提示词: {self.prompt}")
        wallpaper_path = self.wallpaper_generator.generate_wallpaper(self.prompt)
        if wallpaper_path:
            print(f"壁纸生成成功,路径: {wallpaper_path}")
            success = self.wallpaper_setter.set_wallpaper(wallpaper_path)
            if success:
                print("壁纸已成功更新")
            else:
                print("设置壁纸失败")
            self.finished.emit(success)
        else:
            print("生成壁纸失败")
            self.finished.emit(False)
        print("更换壁纸过程结束")

class AutoWallpaper:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.wallpaper_generator = WallpaperGenerator()
        self.wallpaper_setter = WallpaperSetter()
        self.floating_window = FloatingWindow(self.change_wallpaper)
        self.timer = QTimer()
        self.current_prompt_type = DEFAULT_PROMPT_TYPE
        
        # 确保wallpaper文件夹存在
        os.makedirs(WALLPAPER_DIR, exist_ok=True)

        # 添加右键菜单选项
        self.floating_window.add_context_menu_option("更换壁纸类型", self.show_prompt_menu)

        # 设置初始位置
        self.set_initial_position()

    def set_initial_position(self):
        screen = self.app.primaryScreen().geometry()
        initial_x = screen.width() - 10  # 10是窗口右边缘到屏幕右边缘的距离
        initial_y = 5  # 5是窗口上边缘到屏幕上边缘的距离
        self.floating_window.move(initial_x, initial_y)
        self.floating_window.original_pos = QPoint(initial_x - 20, initial_y)  # 展开位置
        self.floating_window.is_collapsed = True

    def start(self):
        self.floating_window.show()
        self.timer.timeout.connect(self.change_wallpaper)
        self.timer.start(CHANGE_INTERVAL * 1000)  # 转换为毫秒
        sys.exit(self.app.exec())

    def change_wallpaper(self):
        prompt = PROMPTS[self.current_prompt_type]
        self.thread = WallpaperThread(self.wallpaper_generator, self.wallpaper_setter, prompt)
        self.thread.finished.connect(self.on_wallpaper_change_finished)
        self.thread.start()

    def on_wallpaper_change_finished(self, success):
        if success:
            print("壁纸更换成功")
        else:
            print("壁纸更换失败")

    def show_prompt_menu(self, point):
        menu = QMenu()
        for prompt_type in PROMPTS.keys():
            action = menu.addAction(prompt_type)
            action.triggered.connect(lambda checked, pt=prompt_type: self.set_prompt_type(pt))
        menu.exec(point)

    def set_prompt_type(self, prompt_type):
        self.current_prompt_type = prompt_type
        print(f"已更改壁纸类型为: {prompt_type}")
        self.change_wallpaper()  # 立即更换壁纸

if __name__ == "__main__":
    auto_wallpaper = AutoWallpaper()
    auto_wallpaper.start()
