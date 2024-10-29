from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMenu, QApplication
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QTimer
from PyQt6.QtGui import QPainter, QColor, QPainterPath

class FloatingWindow(QWidget):
    def __init__(self, change_wallpaper_callback):
        super().__init__()
        self.change_wallpaper_callback = change_wallpaper_callback
        self.is_collapsed = True  # 初始状态为收起
        self.drag_position = QPoint()
        self.context_menu_options = {}
        self.collapse_timer = QTimer(self)
        self.collapse_timer.setSingleShot(True)
        self.collapse_timer.timeout.connect(self.collapse)
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.button = QPushButton('', self)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: rgba(200, 200, 200, 150);
                border-radius: 15px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(220, 220, 220, 180);
            }
        """)
        self.button.setFixedSize(30, 30)  # 缩小按钮尺寸
        self.button.clicked.connect(self.change_wallpaper_callback)

        self.setFixedSize(30, 30)  # 缩小窗口尺寸

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())

        painter.setClipPath(path)
        painter.fillPath(path, QColor(200, 200, 200, 150))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        elif event.button() == Qt.MouseButton.RightButton:
            self.showContextMenu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.check_edge_proximity()
            event.accept()

    def check_edge_proximity(self):
        screen = self.screen().geometry()
        button_pos = self.geometry()

        if button_pos.right() >= screen.width() - 20:
            self.collapse_to_right()
        else:
            self.is_collapsed = False

    def collapse_to_right(self):
        if not self.is_collapsed:
            self.original_pos = self.pos()
            screen = self.screen().geometry()
            self.animate_collapse(screen.width() - 10, self.y())

    def animate_collapse(self, x, y):
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPoint(x, y))
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()
        self.is_collapsed = True

    def enterEvent(self, event):
        self.collapse_timer.stop()
        if self.is_collapsed:
            self.animate_expand()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.collapse_timer.start(500)  # 500毫秒后收起
        super().leaveEvent(event)

    def animate_expand(self):
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(QPoint(self.x() - 20, self.y()))  # 展开时向左移动20像素
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.start()
        self.is_collapsed = False

    def collapse(self):
        if not self.is_collapsed:
            screen = self.screen().geometry()
            self.animate_collapse(screen.width() - 10, self.y())

    def showContextMenu(self, point):
        contextMenu = QMenu(self)
        for option_name, callback in self.context_menu_options.items():
            action = contextMenu.addAction(option_name)
            action.triggered.connect(lambda checked, cb=callback, p=point: cb(p))
        closeAction = contextMenu.addAction("关闭")
        action = contextMenu.exec(point)
        if action == closeAction:
            QApplication.instance().quit()

    def add_context_menu_option(self, option_name, callback):
        self.context_menu_options[option_name] = callback
