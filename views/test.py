from PyQt5 import QtWidgets

app = QtWidgets.QApplication([])

scroll_area = QtWidgets.QScrollArea()
widget = QtWidgets.QWidget()

layout = QtWidgets.QVBoxLayout()
for i in range(50):
    label = QtWidgets.QLabel('Label {}'.format(i))
    layout.addWidget(label)

widget.setLayout(layout)
scroll_area.setWidget(widget)
scroll_area.show()

app.exec_()
