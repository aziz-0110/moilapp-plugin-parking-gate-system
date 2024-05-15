from src.plugin_interface import PluginInterface
from PyQt6 import QtCore
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QMessageBox
from src.models.model_apps import ModelApps
from .ui_main import Ui_Form
import cv2

# from moildev import Moildev

class Controller(QWidget):
    def _init_(self, model):
        super()._init_()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        self.model_apps = ModelApps()
        # self.moildev = Moildev()
        self.panorama = None
        self.gate_in = None
        self.gate_out = None
        self.moildev = None
        self.x = 0
        self.pitch = -90
        self.yaw = 0
        self.roll = 0
        self.zoom = 2
        self.pitch_2 = 0
        self.yaw_2= 0
        self.roll_2 = 0
        self.zoom_2 = 0
        self.set_stylesheet()
        self.image_fisheye = None

    def set_stylesheet(self):
        # This is set up style label on bonding box ui
        self.ui.label_7.setStyleSheet(self.model.style_label())
        self.ui.label_8.setStyleSheet(self.model.style_label())
        self.ui.label_10.setStyleSheet(self.model.style_label())
        self.ui.label_9.setStyleSheet(self.model.style_label())
        self.ui.label_13.setStyleSheet(self.model.style_label())
        self.ui.label_14.setStyleSheet(self.model.style_label())

        self.ui.vidio_fisheye.setStyleSheet(self.model.style_label())
        self.ui.vidio_pano.setStyleSheet(self.model.style_label())
        self.ui.Gate_In.setStyleSheet(self.model.style_label())
        self.ui.Gate_Out.setStyleSheet(self.model.style_label())
        # self.ui.img_plat.setStyleSheet(self.model.style_label())

        self.ui.btn_save.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_stop.setStyleSheet(self.model.style_pushbutton())
        self.ui.btn_start.setStyleSheet(self.model.style_pushbutton())

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

        self.ui.frame_14.setMaximumSize(QtCore.QSize(16777215, 23))
        self.ui.frame_mode1.setMaximumSize(QtCore.QSize(16777215, 23))
        self.ui.frame_mode1_2.setMaximumSize(QtCore.QSize(16777215, 23))
        self.ui.frame_mode2.setMaximumSize(QtCore.QSize(16777215, 23))
        self.ui.frame_mode2_2.setMaximumSize(QtCore.QSize(16777215, 23))

        self.ui.frame_14.hide()
        self.ui.frame_mode1.hide()
        self.ui.frame_mode2.hide()
        self.ui.frame_mode1_2.hide()
        self.ui.frame_mode2_2.hide()

        self.ui.btn_radio_hidden.toggled.connect(self.change_mode)
        self.ui.btn_radio_mode1.toggled.connect(self.change_mode)
        self.ui.btn_radio_mode2.toggled.connect(self.change_mode)

        self.ui.spinBox_alpha_5.setRange(-999,999)
        self.ui.spinBox_beta_4.setRange(-999, 999)
        self.ui.spinBox_x_5.setRange(-999,999)
        self.ui.spinBox_x_6.setRange(-999,999)
        self.ui.spinBox_x_6.setValue(2)

        self.ui.spinBox_alpha_6.setRange(-999, 999)
        self.ui.spinBox_beta_5.setRange(-999, 999)
        self.ui.spinBox_x_7.setRange(-999, 999)
        self.ui.spinBox_x_8.setRange(-999, 999)
        self.ui.spinBox_x_8.setValue(2)


        self.ui.btn_start.clicked.connect(self.start)

        # self.ui.spinBox_alpha_1.setStyleSheet(self.model.)

        #spinbox mode 1 Gate_In
        self.ui.spinBox_alpha_2.valueChanged.connect(self.anypoint_mode_1)
        self.ui.spinBox_beta_2.valueChanged.connect(self.anypoint_mode_1)
        self.ui.spinBox_x_2.valueChanged.connect(self.anypoint_mode_1)


        #Spinbox mode 2 Gate_In
        self.ui.spinBox_alpha_5.valueChanged.connect(self.anypoint_mode_2)
        self.ui.spinBox_beta_4.valueChanged.connect(self.anypoint_mode_2)
        self.ui.spinBox_x_5.valueChanged.connect(self.anypoint_mode_2)
        self.ui.spinBox_x_6.valueChanged.connect(self.anypoint_mode_2)

        #Spinbox mode 2 Gate_out
        self.ui.spinBox_alpha_6.valueChanged.connect(self.anypoint_mode_2)
        self.ui.spinBox_beta_5.valueChanged.connect(self.anypoint_mode_2)
        self.ui.spinBox_x_7.valueChanged.connect(self.anypoint_mode_2)
        self.ui.spinBox_x_8.valueChanged.connect(self.anypoint_mode_2)





    def start(self):
        source_type, cam_type, source_media, parameter_name = self.model.select_media_source()
        self.image_fisheye = cv2.imread(source_media)
        self.gate_out = self.image_fisheye.copy()
        self.gate_in = self.image_fisheye.copy()
        self.moildev = self.model.connect_to_moildev(parameter_name)
        # self.image = cv2.imread('/home/gritz/Documents/ftdc/moilapp/moilapp-pak-heru/src/fisheye.png')
      #self.image = self.moildev.panorama_car(self.panorama, 180, 80, 0, 0.25, 0.75, 0, 1)
        self.showImg()

#  def pano(self):
        #lpabeta_max = self.ui.spinBox_alpha_1.value()

        # self.moildev = self.model.connect_to_moildev(parameter_name)
      # self.panorama = self.moildev.panorama_car(self.panorama, alpabeta_max, 80, 0, 0.25, 0.75, 0, 1)
       #self.showImg()###

    def anypoint_mode_1(self):
        alpha = self.ui.spinBox_alpha_2.value()
        beta = self.ui.spinBox_beta_2.value()
        zoom_mode_1 = self.ui.spinBox_x_2.value()
        self.image_mode_1 = self.moildev.anypoint_mode1(self.gate_in,alpha,beta,zoom_mode_1)
        self.showImg()

    def anypoint_mode_2(self):
        self.gate_in = self.image_fisheye.copy()
        self.pitch = self.ui.spinBox_alpha_5.value()
        self.yaw = self.ui.spinBox_beta_4.value()
        self.roll = self.ui.spinBox_x_5.value()
        self.zoom = self.ui.spinBox_x_6.value()
        map_x,map_y = self.moildev.maps_anypoint_mode2(self.pitch, self.yaw, self.roll, self.zoom)
        self.gate_in = cv2.remap(self.gate_in, map_x, map_y, cv2.INTER_CUBIC)

        self.gate_out = self.image_fisheye.copy()
        self.pitch_2 = self.ui.spinBox_alpha_6.value()
        self.yaw_2 = self.ui.spinBox_beta_5.value()
        self.roll_2 = self.ui.spinBox_x_7.value()
        self.zoom_2 = self.ui.spinBox_x_8.value()
        map_x,map_y= self.moildev.maps_anypoint_mode2(self.pitch_2, self.yaw_2, self.roll_2, self.zoom_2)
        self.gate_out = cv2.remap(self.gate_out,map_x,map_y,cv2.INTER_CUBIC)
        self.showImg()

    def change_mode(self):
        if self.ui.btn_radio_mode1.isChecked():
            mode = 1
            self.ui.frame_14.show()
            self.ui.frame_mode1.show()
            self.ui.frame_mode1_2.show()

            self.ui.frame_mode2.hide()
            self.ui.frame_mode2_2.hide()
        elif self.ui.btn_radio_mode2.isChecked():
            mode = 2
            self.ui.frame_14.show()
            self.ui.frame_mode2.show()
            self.ui.frame_mode2_2.show()

            self.ui.frame_mode1.hide()
            self.ui.frame_mode1_2.hide()
        else:
            mode = 0
            self.ui.frame_14.hide()
            self.ui.frame_mode1.hide()
            self.ui.frame_mode1_2.hide()
            self.ui.frame_mode2.hide()
            self.ui.frame_mode2_2.hide()


        # file = self.model.select_file()
        # if file:
      #     # if file:
        #     #     self.image=
        #     self.image = cv2.imread(source_media)
        #     self.showImg()

    def showImg(self):
        self.model.show_image_to_label(self.ui.Gate_In,self.gate_in,720)
        self.model.show_image_to_label(self.ui.Gate_Out,self.gate_out,720)









        # height, width, channel = self.image_1.shape
        # bytesPerLine = 3 * width
        # qImg_1 = QImage(self.image_1.data, width, height, bytesPerLine, QImage.Format.Format_BGR888)
        # scaled_qImg_1 = qImg_1.scaled(self.ui.Gate_In.width(), self.ui.Gate_In.height())
        # self.ui.Gate_In.setPixmap(QPixmap.fromImage(scaled_qImg_1))
        #
        # # Menyiapkan gambar untuk Gate_Out
        # height, width, channel = self.image_2.shape
        # bytesPerLine = 3 * width
        # qImg_2 = QImage(self.image_2.data, width, height, bytesPerLine, QImage.Format.Format_BGR888)
        # scaled_qImg_2 = qImg_2.scaled(self.ui.Gate_Out.width(), self.ui.Gate_Out.height())
        # self.ui.Gate_Out.setPixmap(QPixmap.fromImage(scaled_qImg_2))
        #
        # height, width, channel = self.image_mode_1.shape
        # bytesPerLine = 3 * width
        # qImg_mode_1= QImage(self.image_mode_1.data, width, height, bytesPerLine, QImage.Format.Format_BGR888)
        # scaled_qImg_mode_1= qImg_mode_1.scaled(self.ui.Gate_In.width(), self.ui.Gate_In.height())
        # self.ui.Gate_In.setPixmap(QPixmap.fromImage(scaled_qImg_mode_1))


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
    def _init_(self):
        super()._init_()
        self.widget = None
        self.description = "This is a plugins application"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "icon.png"

    def change_stylesheet(self):
        self.widget.set_stylesheet()