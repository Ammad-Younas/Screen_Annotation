import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSlider, QToolButton, QColorDialog, QInputDialog, QGraphicsView,
    QGraphicsScene, QGraphicsPathItem, QGraphicsRectItem, QGraphicsEllipseItem,
    QGraphicsTextItem, QGroupBox, QTextEdit, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import (
    QPen, QPainterPath, QColor, QFont, QPalette, QGuiApplication, QIcon, QKeyEvent
)

class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent, overlay_instance):
        super().__init__(parent)
        self.overlay_instance = overlay_instance
        self.setStyleSheet("background: transparent")
        # PyQt6: use QFrame.Shape.NoFrame instead of QGraphicsView.NoFrame
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

    def mousePressEvent(self, event):
        self.overlay_instance.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.overlay_instance.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.overlay_instance.mouseReleaseEvent(event)

class ProfessionalScreenOverlay:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')

        # Set dark theme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(44, 62, 80))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(52, 73, 94))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(44, 62, 80))
        palette.setColor(QPalette.ColorRole.ToolTipBase, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(52, 73, 94))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)
        self.app.setPalette(palette)

        # Drawing state
        self.current_color = QColor(255, 0, 0)
        self.brush_size = 3
        self.current_tool = "pen"
        self.overlay_active = False

        # Load icons
        self.icons = {}
        self.load_icons()

        # Setup control window
        self.control_window = QWidget()
        self.control_window.setWindowTitle("Professional Screen Annotator")
        self.control_window.setFixedSize(320, 520)
        self.control_window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setup_professional_ui()

        # Create overlay
        self.overlay = QWidget()
        self.overlay.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.overlay.setGeometry(QGuiApplication.primaryScreen().geometry())
        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setContentsMargins(0, 0, 0, 0)
        self.view = CustomGraphicsView(None, self)
        self.view.setScene(QGraphicsScene())
        self.scene = self.view.scene()
        screen_rect = self.overlay.geometry()
        self.scene.setSceneRect(0, 0, screen_rect.width(), screen_rect.height())
        overlay_layout.addWidget(self.view)
        self.overlay.hide()

        # Drawing variables
        self.drawing = False
        self.start_pos = None
        self.current_path = None
        self.current_item = None
        self.drawings = []  # list of QGraphicsItem
        self.undo_stack = []
        self.redo_stack = []

        # Bind keyboard shortcuts
        self.control_window.keyPressEvent = self.key_press_event
        self.overlay.keyPressEvent = self.key_press_event

        # Show welcome message
        QMessageBox.information(self.control_window, "Professional Screen Annotator",
                                "Welcome to Professional Screen Annotator!\\n\\n"
                                "Features:\\n"
                                "• Multiple drawing tools with icons\\n"
                                "• Professional UI design\\n"
                                "• Undo/Redo functionality\\n"
                                "• Keyboard shortcuts\\n\\n"
                                "Click 'Start Drawing' to begin!")

    def load_icons(self):
        icon_files = {
            'pen': 'pen.png',
            'rectangle': 'rectangle.png',
            'circle': 'circle.png',
            'ellipse': 'ellipse.png',
            'text': 'text.png',
            'eraser': 'eraser.png',
            'undo': 'undo.png',
            'redo': 'redo.png',
            'delete': 'delete.png'
        }
        icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
        for tool, filename in icon_files.items():
            icon_path = os.path.join(icons_dir, filename)
            if os.path.exists(icon_path):
                self.icons[tool] = QIcon(icon_path)
            else:
                self.icons[tool] = QIcon()  # Placeholder

    def setup_professional_ui(self):
        main_layout = QVBoxLayout(self.control_window)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header
        header_label = QLabel("Screen Annotator Pro")
        header_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        subtitle_label = QLabel("Professional Drawing Tools")
        subtitle_label.setFont(QFont("Segoe UI", 10))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Toggle button
        self.overlay_btn = QPushButton("Start Drawing")
        self.overlay_btn.setStyleSheet("background-color: #27ae60; color: white; font: bold 12pt 'Segoe UI'; padding: 10px; border-radius: 5px;")
        self.overlay_btn.clicked.connect(self.toggle_overlay)
        main_layout.addWidget(self.overlay_btn)

        # Clear button
        clear_btn = QPushButton("Clear All")
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white; font: bold 10pt 'Segoe UI'; padding: 8px; border-radius: 5px;")
        clear_btn.clicked.connect(self.clear_screen)
        main_layout.addWidget(clear_btn)

        # Tools group
        tools_group = QGroupBox("Drawing Tools")
        tools_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        tools_layout = QHBoxLayout()
        tools_layout.setSpacing(5)

        self.tool_buttons = {}
        tools = ['pen', 'rectangle', 'circle', 'ellipse', 'text', 'eraser']
        for tool in tools:
            btn = QToolButton()
            btn.setIcon(self.icons.get(tool))
            btn.setText(tool.capitalize())
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setCheckable(True)
            btn.setStyleSheet("background-color: #7f8c8d; color: white; padding: 5px; border-radius: 5px;")
            if tool == 'pen':
                btn.setChecked(True)
                btn.setStyleSheet("background-color: #3498db; color: white; padding: 5px; border-radius: 5px;")
            btn.clicked.connect(lambda checked, t=tool: self.select_tool(t))
            tools_layout.addWidget(btn)
            self.tool_buttons[tool] = btn
        tools_group.setLayout(tools_layout)
        main_layout.addWidget(tools_group)

        # Settings group
        settings_group = QGroupBox("Settings")
        settings_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        settings_layout = QVBoxLayout()

        # Color
        color_layout = QHBoxLayout()
        color_label = QLabel("Color:")
        color_label.setFont(QFont("Segoe UI", 10))
        color_layout.addWidget(color_label)
        self.color_button = QPushButton()
        self.color_button.setFixedSize(40, 20)
        self.color_button.setStyleSheet(f"background-color: {self.current_color.name()}; border-radius: 3px;")
        self.color_button.clicked.connect(self.choose_color)
        color_layout.addStretch()
        color_layout.addWidget(self.color_button)
        settings_layout.addLayout(color_layout)

        # Size
        size_layout = QHBoxLayout()
        size_label = QLabel("Size:")
        size_label.setFont(QFont("Segoe UI", 10))
        size_layout.addWidget(size_label)
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(20)
        self.size_slider.setValue(self.brush_size)
        self.size_slider.valueChanged.connect(self.update_size)
        size_layout.addWidget(self.size_slider)
        self.size_value = QLabel(str(self.brush_size))
        self.size_value.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        size_layout.addWidget(self.size_value)
        settings_layout.addLayout(size_layout)

        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        # Actions group
        actions_group = QGroupBox("Actions")
        actions_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        actions_layout = QVBoxLayout()

        # Undo/Redo
        undo_redo_layout = QHBoxLayout()
        self.undo_btn = QPushButton("Undo")
        self.undo_btn.setIcon(self.icons.get('undo'))
        self.undo_btn.setStyleSheet("background-color: #95a5a6; color: white; font: 9pt 'Segoe UI'; padding: 5px; border-radius: 5px;")
        self.undo_btn.setEnabled(False)
        self.undo_btn.clicked.connect(self.undo)
        undo_redo_layout.addWidget(self.undo_btn)

        self.redo_btn = QPushButton("Redo")
        self.redo_btn.setIcon(self.icons.get('redo'))
        self.redo_btn.setStyleSheet("background-color: #95a5a6; color: white; font: 9pt 'Segoe UI'; padding: 5px; border-radius: 5px;")
        self.redo_btn.setEnabled(False)
        self.redo_btn.clicked.connect(self.redo)
        undo_redo_layout.addWidget(self.redo_btn)
        actions_layout.addLayout(undo_redo_layout)

        # Save
        save_btn = QPushButton("📸 Save Screenshot")
        save_btn.setStyleSheet("background-color: #9b59b6; color: white; font: bold 10pt 'Segoe UI'; padding: 8px; border-radius: 5px;")
        save_btn.clicked.connect(self.save_screenshot)
        actions_layout.addWidget(save_btn)

        actions_group.setLayout(actions_layout)
        main_layout.addWidget(actions_group)

        # Shortcuts
        shortcuts_group = QGroupBox("Keyboard Shortcuts")
        shortcuts_group.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        shortcuts_text = QTextEdit()
        shortcuts_text.setReadOnly(True)
        shortcuts_text.setPlainText("F1: Toggle overlay\nF2: Clear screen\nESC: Hide overlay\nCtrl+Z: Undo\nCtrl+Y: Redo")
        shortcuts_text.setFixedHeight(80)
        shortcuts_layout = QVBoxLayout()
        shortcuts_layout.addWidget(shortcuts_text)
        shortcuts_group.setLayout(shortcuts_layout)
        main_layout.addWidget(shortcuts_group)

    def select_tool(self, tool):
        for t, btn in self.tool_buttons.items():
            if t == tool:
                btn.setStyleSheet("background-color: #3498db; color: white; padding: 5px; border-radius: 5px;")
            else:
                btn.setStyleSheet("background-color: #7f8c8d; color: white; padding: 5px; border-radius: 5px;")
        self.current_tool = tool
        cursors = {
            'pen': Qt.CursorShape.CrossCursor,
            'rectangle': Qt.CursorShape.CrossCursor,
            'circle': Qt.CursorShape.CrossCursor,
            'ellipse': Qt.CursorShape.CrossCursor,
            'text': Qt.CursorShape.IBeamCursor,
            'eraser': Qt.CursorShape.PointingHandCursor
        }
        self.view.setCursor(cursors.get(tool, Qt.CursorShape.CrossCursor))

    def choose_color(self):
        color = QColorDialog.getColor(self.current_color, self.control_window, "Choose Color")
        if color.isValid():
            self.current_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()}; border-radius: 3px;")

    def update_size(self, value):
        self.brush_size = value
        self.size_value.setText(str(value))

    def toggle_overlay(self):
        if self.overlay_active:
            self.hide_overlay()
        else:
            self.show_overlay()

    def show_overlay(self):
        self.overlay.showFullScreen()
        self.overlay.raise_()
        self.overlay_active = True
        self.overlay_btn.setText("Hide Drawing")
        self.overlay_btn.setStyleSheet("background-color: #e67e22; color: white; font: bold 12pt 'Segoe UI'; padding: 10px; border-radius: 5px;")

    def hide_overlay(self):
        self.overlay.hide()
        self.overlay_active = False
        self.overlay_btn.setText("Start Drawing")
        self.overlay_btn.setStyleSheet("background-color: #27ae60; color: white; font: bold 12pt 'Segoe UI'; padding: 10px; border-radius: 5px;")

    def mousePressEvent(self, event):
        if not self.overlay_active:
            return
        if event.button() == Qt.MouseButton.LeftButton:
            pos = self.view.mapToScene(event.position().toPoint())
            pen = QPen(self.current_color, self.brush_size, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
            if self.current_tool == 'pen':
                self.current_path = QPainterPath()
                self.current_path.moveTo(pos)
                self.current_item = self.scene.addPath(self.current_path, pen)
            elif self.current_tool in ['rectangle', 'circle', 'ellipse']:
                self.start_pos = pos
            elif self.current_tool == 'text':
                text, ok = QInputDialog.getText(self.control_window, "Add Text", "Enter text:")
                if ok and text:
                    text_item = self.scene.addText(text, QFont('Arial', max(8, self.brush_size * 2)))
                    text_item.setDefaultTextColor(self.current_color)
                    text_item.setPos(pos)
                    self.drawings.append(text_item)
                    self.save_state()
            elif self.current_tool == 'eraser':
                self.save_state()
                self.erase_at(pos)
            self.drawing = True

    def mouseMoveEvent(self, event):
        if not self.overlay_active or not self.drawing:
            return
        pos = self.view.mapToScene(event.position().toPoint())
        pen = QPen(self.current_color, self.brush_size, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        if self.current_tool == 'pen':
            self.current_path.lineTo(pos)
            self.current_item.setPath(self.current_path)
        elif self.current_tool in ['rectangle', 'circle', 'ellipse']:
            if self.current_item:
                self.scene.removeItem(self.current_item)
            if self.current_tool == 'rectangle':
                rect = QRectF(self.start_pos, pos).normalized()
                self.current_item = self.scene.addRect(rect, pen)
            else:  # circle or ellipse
                rect = QRectF(self.start_pos, pos).normalized()
                if self.current_tool == 'circle':
                    dx = pos.x() - self.start_pos.x()
                    dy = pos.y() - self.start_pos.y()
                    size = max(abs(dx), abs(dy))
                    end_x = self.start_pos.x() + size * (1 if dx >= 0 else -1)
                    end_y = self.start_pos.y() + size * (1 if dy >= 0 else -1)
                    rect = QRectF(self.start_pos, QPointF(end_x, end_y)).normalized()
                self.current_item = self.scene.addEllipse(rect, pen)
        elif self.current_tool == 'eraser':
            self.erase_at(pos)

    def mouseReleaseEvent(self, event):
        if not self.overlay_active:
            return
        if event.button() == Qt.MouseButton.LeftButton and self.drawing:
            if self.current_tool in ['pen', 'rectangle', 'circle', 'ellipse']:
                if self.current_item:
                    self.drawings.append(self.current_item)
                    self.current_item = None
                self.save_state()
            self.current_path = None
            self.start_pos = None
            self.drawing = False

    def erase_at(self, pos):
        erase_rect = QRectF(pos.x() - self.brush_size, pos.y() - self.brush_size, self.brush_size * 2, self.brush_size * 2)
        colliding = self.scene.items(erase_rect)
        for item in colliding:
            self.scene.removeItem(item)
            if item in self.drawings:
                self.drawings.remove(item)

    def save_state(self):
        self.undo_stack.append(self.drawings.copy())
        self.redo_stack.clear()
        self.update_undo_redo_buttons()

    def undo(self):
        if self.undo_stack:
            current = self.drawings.copy()
            self.redo_stack.append(current)
            previous = self.undo_stack.pop()
            for item in list(self.drawings):
                if item not in previous:
                    self.scene.removeItem(item)
            for item in previous:
                if item not in self.drawings:
                    self.scene.addItem(item)
            self.drawings = previous
            self.update_undo_redo_buttons()

    def redo(self):
        if self.redo_stack:
            current = self.drawings.copy()
            self.undo_stack.append(current)
            previous = self.redo_stack.pop()
            for item in list(self.drawings):
                if item not in previous:
                    self.scene.removeItem(item)
            for item in previous:
                if item not in self.drawings:
                    self.scene.addItem(item)
            self.drawings = previous
            self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        self.undo_btn.setEnabled(bool(self.undo_stack))
        self.undo_btn.setStyleSheet("background-color: #3498db; color: white; font: 9pt 'Segoe UI'; padding: 5px; border-radius: 5px;" if self.undo_stack else "background-color: #95a5a6; color: white; font: 9pt 'Segoe UI'; padding: 5px; border-radius: 5px;")
        self.redo_btn.setEnabled(bool(self.redo_stack))
        self.redo_btn.setStyleSheet("background-color: #3498db; color: white; font: 9pt 'Segoe UI'; padding: 5px; border-radius: 5px;" if self.redo_stack else "background-color: #95a5a6; color: white; font: 9pt 'Segoe UI'; padding: 5px; border-radius: 5px;")

    def clear_screen(self):
        reply = QMessageBox.question(self.control_window, "Clear All", "Are you sure you want to clear all drawings?")
        if reply == QMessageBox.StandardButton.Yes:
            self.save_state()
            for item in list(self.drawings):
                self.scene.removeItem(item)
            self.drawings.clear()

    def save_screenshot(self):
        was_active = self.overlay_active
        if was_active:
            self.hide_overlay()
        QApplication.processEvents()
        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(0)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screen_annotation_{timestamp}.png"
        screenshot.save(filename, "png")
        QMessageBox.information(self.control_window, "Screenshot Saved", f"Screenshot saved as:\\n{filename}")
        if was_active:
            self.show_overlay()

    def key_press_event(self, event):
        if event.key() == Qt.Key.Key_F1:
            self.toggle_overlay()
        elif event.key() == Qt.Key.Key_F2:
            self.clear_screen()
        elif event.key() == Qt.Key.Key_Escape:
            self.hide_overlay()
        elif event.key() == Qt.Key.Key_Z and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.undo()
        elif event.key() == Qt.Key.Key_Y and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.redo()

    def run(self):
        self.control_window.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    app = ProfessionalScreenOverlay()
    app.run()
