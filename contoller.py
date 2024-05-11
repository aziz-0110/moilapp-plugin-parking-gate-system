from src.plugin_interface import PluginInterface
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QMessageBox
from src.models.model_apps import ModelApps
from .ui_main import Ui_Form
import cv2

# from moildev import Moildev

class Controller(QWidget):
    def __init__(self, model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.model_apps = ModelApps()
        # self.moildev = Moildev()
        self.img_fisheye = None
        self.img_pano = None
        self.img_gate_in = None
        self.img_gate_out = None
        self.gate = 0
        self.pano_alpha_max = 180
        self.pano_alpha = 150
        self.pano_beta = 0
        self.pano_left = 0.25
        self.pano_right = 0.75
        self.pano_top = 0
        self.pano_buttom = 1
        self.maps_any_g1_alpha = 30
        self.maps_any_g1_beta = 180
        self.maps_any_g1_zoom = 2
        self.maps_any_g2_alpha = -40
        self.maps_any_g2_beta = 180
        self.maps_any_g2_zoom = 2
        self.set_stylesheet()

    def set_stylesheet(self):
        # This is set up style label on bonding box ui
        # self.ui.label_7.setStyleSheet(self.model.style_label())
        # self.ui.label_8.setStyleSheet(self.model.style_label())
        # self.ui.label_10.setStyleSheet(self.model.style_label())
        # self.ui.label_9.setStyleSheet(self.model.style_label())
        # self.ui.label_13.setStyleSheet(self.model.style_label())
        # self.ui.label_14.setStyleSheet(self.model.style_label())

        self.ui.vidio_fisheye.setStyleSheet(self.model.style_label())
        self.ui.vidio_pano.setStyleSheet(self.model.style_label())
        self.ui.vidio_gate_in.setStyleSheet(self.model.style_label())
        self.ui.vidio_gate_out.setStyleSheet(self.model.style_label())
        # self.ui.img_plat.setStyleSheet(self.model.style_label())

        self.ui.btn_save.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_stop.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_start.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_params_cam.setStyleSheet(self.model.style_pushbutton())

        self.ui.frame_4.setStyleSheet(self.model.style_frame_main())
        self.ui.frame_3.setStyleSheet(self.model.style_frame_main())

        self.ui.frame_12.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_11.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_10.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_5.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_7.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_13.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_15.setStyleSheet(self.model.style_frame_object())
        self.ui.frame_19.setStyleSheet(self.model.style_frame_object())

        self.ui.line.setStyleSheet(self.model.style_line())
        self.ui.line_2.setStyleSheet(self.model.style_line())
        self.ui.line_6.setStyleSheet(self.model.style_line())
        self.ui.line_4.setStyleSheet(self.model.style_line())
        self.ui.line_5.setStyleSheet(self.model.style_line())

        self.ui.frame_14.setMaximumSize(QtCore.QSize(16777215, 23))
        self.ui.frame_mode1.setMaximumSize(QtCore.QSize(16777215, 23))
        self.ui.frame_mode1_2.setMaximumSize(QtCore.QSize(16777215, 23))
        self.ui.frame_mode2.setMaximumSize(QtCore.QSize(16777215, 23))
        self.ui.frame_mode2_2.setMaximumSize(QtCore.QSize(16777215, 23))

        # panorama view
        self.ui.spinBox_alpha_max.setRange(-999, 999)
        self.ui.spinBox_alpha_4.setRange(-999, 999)
        self.ui.spinBox_beta_1.setRange(-999, 999)
        self.ui.spinBox_left_1.setRange(0, 1)
        self.ui.spinBox_right_1.setRange(0, 1)
        self.ui.spinBox_top_1.setRange(0, 1)
        self.ui.spinBox_bottom_4.setRange(0, 1)

        self.ui.spinBox_alpha_max.setValue(self.pano_alpha_max)
        self.ui.spinBox_alpha_4.setValue(self.pano_alpha)
        self.ui.spinBox_beta_1.setValue(self.pano_beta)
        self.ui.spinBox_left_1.setValue(self.pano_left)
        self.ui.spinBox_right_1.setValue(self.pano_right)
        self.ui.spinBox_top_1.setValue(self.pano_top)
        self.ui.spinBox_bottom_4.setValue(self.pano_buttom)
        # self.ui.spinBox_rotate_4.valueChanged.connect(self.value_change_pano)

        # gate in view
        self.ui.spinBox_alpha_2.setRange(-999, 999)
        self.ui.spinBox_beta_2.setRange(-999, 999)
        self.ui.spinBox_zoom_2.setRange(1, 100)
        self.ui.spinBox_rotate_2.setRange(1, 4)

        self.ui.spinBox_alpha_2.setValue(self.maps_any_g1_alpha)
        self.ui.spinBox_beta_2.setValue(self.maps_any_g1_beta)
        self.ui.spinBox_zoom_2.setValue(self.maps_any_g1_zoom)
        # self.ui.spinBox_rotate_2.setValue(self.)


        self.ui.line_2.hide()
        self.ui.line_6.hide()
        self.ui.frame_23.hide()
        self.ui.frame_25.hide()
        self.ui.frame_24.hide()
        # self.ui.frame_mode1.hide()
        # self.ui.frame_mode2.hide()
        # self.ui.frame_mode1_2.hide()
        # self.ui.frame_mode2_2.hide()

        self.ui.btn_radio_hidden.toggled.connect(self.change_mode)
        self.ui.btn_radio_mode1.toggled.connect(self.change_mode)
        self.ui.btn_radio_mode2.toggled.connect(self.change_mode)

        self.ui.btn_start.clicked.connect(self.start)

        self.value_connect_pano()
        self.value_connect_maps_any_m1()
        # self.ui.spinBox_alpha_1.setStyleSheet(self.model.)

        # if self.ui.btn_radio_mode1.isChecked():
        #     QMessageBox.information(self, "tes,", f"aa")
        # else:
        #     QMessageBox.information(self, "tes,", f"bb")

    def value_connect_pano(self):
        self.ui.spinBox_alpha_max.valueChanged.connect(self.value_change_pano)
        self.ui.spinBox_alpha_4.valueChanged.connect(self.value_change_pano)
        self.ui.spinBox_beta_1.valueChanged.connect(self.value_change_pano)
        self.ui.spinBox_left_1.valueChanged.connect(self.value_change_pano)
        self.ui.spinBox_right_1.valueChanged.connect(self.value_change_pano)
        self.ui.spinBox_top_1.valueChanged.connect(self.value_change_pano)
        self.ui.spinBox_bottom_4.valueChanged.connect(self.value_change_pano)
        # rotate blm fix
        self.ui.spinBox_rotate_4.valueChanged.connect(self.value_change_pano)

    def value_connect_maps_any_m1(self):
        # seperti ini juga bisa, bedanya ini langsung mengambil dinilai dari spinbox
        # self.ui.spinBox_alpha_2.valueChanged.connect(lambda value: self.tes("aa", value))
        # self.ui.spinBox_alpha_2.valueChanged.connect(self.value_change_maps_any_m1)
        self.ui.spinBox_beta_2.valueChanged.connect(self.value_change_maps_any_m1)
        # zoom blm fix
        self.ui.spinBox_zoom_2.valueChanged.connect(self.value_change_maps_any_m1)
        self.ui.spinBox_rotate_2.valueChanged.connect(self.value_change_maps_any_m1)

        self.ui.spinBox_alpha_3.valueChanged.connect(self.value_change_maps_any_m1)
        self.ui.spinBox_beta_3.valueChanged.connect(self.value_change_maps_any_m1)
        # zoom blm fix
        self.ui.spinBox_zoom_3.valueChanged.connect(self.value_change_maps_any_m1)
        self.ui.spinBox_rotate_3.valueChanged.connect(self.value_change_maps_any_m1)

    def tes(self, aa, bb):
        print(bb)

    def change_mode(self):
        if self.ui.btn_radio_mode1.isChecked():
            mode = 1
            self.ui.line_2.show()
            self.ui.line_6.show()
            self.ui.frame_23.show()
            self.ui.frame_mode1.show()
            self.ui.frame_mode1_2.show()

            self.ui.frame_24.show()
            self.ui.frame_25.show()

            self.ui.frame_mode2.hide()
            self.ui.frame_mode2_2.hide()
        elif self.ui.btn_radio_mode2.isChecked():
            mode = 2
            self.ui.line_2.show()
            self.ui.line_6.show()
            self.ui.frame_23.show()
            self.ui.frame_mode2.show()
            self.ui.frame_mode2_2.show()

            self.ui.frame_24.show()
            self.ui.frame_25.show()

            self.ui.frame_mode1.hide()
            self.ui.frame_mode1_2.hide()
        else:
            mode = 0
            self.ui.frame_24.hide()
            self.ui.frame_25.hide()
            self.ui.frame_23.hide()

    def start(self):
        source_type, cam_type, source_media, parameter_name = self.model.select_media_source()
        self.img_fisheye = cv2.imread(source_media)
        self.img_pano = self.img_fisheye.copy()
        self.img_gate_in = self.img_fisheye.copy()
        self.img_gate_out = self.img_fisheye.copy()
        self.moildev = self.model.connect_to_moildev(parameter_name)
        # self.image = cv2.imread('/home/gritz/Documents/ftdc/moilapp/moilapp-pak-heru/src/fisheye.png')

        self.pano_car()
        self.anypoint_m1()

        self.showImg()

    def showImg(self):
        self.model.show_image_to_label(self.ui.vidio_pano, self.img_pano, 944)
        self.model.show_image_to_label(self.ui.vidio_gate_in, self.img_gate_in, 480)
        self.model.show_image_to_label(self.ui.vidio_gate_out, self.img_gate_out, 480)

        self.model.show_image_to_label(self.ui.vidio_fisheye, self.img_fisheye, 280)

    def value_change_pano(self):
        self.pano_alpha_max = self.ui.spinBox_alpha_max.value()
        self.pano_alpha = self.ui.spinBox_alpha_4.value()
        self.pano_beta = self.ui.spinBox_beta_1.value()
        self.pano_left = self.ui.spinBox_left_1.value()
        self.pano_right = self.ui.spinBox_right_1.value()
        self.pano_top = self.ui.spinBox_top_1.value()
        self.pano_buttom = self.ui.spinBox_bottom_4.value()

        self.img_pano = self.img_fisheye.copy()

        self.pano_car()

        self.model.show_image_to_label(self.ui.vidio_pano, self.img_pano, 944)

    def value_change_maps_any_m1(self):
        self.maps_any_g1_alpha = self.ui.spinBox_alpha_2.value()
        self.maps_any_g1_beta = self.ui.spinBox_zoom_2.value()
        self.maps_any_g1_zoom = self.ui.spinBox_zoom_2.value()
        self.maps_any_g2_alpha = self.ui.spinBox_alpha_3.value()
        self.maps_any_g2_beta = self.ui.spinBox_beta_3.value()
        self.maps_any_g2_zoom = self.ui.spinBox_zoom_3.value()

        self.img_gate_in = self.img_fisheye.copy()
        self.img_gate_out = self.img_fisheye.copy()

        self.anypoint_m1()
        # cv2.imshow("a", self.img_gate_in)
        self.model.show_image_to_label(self.ui.vidio_gate_in, self.img_gate_in, 480)
        # self.model.show_image_to_label(self.ui.vidio_gate_out, self.img_gate_out, 480)

    def pano_car(self):
        # alpa max = bisa +/-, alpa = +/-, beta = +/-, left = +/-, right = -, top = -, button = -
        self.img_pano = self.moildev.panorama_car(self.img_pano, self.pano_alpha_max, self.pano_alpha, self.pano_beta, self.pano_left, self.pano_right, self.pano_top, self.pano_buttom)
        # self.image = cv2.resize(self.image, ())
        self.img_pano = cv2.resize(self.img_pano, (900,300))

    def anypoint_m1(self):
        # self.img_gate_in = self.moildev.anypoint_mode1(self.img_gate_in, 90, 180, 2)
        x_in, y_in = self.moildev.maps_anypoint_mode1(self.maps_any_g1_beta, self.maps_any_g1_beta, self.maps_any_g1_zoom)
        self.img_gate_in = cv2.remap(self.img_gate_in, x_in, y_in, cv2.INTER_CUBIC)

        # x_out, y_out = self.moildev.maps_anypoint_mode1(self.maps_any_g2_beta, self.maps_any_g2_beta, self.maps_any_g2_zoom)
        # self.img_gate_out = cv2.remap(self.img_gate_out, x_out, y_out, cv2.INTER_CUBIC)
        # self.img_gate_out = self.img_rotate(self.img_gate_out)

    def img_rotate(self, img):
        # rotate = self.ui.spinBox_2.value()
        h, w = img.shape[:2]
        center = (w / 2, h / 2)

        # rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=rotate, scale=1)
        rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=180, scale=1)

        # rotate the image using cv2.warpAffine
        return cv2.warpAffine(src=img, M=rotate_matrix, dsize=(w, h))

    def load_image(self):
        file = self.model.select_file()
        if file:
            if file:
                self.moildev = self.model.connect_to_moildev(parameter_name=file)
            self.image_original = cv2.imread(file)
            self.image = self.image_original.copy()
            # self.panorma_views()
            self.show_to_ui()



class ParkingGateSystem(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "This is a plugins application"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon.png"

    def change_stylesheet(self):
        self.widget.set_stylesheet()

