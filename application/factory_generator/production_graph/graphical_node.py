from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject, QStyleOptionGraphicsItem, QWidget



class GraphicalNode(QGraphicsObject):

    def __init__(self, name: str, label: str, label_color: str, color = None, parent=None):
        super().__init__(parent)
        self._name = name
        self._edges = []
        self._color = color
        self._radius = 40
        self._rect = QRectF(0, 0, self._radius * 2, self._radius * 2)
        self._shape = "s"
        self.label = label
        self.label_color = label_color

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.CacheMode.DeviceCoordinateCache)

    def boundingRect(self) -> QRectF:
        return self._rect

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget = None):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(
            QPen(
                QColor(self._color).darker(),
                2.0,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
                Qt.PenJoinStyle.RoundJoin,
            )
        )
        painter.setBrush(QBrush(QColor(self._color)))
        painter.drawEllipse(self.boundingRect())
        painter.setPen(QPen(QColor("white")))
        font = painter.font()
        font.setPointSize(8)  # Increase font size here
        painter.setFont(font)
        painter.setPen(QColor(self.label_color))
        painter.drawText(self.boundingRect(), Qt.AlignmentFlag.AlignCenter, self.label)

    def add_edge(self, edge):
        self._edges.append(edge)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for edge in self._edges:
                edge.adjust()

        return super().itemChange(change, value)
