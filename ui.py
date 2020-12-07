# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 960)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(930, 0))
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(0, 211))
        self.frame.setObjectName("frame")

        self.list_view_bounding_boxes = QtWidgets.QListView(self.frame)
        self.list_view_bounding_boxes.setGeometry(QtCore.QRect(290, 30, 261, 181))
        self.list_view_bounding_boxes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_view_bounding_boxes.setObjectName("list_view_bounding_boxes")

        # self.class_view = QtWidgets.QTextEdit()
        # self.class_view.setObjectName("class_view")
        self.list_view_classes = QtWidgets.QListView(self.frame)
        self.list_view_classes.setGeometry(QtCore.QRect(1155, 30, 266, 181))
        # self.list_view_classes.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.list_view_classes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_view_classes.setObjectName("list_view_classes")

        self.label_1 = QtWidgets.QLabel(self.frame)
        self.label_1.setGeometry(QtCore.QRect(290, 0, 111, 21))
        self.label_1.setObjectName("label_1")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 91, 21))
        self.label.setObjectName("label")
        self.list_view_images = QtWidgets.QListView(self.frame)
        self.list_view_images.setGeometry(QtCore.QRect(0, 30, 271, 181))
        self.list_view_images.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_view_images.setObjectName("list_view_images")

        # image directory
        self.push_button_image_path = QtWidgets.QPushButton(self.frame)
        self.push_button_image_path.setGeometry(QtCore.QRect(230, 0, 21, 23))
        self.push_button_image_path.setObjectName("push_button_image_path")
        self.line_edit_image_path = QtWidgets.QLineEdit(self.frame)
        self.line_edit_image_path.setGeometry(QtCore.QRect(100, 0, 121, 21))
        self.line_edit_image_path.setObjectName("line_edit_image_path")

        # delete button
        self.push_button_delete = QtWidgets.QPushButton(self.frame)
        self.push_button_delete.setGeometry(QtCore.QRect(850, 90, 61, 31))
        self.push_button_delete.setObjectName("push_button_delete")

        # coco export button
        self.push_button_coco = QtWidgets.QPushButton(self.frame)
        self.push_button_coco.setGeometry(QtCore.QRect(850, 0, 61, 31))
        self.push_button_coco.setObjectName("push_button_coco")

        self.line_edit_x2 = QtWidgets.QLineEdit(self.frame)
        self.line_edit_x2.setGeometry(QtCore.QRect(650, 100, 71, 21))
        self.line_edit_x2.setObjectName("line_edit_x2")
        self.line_edit_y1 = QtWidgets.QLineEdit(self.frame)
        self.line_edit_y1.setGeometry(QtCore.QRect(740, 70, 71, 21))
        self.line_edit_y1.setObjectName("line_edit_y1")
        self.line_edit_label = QtWidgets.QLineEdit(self.frame)
        self.line_edit_label.setGeometry(QtCore.QRect(650, 170, 161, 20))
        self.line_edit_label.setObjectName("line_edit_label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(680, 20, 21, 21))
        self.label_2.setObjectName("label_2")
        self.line_edit_x3 = QtWidgets.QLineEdit(self.frame)
        self.line_edit_x3.setGeometry(QtCore.QRect(650, 130, 71, 21))
        self.line_edit_x3.setObjectName("line_edit_x3")
        self.line_edit_y0 = QtWidgets.QLineEdit(self.frame)
        self.line_edit_y0.setGeometry(QtCore.QRect(740, 40, 71, 21))
        self.line_edit_y0.setObjectName("line_edit_y0")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(590, 170, 41, 21))
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(590, 80, 41, 21))
        self.label_4.setObjectName("label_4")
        self.line_edit_y2 = QtWidgets.QLineEdit(self.frame)
        self.line_edit_y2.setGeometry(QtCore.QRect(740, 100, 71, 21))
        self.line_edit_y2.setObjectName("line_edit_y2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(770, 20, 21, 21))
        self.label_3.setObjectName("label_3")
        self.line_edit_x1 = QtWidgets.QLineEdit(self.frame)
        self.line_edit_x1.setGeometry(QtCore.QRect(650, 70, 71, 21))
        self.line_edit_x1.setObjectName("line_edit_x1")
        self.line_edit_x0 = QtWidgets.QLineEdit(self.frame)
        self.line_edit_x0.setGeometry(QtCore.QRect(650, 40, 71, 21))
        self.line_edit_x0.setObjectName("line_edit_x0")
        self.line_edit_y3 = QtWidgets.QLineEdit(self.frame)
        self.line_edit_y3.setGeometry(QtCore.QRect(740, 130, 71, 21))
        self.line_edit_y3.setObjectName("line_edit_y3")

        self.check_box_selection_mode = QtWidgets.QCheckBox(self.frame)
        self.check_box_selection_mode.setGeometry(QtCore.QRect(1040, 175, 81, 21))
        self.check_box_selection_mode.setObjectName("check_box_selection_mode")

        self.check_box_modify_mode = QtWidgets.QCheckBox(self.frame)
        self.check_box_modify_mode.setGeometry(QtCore.QRect(1040, 155, 81, 21))
        self.check_box_modify_mode.setObjectName("check_box_modify_mode")

        self.horizontalLayout_1.addWidget(self.frame)
        self.verticalLayout_4.addLayout(self.horizontalLayout_1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.graphics_view = GraphicsView(self.centralwidget)
        self.graphics_view.setMouseTracking(True)
        self.graphics_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphics_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.graphics_view.setObjectName("graphics_view")
        self.horizontalLayout_4.addWidget(self.graphics_view)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_1.setText(_translate("MainWindow", "Bounding Boxes"))
        self.label.setText(_translate("MainWindow", "이미지파일 경로"))
        self.push_button_image_path.setText(_translate("MainWindow", "..."))
        self.push_button_delete.setText(_translate("MainWindow", "삭제"))
        self.push_button_coco.setText(_translate("MainWindow", "COCO"))

        self.label_2.setText(_translate("MainWindow", "x"))
        self.label_5.setText(_translate("MainWindow", "Label"))
        self.label_4.setText(_translate("MainWindow", "Points"))
        self.label_3.setText(_translate("MainWindow", "y"))
        self.check_box_selection_mode.setText(_translate("MainWindow", "선택모드"))
        self.check_box_modify_mode.setText(_translate("MainWindow", "수정모드"))


from graphicsview import GraphicsView

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

