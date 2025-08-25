import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSlider, QToolButton, QColorDialog, QInputDialog, QGraphicsView,
    QGraphicsScene, QGroupBox, QMessageBox, QFrame, QFileDialog
)
from PyQt6.QtCore import Qt, QPointF, QRectF, QSizeF
from PyQt6.QtGui import (
    QPen, QPainterPath, QColor, QFont, QPalette, QGuiApplication, QIcon,
    QBrush, QPainter, QPixmap, QBrush
)
from PyQt6.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPathItem, QGraphicsItem, QStyleOptionGraphicsItem

# ---------- Custom Graphics Items with Handles ----------
HANDLE_SIZE = 8.0

class ResizeHandle(QGraphicsRectItem):
    """Small square handle used to resize parent shape."""
    def __init__(self, x, y, parentShape, role):
        # role: 'tl','tr','bl','br' or 'start','end' for lines
        super().__init__(-HANDLE_SIZE/2, -HANDLE_SIZE/2, HANDLE_SIZE, HANDLE_SIZE, parent=parentShape)
        self.setBrush(QBrush(QColor(255, 255, 255)))
        self.setPen(QPen(QColor(0,0,0)))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True)
        self.role = role
        self.parentShape = parentShape
        self.setPos(x, y)
        # easier to pick with larger area
        self.setZValue(1000)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            new_scene_pos = self.mapToScene(value)
            self.parentShape.handle_moved(self.role, new_scene_pos)
            return self.pos()
        return super().itemChange(change, value)


class AnnotShape:
    """Mixin/utility wrapper to keep track of shape and its handles"""
    pass


class RectShape(QGraphicsRectItem):
    def __init__(self, rect: QRectF, pen: QPen):
        super().__init__(rect)
        self.setPen(pen)
        self.setBrush(Qt.BrushStyle.NoBrush)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.handles = {}
        self.create_handles()

    def create_handles(self):
        rect = self.rect()
        tl = rect.topLeft()
        tr = rect.topRight()
        bl = rect.bottomLeft()
        br = rect.bottomRight()
        self.handles.clear()
        self.handles['tl'] = ResizeHandle(tl.x(), tl.y(), self, 'tl')
        self.handles['tr'] = ResizeHandle(tr.x(), tr.y(), self, 'tr')
        self.handles['bl'] = ResizeHandle(bl.x(), bl.y(), self, 'bl')
        self.handles['br'] = ResizeHandle(br.x(), br.y(), self, 'br')
        self.set_handles_visible(False)

    def set_handles_visible(self, visible: bool):
        for h in list(self.handles.values()):
            h.setVisible(visible)

    def handle_moved(self, role, scene_pos):
        # calculate new rect in scene coordinates and update shape
        parent = self
        s = parent.scene()
        # map scene_pos to parent's local coordinates
        local = parent.mapFromScene(scene_pos)
        r = QRectF(parent.rect())
        if role == 'tl':
            r.setTopLeft(local)
        elif role == 'tr':
            r.setTopRight(local)
        elif role == 'bl':
            r.setBottomLeft(local)
        elif role == 'br':
            r.setBottomRight(local)
        # normalize and set
        r = r.normalized()
        parent.prepareGeometryChange()
        parent.setRect(r)
        # reposition handles
        rect = parent.rect()
        parent.handles['tl'].setPos(rect.topLeft())
        parent.handles['tr'].setPos(rect.topRight())
        parent.handles['bl'].setPos(rect.bottomLeft())
        parent.handles['br'].setPos(rect.bottomRight())

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget):
        super().paint(painter, option, widget)
        # show handles if selected
        self.set_handles_visible(self.isSelected())


class EllipseShape(QGraphicsEllipseItem):
    def __init__(self, rect: QRectF, pen: QPen):
        super().__init__(rect)
        self.setPen(pen)
        self.setBrush(Qt.BrushStyle.NoBrush)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.handles = {}
        self.create_handles()

    def create_handles(self):
        rect = self.rect()
        tl = rect.topLeft(); tr = rect.topRight(); bl = rect.bottomLeft(); br = rect.bottomRight()
        self.handles.clear()
        self.handles['tl'] = ResizeHandle(tl.x(), tl.y(), self, 'tl')
        self.handles['tr'] = ResizeHandle(tr.x(), tr.y(), self, 'tr')
        self.handles['bl'] = ResizeHandle(bl.x(), bl.y(), self, 'bl')
        self.handles['br'] = ResizeHandle(br.x(), br.y(), self, 'br')
        self.set_handles_visible(False)

    def set_handles_visible(self, visible: bool):
        for h in list(self.handles.values()):
            h.setVisible(visible)

    def handle_moved(self, role, scene_pos):
        local = self.mapFromScene(scene_pos)
        r = QRectF(self.rect())
        if role == 'tl':
            r.setTopLeft(local)
        elif role == 'tr':
            r.setTopRight(local)
        elif role == 'bl':
            r.setBottomLeft(local)
        elif role == 'br':
            r.setBottomRight(local)
        r = r.normalized()
        self.prepareGeometryChange()
        self.setRect(r)
        rect = self.rect()
        self.handles['tl'].setPos(rect.topLeft())
        self.handles['tr'].setPos(rect.topRight())
        self.handles['bl'].setPos(rect.bottomLeft())
        self.handles['br'].setPos(rect.bottomRight())

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget):
        super().paint(painter, option, widget)
        self.set_handles_visible(self.isSelected())


class LineShape(QGraphicsLineItem):
    def __init__(self, line, pen: QPen, arrow=False):
        super().__init__(line)
        self.setPen(pen)
        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.handles = {}
        self.arrow = arrow
        self.create_handles()

    def create_handles(self):
        line = self.line()
        p1 = line.p1(); p2 = line.p2()
        self.handles.clear()
        self.handles['start'] = ResizeHandle(p1.x(), p1.y(), self, 'start')
        self.handles['end'] = ResizeHandle(p2.x(), p2.y(), self, 'end')
        self.set_handles_visible(False)

    def set_handles_visible(self, visible: bool):
        for h in list(self.handles.values()):
            h.setVisible(visible)

    def handle_moved(self, role, scene_pos):
        local = self.mapFromScene(scene_pos)
        ln = self.line()
        if role == 'start':
            ln.setP1(local)
        else:
            ln.setP2(local)
        self.prepareGeometryChange()
        self.setLine(ln)
        # reposition handles
        self.handles['start'].setPos(self.line().p1())
        self.handles['end'].setPos(self.line().p2())

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget):
        super().paint(painter, option, widget)
        # custom arrowhead if arrow flag is True
        if self.arrow:
            # draw simple triangle arrow at end
            p1 = self.line().p1()
            p2 = self.line().p2()
            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            length = (dx*dx + dy*dy) ** 0.5
            if length > 0.001:
                ux, uy = dx/length, dy/length
                # base of arrow
                arrow_size = max(8.0, self.pen().widthF()*3)
                left = QPointF(p2.x() - ux*arrow_size - uy*(arrow_size/2),
                               p2.y() - uy*arrow_size + ux*(arrow_size/2))
                right = QPointF(p2.x() - ux*arrow_size + uy*(arrow_size/2),
                                p2.y() - uy*arrow_size - ux*(arrow_size/2))
                path = QPainterPath()
                path.moveTo(p2)
                path.lineTo(left)
                path.lineTo(right)
                path.closeSubpath()
                painter.setBrush(self.pen().color())
                painter.drawPath(path)
        self.set_handles_visible(self.isSelected())


# ---------- Main Application ----------
class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent, overlay_instance):
        super().__init__(parent)
        self.overlay_instance = overlay_instance
        self.setStyleSheet("background: transparent")
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

        # Dark theme palette
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(44, 62, 80))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(52, 73, 94))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(44, 62, 80))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Button, QColor(52, 73, 94))
        palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        self.app.setPalette(palette)

        # Drawing state
        self.current_color = QColor(255, 0, 0)
        self.brush_size = 3
        self.current_tool = "pen"
        self.overlay_active = False

        # Load icons (if any)
        self.icons = {}
        self.load_icons()

        # Setup control window
        self.control_window = QWidget()
        self.control_window.setWindowTitle("MADIrwx Screen Annotator")
        self.control_window.setFixedSize(1600, 180)
        self.control_window.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        screen_geometry = QGuiApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.control_window.width()) // 2
        y = (screen_geometry.height() - self.control_window.height()) // 2
        self.control_window.move(x, y)
        self.control_window.closeEvent = self.closeEvent

        self.setup_professional_ui()

        # Create overlay (fullscreen transparent widget)
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

        # drawing variables
        self.drawing = False
        self.start_pos = None
        self.current_path = None
        self.current_item = None
        self.drawings = []  # list of QGraphicsItem (shapes)
        self.undo_stack = []
        self.redo_stack = []

        # Bind keyboard shortcuts
        self.control_window.keyPressEvent = self.key_press_event
        self.overlay.keyPressEvent = self.key_press_event

        # initial message
        QMessageBox.information(self.control_window, "Professional Screen Annotator",
                                "Welcome!\n\nHotkeys: P=Pen, R=Rect, O=Ellipse, C=Circle, L=Line, A=Arrow, S=Select, E=Eraser, T=Text\nF1 Toggle overlay, F2 Clear, Del Delete selection, Ctrl+Z Undo, Ctrl+Y Redo")

    def load_icons(self):
        icon_files = {
            'pen': 'pen.png', 'rectangle': 'rectangle.png', 'circle': 'circle.png', 'ellipse': 'ellipse.png',
            'text': 'text.png', 'eraser': 'eraser.png', 'undo': 'undo.png', 'redo': 'redo.png', 'delete': 'eraser.png',
            'line': 'line.png', 'arrow': 'arrow.png', 'select': 'move.png', 'export': 'export.png'
        }
        icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
        for tool, filename in icon_files.items():
            icon_path = os.path.join(icons_dir, filename)
            if os.path.exists(icon_path):
                self.icons[tool] = QIcon(icon_path)
            else:
                self.icons[tool] = QIcon()

    def setup_professional_ui(self):
        main_layout = QHBoxLayout(self.control_window)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Left - header & actions
        left_section = QVBoxLayout()
        header = QLabel("Screen Annotator Pro")
        header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_section.addWidget(header)

        btn_layout = QHBoxLayout()
        self.overlay_btn = QPushButton("Start Drawing")
        self.overlay_btn.setFixedSize(140, 40)
        self.overlay_btn.setStyleSheet("background-color: #27ae60; color: white; font: bold 10pt 'Segoe UI';")
        self.overlay_btn.clicked.connect(self.toggle_overlay)
        btn_layout.addWidget(self.overlay_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.setFixedSize(120, 40)
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white; font: bold 10pt 'Segoe UI';")
        clear_btn.clicked.connect(self.clear_screen)
        btn_layout.addWidget(clear_btn)

        left_section.addLayout(btn_layout)
        main_layout.addLayout(left_section)

        # Tools
        tools_group = QGroupBox("Tools")
        tools_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        tools_layout = QHBoxLayout()
        tools = ['pen', 'rectangle', 'circle', 'ellipse', 'line', 'arrow', 'text', 'select', 'eraser']
        self.tool_buttons = {}
        for t in tools:
            btn = QToolButton()
            btn.setIcon(self.icons.get(t))
            btn.setText(t.capitalize())
            # btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, tool=t: self.select_tool(tool))
            btn.setFixedSize(80, 80)
            tools_layout.addWidget(btn)
            self.tool_buttons[t] = btn
        # default pen
        self.tool_buttons['pen'].setChecked(True); self.tool_buttons['pen'].setStyleSheet("background:#3498db;color:white")
        tools_group.setLayout(tools_layout)
        main_layout.addWidget(tools_group)

        # Right - settings and actions
        right_section = QVBoxLayout()

        # color + size + opacity + export + delete + undo/redo
        settings_row = QHBoxLayout()
        settings_row.addWidget(QLabel("Color:"))
        self.color_button = QPushButton()
        self.color_button.setFixedSize(30, 22)
        self.color_button.setStyleSheet(f"background-color: {self.current_color.name()};")
        self.color_button.clicked.connect(self.choose_color)
        settings_row.addWidget(self.color_button)

        settings_row.addWidget(QLabel("Size:"))
        self.size_slider = QSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(1); self.size_slider.setMaximum(30); self.size_slider.setValue(self.brush_size)
        self.size_slider.setFixedWidth(90)
        self.size_slider.valueChanged.connect(self.update_size)
        settings_row.addWidget(self.size_slider)
        self.size_label = QLabel(str(self.brush_size)); settings_row.addWidget(self.size_label)

        settings_row.addWidget(QLabel("Overlay Opacity:"))
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setMinimum(10); self.opacity_slider.setMaximum(100); self.opacity_slider.setValue(100)
        self.opacity_slider.setFixedWidth(120)
        self.opacity_slider.valueChanged.connect(self.update_opacity)
        settings_row.addWidget(self.opacity_slider)

        right_section.addLayout(settings_row)

        action_row = QHBoxLayout()
        self.undo_btn = QPushButton("Undo"); self.undo_btn.setIcon(self.icons.get('undo')); self.undo_btn.clicked.connect(self.undo); self.undo_btn.setEnabled(False)
        self.redo_btn = QPushButton("Redo"); self.redo_btn.setIcon(self.icons.get('redo')); self.redo_btn.clicked.connect(self.redo); self.redo_btn.setEnabled(False)
        self.delete_btn = QPushButton("Delete"); self.delete_btn.setIcon(self.icons.get('delete')); self.delete_btn.clicked.connect(self.delete_selected)
        self.export_btn = QPushButton("Export"); self.export_btn.setIcon(self.icons.get('export')); self.export_btn.clicked.connect(self.export_image)
        action_row.addWidget(self.undo_btn); action_row.addWidget(self.redo_btn); action_row.addWidget(self.delete_btn); action_row.addWidget(self.export_btn)

        right_section.addLayout(action_row)

        main_layout.addLayout(right_section)

    # ---------- UI helper methods ----------
    def select_tool(self, tool):
        for t, btn in self.tool_buttons.items():
            if t == tool:
                btn.setStyleSheet("background:#3498db;color:white")
                btn.setChecked(True)
            else:
                btn.setStyleSheet("")
                btn.setChecked(False)
        self.current_tool = tool
        cursors = {
            'pen': Qt.CursorShape.CrossCursor,
            'rectangle': Qt.CursorShape.CrossCursor,
            'circle': Qt.CursorShape.CrossCursor,
            'ellipse': Qt.CursorShape.CrossCursor,
            'text': Qt.CursorShape.IBeamCursor,
            'eraser': Qt.CursorShape.PointingHandCursor,
            'line': Qt.CursorShape.CrossCursor,
            'arrow': Qt.CursorShape.CrossCursor,
            'select': Qt.CursorShape.ArrowCursor
        }
        self.view.setCursor(cursors.get(tool, Qt.CursorShape.CrossCursor))

    def choose_color(self):
        color = QColorDialog.getColor(self.current_color, self.control_window, "Choose Color")
        if color.isValid():
            self.current_color = color
            self.color_button.setStyleSheet(f"background-color: {color.name()};")

    def update_size(self, v):
        self.brush_size = v
        self.size_label.setText(str(v))

    def update_opacity(self, v):
        self.overlay.setWindowOpacity(v / 100.0)

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
        self.overlay_btn.setStyleSheet("background-color:#e67e22;color:white")

    def hide_overlay(self):
        self.overlay.hide()
        self.overlay_active = False
        self.overlay_btn.setText("Start Drawing")
        self.overlay_btn.setStyleSheet("background-color:#27ae60;color:white")

    # ---------- Mouse event handling (centralized) ----------
    def mousePressEvent(self, event):
        if not self.overlay_active:
            return
        if event.button() != Qt.MouseButton.LeftButton:
            return
        pos = self.view.mapToScene(event.position().toPoint())
        pen = QPen(self.current_color, max(1, self.brush_size), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)

        if self.current_tool == 'pen':
            self.current_path = QPainterPath()
            self.current_path.moveTo(pos)
            self.current_item = QGraphicsPathItem(self.current_path)
            self.current_item.setPen(pen)
            self.scene.addItem(self.current_item)
            self.drawings.append(self.current_item)
            self.save_state()
            self.drawing = True

        elif self.current_tool in ('rectangle', 'circle', 'ellipse'):
            self.start_pos = pos
            self.drawing = True
            # create a placeholder item (will be replaced while dragging)
            rect = QRectF(pos, QSizeF(1,1))
            if self.current_tool == 'rectangle':
                item = RectShape(rect, pen)
            else:
                item = EllipseShape(rect, pen)
            self.current_item = item
            self.scene.addItem(item)

        elif self.current_tool in ('line', 'arrow'):
            self.start_pos = pos
            self.drawing = True
            line = QGraphicsLineItem(pos.x(), pos.y(), pos.x(), pos.y())
            if self.current_tool == 'arrow':
                # use our LineShape with arrow flag
                item = LineShape(line.line(), pen, arrow=True)
            else:
                item = LineShape(line.line(), pen, arrow=False)
            self.current_item = item
            self.scene.addItem(item)

        elif self.current_tool == 'text':
            text, ok = QInputDialog.getText(self.control_window, "Add Text", "Enter text:")
            if ok and text:
                text_item = self.scene.addText(text, QFont('Arial', max(8, self.brush_size * 2)))
                text_item.setDefaultTextColor(self.current_color)
                text_item.setPos(pos)
                text_item.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable | QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
                self.drawings.append(text_item)
                self.save_state()

        elif self.current_tool == 'select':
            # default QGraphics handles selection; nothing special here
            pass

        elif self.current_tool == 'eraser':
            # remove items at point (skip handles)
            self.save_state()
            items = self.scene.items(QRectF(pos.x()-self.brush_size, pos.y()-self.brush_size, self.brush_size*2, self.brush_size*2))
            for it in items:
                # skip handles
                if isinstance(it, ResizeHandle):
                    continue
                # avoid removing control window etc.
                try:
                    self.scene.removeItem(it)
                    if it in self.drawings:
                        self.drawings.remove(it)
                except Exception:
                    pass

    def mouseMoveEvent(self, event):
        if not self.overlay_active or not self.drawing:
            return
        pos = self.view.mapToScene(event.position().toPoint())
        pen = QPen(self.current_color, max(1, self.brush_size), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)

        if self.current_tool == 'pen' and self.current_item:
            path: QPainterPath = self.current_item.path()
            path.lineTo(pos)
            self.current_item.setPath(path)

        elif self.current_tool in ('rectangle', 'circle', 'ellipse'):
            if not self.current_item:
                return
            rect = QRectF(self.start_pos, pos).normalized()
            if self.current_tool == 'rectangle':
                self.current_item.setRect(rect)
                # reposition handles (they are managed in class)
                r = self.current_item.rect()
                for role, h in self.current_item.handles.items():
                    if role == 'tl': h.setPos(r.topLeft())
                    if role == 'tr': h.setPos(r.topRight())
                    if role == 'bl': h.setPos(r.bottomLeft())
                    if role == 'br': h.setPos(r.bottomRight())
            else:
                # circle or ellipse
                if self.current_tool == 'circle':
                    dx = pos.x() - self.start_pos.x()
                    dy = pos.y() - self.start_pos.y()
                    size = max(abs(dx), abs(dy))
                    end_x = self.start_pos.x() + size * (1 if dx >= 0 else -1)
                    end_y = self.start_pos.y() + size * (1 if dy >= 0 else -1)
                    rect = QRectF(self.start_pos, QPointF(end_x, end_y)).normalized()
                self.current_item.setRect(rect)
                r = self.current_item.rect()
                for role, h in self.current_item.handles.items():
                    if role == 'tl': h.setPos(r.topLeft())
                    if role == 'tr': h.setPos(r.topRight())
                    if role == 'bl': h.setPos(r.bottomLeft())
                    if role == 'br': h.setPos(r.bottomRight())

        elif self.current_tool in ('line', 'arrow'):
            if not self.current_item:
                return
            ln = self.current_item.line()
            ln.setP2(pos)
            self.current_item.setLine(ln)
            # reposition handles
            self.current_item.handles['start'].setPos(ln.p1())
            self.current_item.handles['end'].setPos(ln.p2())

        elif self.current_tool == 'eraser':
            pos = self.view.mapToScene(event.position().toPoint())
            items = self.scene.items(QRectF(pos.x()-self.brush_size, pos.y()-self.brush_size, self.brush_size*2, self.brush_size*2))
            for it in items:
                if isinstance(it, ResizeHandle):
                    continue
                try:
                    self.scene.removeItem(it)
                    if it in self.drawings:
                        self.drawings.remove(it)
                except Exception:
                    pass

    def mouseReleaseEvent(self, event):
        if not self.overlay_active:
            return
        if event.button() != Qt.MouseButton.LeftButton:
            return
        if not self.drawing:
            return

        if self.current_tool == 'pen':
            if self.current_item:
                self.drawings.append(self.current_item)
                self.current_item = None
                self.save_state()

        elif self.current_tool in ('rectangle', 'circle', 'ellipse'):
            if self.current_item:
                # replace placeholder with shape class if it's not yet that class
                if isinstance(self.current_item, (RectShape, EllipseShape)):
                    self.drawings.append(self.current_item)
                else:
                    self.scene.removeItem(self.current_item)
                self.current_item = None
                self.save_state()

        elif self.current_tool in ('line', 'arrow'):
            if self.current_item:
                # ensure we use LineShape which has handles
                if isinstance(self.current_item, LineShape):
                    self.drawings.append(self.current_item)
                else:
                    self.scene.removeItem(self.current_item)
                self.current_item = None
                self.save_state()

        self.drawing = False
        self.start_pos = None
        self.current_path = None

    # ---------- Erase / Delete / Clear ----------
    def erase_at(self, pos):
        # not used; we integrated eraser in mouse handlers
        pass

    def delete_selected(self):
        # remove selected items (skip handles)
        self.save_state()
        for it in list(self.scene.selectedItems()):
            # skip handles
            if isinstance(it, ResizeHandle):
                parent = it.parentItem()
                # if handle selected maybe delete parent instead
                continue
            try:
                self.scene.removeItem(it)
                if it in self.drawings:
                    self.drawings.remove(it)
            except Exception:
                pass

    def clear_screen(self):
        reply = QMessageBox.question(self.control_window, "Clear All", "Are you sure you want to clear all drawings?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.save_state()
            for item in list(self.drawings):
                try:
                    self.scene.removeItem(item)
                except Exception:
                    pass
            self.drawings.clear()

    # ---------- Undo/Redo (basic snapshot by item list) ----------
    def save_state(self):
        # Save shallow copies of existing items (we store references; for robust deep snapshots you'd serialize)
        snapshot = list(self.drawings)
        self.undo_stack.append(snapshot)
        if len(self.undo_stack) > 50:
            self.undo_stack.pop(0)
        self.redo_stack.clear()
        self.update_undo_redo_buttons()

    def undo(self):
        if not self.undo_stack:
            return
        current = list(self.drawings)
        self.redo_stack.append(current)
        prev = self.undo_stack.pop()
        # clear scene of current drawables and re-add prev
        for it in list(self.drawings):
            try:
                self.scene.removeItem(it)
            except Exception:
                pass
        self.drawings = []
        for it in prev:
            # if the item still belongs to scene we re-add; if not, we add a copy? For simplicity try to re-add
            self.scene.addItem(it)
            self.drawings.append(it)
        self.update_undo_redo_buttons()

    def redo(self):
        if not self.redo_stack:
            return
        current = list(self.drawings)
        self.undo_stack.append(current)
        prev = self.redo_stack.pop()
        for it in list(self.drawings):
            try:
                self.scene.removeItem(it)
            except Exception:
                pass
        self.drawings = []
        for it in prev:
            self.scene.addItem(it)
            self.drawings.append(it)
        self.update_undo_redo_buttons()

    def update_undo_redo_buttons(self):
        self.undo_btn.setEnabled(bool(self.undo_stack))
        self.redo_btn.setEnabled(bool(self.redo_stack))

    # ---------- Export ----------
    def export_image(self):
        # Render scene to QPixmap
        rect = self.scene.sceneRect()
        img = QPixmap(int(rect.width()), int(rect.height()))
        img.fill(Qt.GlobalColor.transparent)
        painter = QPainter(img)
        self.scene.render(painter)
        painter.end()

        path, _ = QFileDialog.getSaveFileName(self.control_window, "Export Image", os.path.expanduser("~"), "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)")
        if path:
            # choose format by extension
            if path.lower().endswith(('.jpg', '.jpeg')):
                img.save(path, 'JPEG', quality=92)
            else:
                img.save(path, 'PNG')

    # ---------- Key handling ----------
    def key_press_event(self, event):
        # global hotkeys mapping
        key = event.key()
        mods = event.modifiers()
        if key == Qt.Key.Key_F1:
            self.toggle_overlay()
        elif key == Qt.Key.Key_F2:
            self.clear_screen()
        elif key == Qt.Key.Key_Escape:
            self.hide_overlay()
        elif key == Qt.Key.Key_P:
            self.select_tool('pen')
        elif key == Qt.Key.Key_R:
            self.select_tool('rectangle')
        elif key == Qt.Key.Key_O:
            self.select_tool('ellipse')
        elif key == Qt.Key.Key_C:
            self.select_tool('circle')  # treated like circle not same as ellipse; depending on UI mapping
        elif key == Qt.Key.Key_L:
            self.select_tool('line')
        elif key == Qt.Key.Key_A:
            self.select_tool('arrow')
        elif key == Qt.Key.Key_S:
            self.select_tool('select')
        elif key == Qt.Key.Key_E:
            self.select_tool('eraser')
        elif key == Qt.Key.Key_T:
            self.select_tool('text')
        elif key == Qt.Key.Key_Delete:
            self.delete_selected()
        elif key == Qt.Key.Key_Z and mods & Qt.KeyboardModifier.ControlModifier:
            self.undo()
        elif key == Qt.Key.Key_Y and mods & Qt.KeyboardModifier.ControlModifier:
            self.redo()

    def closeEvent(self, event):
        if self.overlay.isVisible():
            self.overlay.close()
        self.app.quit()

    def run(self):
        self.control_window.show()
        sys.exit(self.app.exec())


if __name__ == "__main__":
    app = ProfessionalScreenOverlay()
    app.run()
