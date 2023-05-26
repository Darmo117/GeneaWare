import sys

import PyQt5.QtWidgets as QtW
import PyQt5.QtGui as QtG

app = QtW.QApplication(sys.argv)

filter_ = sys.argv[1] if len(sys.argv) > 1 else ''
w = QtW.QWidget()
layout = QtW.QVBoxLayout()
list_ = QtW.QListWidget(parent=w)
with open('fd_icons.txt') as f:
    for icon_name in f.readlines():
        if filter_ and filter_ not in icon_name:
            continue
        name = icon_name.strip()
        list_.addItem(QtW.QListWidgetItem(QtG.QIcon.fromTheme(name), name, parent=list_))
layout.addWidget(list_)
w.setLayout(layout)
w.show()

sys.exit(app.exec_())
