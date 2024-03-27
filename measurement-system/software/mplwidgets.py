
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# custom toolbar with lorem ipsum text
class ToolbarWidget(NavigationToolbar):
	def __init__(self, canvas_, parent_=None):
		self.toolitems = (
		('Home', 'Reset original view', 'home', 'home'),
		#('Back', 'Back to  previous view', 'back', 'back'),
		#('Forward', 'Forward to next view', 'forward', 'forward'),
		('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
		('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
		('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
		#('Save', 'Save the figure', 'filesave', 'save_figure'),
		)
		NavigationToolbar.__init__(self, canvas_, parent_)


class PlotWidget(QWidget):
	"""docstring for MplWidget"""
	def __init__(self, parent = None):
		super(PlotWidget, self).__init__()
		
		self.vertical_layout = QVBoxLayout()
		self.canvas = FigureCanvas(plt.Figure(dpi=100, facecolor="#fff"))
		self.toolbar = ToolbarWidget(self.canvas, parent)

		self.vertical_layout.addWidget(self.canvas)
		self.vertical_layout.addWidget(self.toolbar)

		self.vertical_layout.setAlignment(self.toolbar, Qt.AlignBaseline | Qt.AlignRight)
		self.vertical_layout.setSpacing(0)
		self.vertical_layout.setContentsMargins(0, 0, 0, 0)

		self.canvas.axes = self.canvas.figure.add_subplot(111, facecolor="#000")

		self.setLayout(self.vertical_layout)
