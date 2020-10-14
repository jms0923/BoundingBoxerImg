import sys, os, re
from PyQt5 import QtWidgets, QtCore, QtGui

from gt2coco import cocoExport
import ui

class MainWindow(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlag(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.image_path = ""
        self.gt_path = ""
        self.push_button_image_path.clicked.connect(self.get_image_path)
        self.push_button_delete.clicked.connect(self.delete_current_bounding_box)
        self.push_button_coco.clicked.connect(self.cocoExport)
        self.line_edit_image_path.returnPressed.connect(self.image_path_changed)
        self.line_edit_x0.returnPressed.connect(self.modify_current_bounding_box)
        self.line_edit_y0.returnPressed.connect(self.modify_current_bounding_box)
        self.line_edit_x1.returnPressed.connect(self.modify_current_bounding_box)
        self.line_edit_y1.returnPressed.connect(self.modify_current_bounding_box)
        self.line_edit_x2.returnPressed.connect(self.modify_current_bounding_box)
        self.line_edit_y2.returnPressed.connect(self.modify_current_bounding_box)
        self.line_edit_x3.returnPressed.connect(self.modify_current_bounding_box)
        self.line_edit_y3.returnPressed.connect(self.modify_current_bounding_box)
        self.line_edit_label.returnPressed.connect(self.modify_current_bounding_box)
        self.check_box_selection_mode.clicked.connect(self.selection_mode_changed)
        self.model_images = QtGui.QStandardItemModel()
        self.list_view_images.setModel(self.model_images)
        self.list_view_images.selectionModel().currentRowChanged.connect(self.image_selected)

        self.model_bounding_boxes = QtGui.QStandardItemModel()
        self.list_view_bounding_boxes.setModel(self.model_bounding_boxes)
        self.list_view_bounding_boxes.selectionModel().currentRowChanged.connect(self.bounding_box_selected)

        self.model_classes = QtGui.QStandardItemModel()
        self.list_view_classes.setModel(self.model_classes)

        self.graphics_scene = GraphicsScene(self.graphics_view)
        self.graphics_view.setScene(self.graphics_scene)
        self.bounding_boxes = []
        self.bounding_labels = []

        self.line_edit_label.installEventFilter(self)

        self.shortCut = [QtCore.Qt.Key_F1, QtCore.Qt.Key_F2, QtCore.Qt.Key_F3, QtCore.Qt.Key_F4, QtCore.Qt.Key_F5, QtCore.Qt.Key_F6, QtCore.Qt.Key_F7, QtCore.Qt.Key_F8, QtCore.Qt.Key_F9, QtCore.Qt.Key_F10, QtCore.Qt.Key_F11, QtCore.Qt.Key_F12]
        self.classes = []
        self.get_classes()
        self.class_view_init()

    def get_classes(self):
        classFilePath = 'classes.txt'
        if os.path.exists(classFilePath):
            with open(classFilePath, 'r') as lines:
                for line in lines:
                    self.classes.append(line.split('\n')[0])
        self.shortCut = self.shortCut[:len(self.classes)] if len(self.shortCut) > len(self.classes) else self.shortCut

    def get_image_path(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select image path"))
        if path:
            self.line_edit_image_path.setText(path)
            self.image_path_changed()

    def image_path_changed(self):
        self.image_path = self.line_edit_image_path.text()
        files = [f for f in os.listdir(self.image_path) if re.match(r'.+\.(jpg|png|JPG|PNG|jpeg|JPEG)', f)]
        self.model_images.clear()
        for f in files:
            self.model_images.appendRow(QtGui.QStandardItem(f))

        self.gt_path = os.path.join(self.image_path, "gt")
        os.makedirs(self.gt_path, exist_ok=True)

        self.graphics_scene.clear()
        self.model_bounding_boxes.clear()
        self.bounding_boxes.clear()
        self.bounding_labels.clear()
        self.line_edit_x0.setText("")
        self.line_edit_y0.setText("")
        self.line_edit_x1.setText("")
        self.line_edit_y1.setText("")
        self.line_edit_x2.setText("")
        self.line_edit_y2.setText("")
        self.line_edit_x3.setText("")
        self.line_edit_y3.setText("")
        self.line_edit_label.setText("")

    def save_gt(self):
        image_name = self.model_images.data(self.list_view_images.currentIndex())
        gt_name = "gt_{}.txt".format(os.path.splitext(image_name)[0])
        with open(os.path.join(self.gt_path, gt_name), 'w', newline='\n', encoding='utf-8') as fp:
            gt_string = ["{},{}".format(','.join((str(bb) for bb in b[0])), b[1]) for b in self.bounding_boxes]
            fp.write('\n'.join(gt_string))

    def class_view_init(self):
        for idx, cls in enumerate(self.classes):
            explan = 'F' + str(idx+1) + ' / ' + cls
            self.model_classes.appendRow(QtGui.QStandardItem(explan))

    def cocoExport(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle('coco export')
        msg.setText('Are you really want to convert data from now to COCO format?')
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel|QtWidgets.QMessageBox.Ok)
        resut = msg.exec_()
        if resut == QtWidgets.QMessageBox.Ok:
            cocoExport(self.line_edit_image_path.text(), self.classes)

    def image_selected(self):
        index = self.list_view_images.currentIndex().row()
        if index < 0: return
        image_name = self.model_images.data(self.list_view_images.currentIndex())
        image = os.path.join(self.image_path, image_name)
        self.graphics_scene.clear()
        pixmap = QtGui.QPixmap(image)
        pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        pixmap_item.setZValue(-1)
        pixmap_qrectf = QtCore.QRectF(0, 0, pixmap.size().width(), pixmap.size().height())
        self.graphics_scene.setSceneRect(pixmap_qrectf)
        self.graphics_scene.addItem(pixmap_item)
        self.graphics_view.resetTransform()
        fit_to_view = min(self.graphics_view.size().width() / pixmap.size().width(),
                          self.graphics_view.size().height() / pixmap.size().height())
        self.graphics_view.scale(fit_to_view, fit_to_view)

        self.model_bounding_boxes.clear()
        self.bounding_boxes.clear()
        self.bounding_labels.clear()
        gt_name = "gt_{}.txt".format(os.path.splitext(image_name)[0])
        if os.path.exists(os.path.join(self.gt_path, gt_name)):
            with open(os.path.join(self.gt_path, gt_name), 'r', encoding='utf-8') as fp:
                for line in fp:
                    line = line.split(',')
                    points = [int(x) for x in line[:8]]
                    self.graphics_scene.from_gt(points, line[-1].split('\n')[0])
                    self.bounding_boxes.append((points, line[8].strip()))
                    self.bounding_labels.append(line[-1].split('\n')[0])

        for b in self.bounding_boxes:
            self.model_bounding_boxes.appendRow(QtGui.QStandardItem("{},{}".format(','.join((str(bb) for bb in b[0])), b[1])))

        self.select_bounding_box_index(0)

    def poly_added(self, poly):
        index = self.list_view_images.currentIndex().row()
        if index < 0:
            self.graphics_scene.remove_poly(0)
            return
        points = [int(poly[0].x()), int(poly[0].y()),
                  int(poly[1].x()), int(poly[1].y()),
                  int(poly[2].x()), int(poly[2].y()),
                  int(poly[3].x()), int(poly[3].y()),]
        self.bounding_boxes.append((points, ""))
        self.model_bounding_boxes.appendRow(QtGui.QStandardItem("{},{}".format(','.join((str(bb) for bb in points)), "")))
        self.select_bounding_box_index(len(self.bounding_boxes) - 1)
        self.save_gt()

    def delete_current_bounding_box(self):
        index = self.list_view_bounding_boxes.currentIndex().row()
        if index < 0: return
        self.model_bounding_boxes.removeRow(index)
        del self.bounding_boxes[index]
        self.graphics_scene.remove_poly(index)
        self.save_gt()

    def bounding_box_selected(self):
        index = self.list_view_bounding_boxes.currentIndex().row()
        if index < 0:
            self.line_edit_x0.setText("")
            self.line_edit_y0.setText("")
            self.line_edit_x1.setText("")
            self.line_edit_y1.setText("")
            self.line_edit_x2.setText("")
            self.line_edit_y2.setText("")
            self.line_edit_x3.setText("")
            self.line_edit_y3.setText("")
            self.line_edit_label.setText("")
        else:
            bb, label = self.bounding_boxes[index]
            self.line_edit_x0.setText(str(bb[0]))
            self.line_edit_y0.setText(str(bb[1]))
            self.line_edit_x1.setText(str(bb[2]))
            self.line_edit_y1.setText(str(bb[3]))
            self.line_edit_x2.setText(str(bb[4]))
            self.line_edit_y2.setText(str(bb[5]))
            self.line_edit_x3.setText(str(bb[6]))
            self.line_edit_y3.setText(str(bb[7]))
            self.line_edit_label.setText(label)
            self.graphics_scene.set_bounding_box_focused(index)
            
        self.line_edit_label.setFocus()

    def modify_current_bounding_box(self):
        index = self.list_view_bounding_boxes.currentIndex().row()
        if index < 0: return
        bbs = [int(self.line_edit_x0.text()),
               int(self.line_edit_y0.text()),
               int(self.line_edit_x1.text()),
               int(self.line_edit_y1.text()),
               int(self.line_edit_x2.text()),
               int(self.line_edit_y2.text()),
               int(self.line_edit_x3.text()),
               int(self.line_edit_y3.text()),]
        label = self.line_edit_label.text()
        self.bounding_boxes[index] = (bbs, label)
        item = self.model_bounding_boxes.itemFromIndex(self.list_view_bounding_boxes.currentIndex())
        item.setText("{},{}".format(','.join((str(bb) for bb in bbs)), label))
        self.graphics_scene.modify_poly(index, bbs, label)
        self.save_gt()
        self.select_bounding_box_index(index + 1)

    def selection_mode_changed(self, checked):
        self.graphics_scene.selection_mode = checked

    def shortCutAction(self, key):
        idx = self.shortCut.index(key)
        self.line_edit_label.setText(self.classes[idx])
        self.modify_current_bounding_box()

    def keyPressEvent(self, event):
        nowKey = event.key()
        if nowKey == QtCore.Qt.Key_Delete:
            self.delete_current_bounding_box()
        elif nowKey in self.shortCut:
            self.shortCutAction(nowKey)

        return super().keyPressEvent(event)

    def select_bounding_box_index(self, index):
        if index < 0 or index >= len(self.bounding_boxes): return
        listview_index = self.model_bounding_boxes.index(index, 0)
        self.list_view_bounding_boxes.selectionModel().select(listview_index, QtCore.QItemSelectionModel.ClearAndSelect)
        self.list_view_bounding_boxes.setCurrentIndex(listview_index)

    def eventFilter(self, QObject, event):
        if QObject == self.line_edit_label:
            if event.type() == QtCore.QEvent.KeyPress:
                keyevent = QtGui.QKeyEvent(event)
                if keyevent.key() == QtCore.Qt.Key_Delete:
                    self.delete_current_bounding_box()
                elif keyevent.key() == QtCore.Qt.Key_Up:
                    index = self.list_view_bounding_boxes.currentIndex().row()
                    self.select_bounding_box_index(index - 1)
                elif keyevent.key() == QtCore.Qt.Key_Down:
                    index = self.list_view_bounding_boxes.currentIndex().row()
                    self.select_bounding_box_index(index + 1)
                    
        return super().eventFilter(QObject, event)


class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, view, parent=None):
        super().__init__(QtCore.QRectF(0, 0, 1280, 720), parent)
        self.view = view
        self.window = view.parent().parent()
        self.poly_list = []
        self.label_list = []
        self.current_poly = None
        self.current_poly_size = None
        self.current_focused = None
        self.current_focused_label = None
        self.current_horizontal_line = None
        self.current_vertical_line = None
        self.selection_mode = False

    def clear(self):
        self.poly_list.clear()
        self.label_list.clear()
        self.current_poly = None
        self.current_poly_size = None
        self.current_focused = None
        self.current_focused_label = None
        self.current_horizontal_line = None
        self.current_vertical_line = None
        return super().clear()

    def labelMaker(self, points, label):
        labelItem = QtWidgets.QGraphicsTextItem(label)
        font = labelItem.font()
        font.setPointSize(20)
        labelItem.setDefaultTextColor(QtGui.QColor('black'))
        labelItem.setFont(font)
        labelItem.setX(points[0]-5)
        labelItem.setY(points[1]-30)
        self.addItem(labelItem)
        self.label_list.append(labelItem)

    def from_gt(self, points, label):
        self.labelMaker(points, label)
        points = [QtCore.QPointF(points[2 * x], points[2 * x + 1]) for x in range(0, 4)]
        poly = QtGui.QPolygonF(points)
        self.poly_list.append(self.addPolygon(poly, pen=QtGui.QPen(QtCore.Qt.green, 1.5)))

    def remove_poly(self, index):
        self.removeItem(self.poly_list[index])
        self.removeItem(self.label_list[index])
        del self.poly_list[index]
        del self.label_list[index]

    def modify_poly(self, index, points, label):
        points = [QtCore.QPointF(points[2 * x], points[2 * x + 1]) for x in range(0, 4)]
        self.poly_list[index].setPolygon(QtGui.QPolygonF(points))
        self.label_list[index].setPlainText(label)

    def set_bounding_box_focused(self, index):
        if self.current_focused:
            self.current_focused.setPen(QtGui.QPen(QtCore.Qt.green, 1.5))
            self.current_focused_label.setDefaultTextColor(QtGui.QColor('black'))
        self.poly_list[index].setPen(QtGui.QPen(QtCore.Qt.red, 1.5))
        self.label_list[index].setDefaultTextColor(QtGui.QColor('red'))
        self.current_focused = self.poly_list[index]
        self.current_focused_label = self.label_list[index]
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and not self.current_poly and not self.selection_mode:
            self.current_poly_begin = event.scenePos()
            r = QtCore.QRectF(self.current_poly_begin, self.current_poly_begin)
            self.current_poly = self.addPolygon(QtGui.QPolygonF(r), pen=QtGui.QPen(QtCore.Qt.green, 1.5))
            self.current_poly.setZValue(1)
            self.current_poly_size = self.addSimpleText("(0 x 0)")
            self.current_poly_size.setPos(event.scenePos() - QtCore.QPointF(0, 11))
            self.current_poly_size.setBrush(QtGui.QBrush(QtCore.Qt.gray))

        if event.button() == QtCore.Qt.LeftButton and self.selection_mode:
            items = self.items(event.scenePos())
            for item in items:
                if item in self.poly_list:
                    self.window.select_bounding_box_index(self.poly_list.index(item))
                    break

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton and self.current_poly and not self.selection_mode:
            r = QtCore.QRectF(self.current_poly_begin, event.scenePos()).normalized()
            self.current_poly.setPolygon(QtGui.QPolygonF(r))

            self.current_poly_size.setPos(event.scenePos() - QtCore.QPointF(0, 11))
            self.current_poly_size.setText(f"({int(r.width())} x {int(r.height())})")

        if event.buttons() & QtCore.Qt.RightButton:
            delta = event.lastScreenPos() - event.screenPos()
            x = self.view.horizontalScrollBar().value() + delta.x()
            y = self.view.verticalScrollBar().value() + delta.y()
            self.view.horizontalScrollBar().setValue(x)
            self.view.verticalScrollBar().setValue(y)

        x = event.scenePos().x()
        y = event.scenePos().y()
        scene_min = self.view.mapToScene(0, 0)
        scene_max = self.view.mapToScene(self.view.width(), self.view.height())
        x_min = scene_min.x()
        y_min = scene_min.y()
        x_max = scene_max.x()
        y_max = scene_max.y()

        if not self.current_vertical_line:
            self.current_vertical_line = self.addLine(x, y_min, x, y_max, QtGui.QPen(QtCore.Qt.gray, 1))
            self.current_vertical_line.setZValue(0.5)
        else:
            self.current_vertical_line.setLine(x, y_min, x, y_max)
        if not self.current_horizontal_line:
            self.current_horizontal_line = self.addLine(x_min, y, x_max, y, QtGui.QPen(QtCore.Qt.gray, 1))
            self.current_horizontal_line.setZValue(0.5)
        else:
            self.current_horizontal_line.setLine(x_min, y, x_max, y)

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.current_poly and not self.selection_mode:
            self.poly_list.append(self.current_poly)
            self.labelMaker([0, 0], '')
            self.window.poly_added(self.current_poly.polygon())
            self.current_poly = None

            self.removeItem(self.current_poly_size)
            del self.current_poly_size

        return super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
