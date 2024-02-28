from matplotlib.figure import Figure 
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class MplWidget(QWidget):
	"""docstring for MplWidget"""
	def __init__(self, parent = None):
		super(MplWidget, self).__init__()
		
		self.vertical_layout = QVBoxLayout()
		self.canvas = FigureCanvas(Figure(dpi=100, facecolor="#f0f0f0"))
		self.toolbar = NavigationToolbar(self.canvas, parent)

		self.vertical_layout.addWidget(self.canvas)
		self.vertical_layout.addWidget(self.toolbar)

		self.canvas.axes = self.canvas.figure.add_subplot(111, facecolor="#000")

		self.setLayout(self.vertical_layout)