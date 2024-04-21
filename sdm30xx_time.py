#!/usr/bin python3
# -*- coding: utf-8 -*-
import sys
from sys import argv
import vxi11
import sched, time
from time import sleep
from datetime import datetime
from numpy import*
import numpy as np
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import socket, errno
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import xlsxwriter
import configparser
from PIL import Image

global aci_first, run_stop, TEMP_SET, G_timer, G_intervall, G_start, SC_card, wb_row, sa_timer, sa_intervall, sa_start, sa_flag, scan_timer, scan_loop_toggle, scan_loop, limit_disable, limit_switch, low_fail, up_fail, upper, lower, upper_val, lower_val, db_switch, db_bak, save_timer, save_intervall, save_start, scanner_run, scanner_on, scanner_auswahl, scanner_auswahl_i, ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner, wert
upper = 0
lower = 0
dot_on = 0
f1_start = 0
nk = 0
db_switch = 0
db_bak = 0
run_stop = 0
aci_first = 0
#worksheet_row_wert = ['DUMMY', 'C1', 'E1', 'G1', 'I1', 'K1', 'M1', 'O1', 'Q1', 'S1', 'U1', 'W1', 'Y1', 'A2', 'C2', 'E2', 'G2']
#worksheet_row_einheit = ['DUMMY', 'D1', 'F1', 'H1', 'J1', 'L1', 'N1', 'P1', 'R1', 'T1', 'V1', 'X1', 'Z1', 'B2', 'D2', 'F2', 'H2']
komma_plus = ["{0:+07.5f}", "{0:+07.4f}", "{0:+07.3f}", "{0:+07.2f}"]
komma = ["{0:.5f}", "{0:.4f}", "{0:.3f}", "{0:.2f}", "{0:.1f}"]
DB_DBM_REF = [50, 75, 93, 110, 124, 125, 135, 150, 250, 300, 500, 600, 800, 900, 1000, 1200, 8000]
VDC = ["AUTO", "200mV", "2V", "20V", "200V", "1000V"]
VDC_45 = ["AUTO", "600mV", "6V", "60V", "600V", "1000V"]
VAC = ["AUTO", "200mV", "2V", "20V", "200V", "750V"]
VAC_45 = ["AUTO", "600mV", "6V", "60V", "600V", "750V"]
ADC = ["AUTO", "200µA", "2mA", "20mA", "200mA", "2A", "10A"]
ADC_45 = ["AUTO", "600µA", "6mA", "60mA", "600mA", "6A", "10A"]
AAC = ["AUTO", "20mA", "200mA", "2A", "10A"]
AAC_45 = ["AUTO", "60mA", "600mA", "6A", "10A"]
RES = ["AUTO", "200", "2000", "20000", "200000", "2000000", "10000000", "100000000"]
RES_45 = ["AUTO", "600", "6000", "60000", "600000", "6000000", "60000000", "100000000"]
RES_display = ["AUTO", "200Ω", "2kΩ", "20kΩ", "200kΩ", "2MΩ", "10MΩ", "100MΩ"]
RES_display_45 = ["AUTO", "600Ω", "6kΩ", "60kΩ", "600kΩ", "6MΩ", "60MΩ", "100MΩ"]
TEMP_RDT_TYPE = ["KITS90", "NITS90", "EITS90", "JITS90", "TITS90", "SITS90", "RITS90", "BITS90", "PT100", "PT1000"]
CAP = ["AUTO", "2nF", "20nF", "200nF", "2uF", "20uF", "200uF", "10mF"]
CAP_65 = ["AUTO", "2nF", "20nF", "200nF", "2uF", "20uF", "200uF", "2mF", "20mF", "100mF"]
CAP_display = ["AUTO", "2nF", "20nF", "200nF", "2µF", "20µF", "200µF", "10mF"]
CAP_display_65 = ["AUTO", "2nF", "20nF", "200nF", "2µF", "20µF", "200µF", "2mF", "20mF", "100mF"]
scanner_auswahl = ["DCV","ACV","FRQ","PER","TEMP","CAP","CONT","2W","DIO","NTC"]
scanner_auswahl_i = ["DCI","ACI"]
scanner_run = 0
scanner_on = 0
scan_loop = 0
scan_loop_toggle = 0
max_graph = 599
xy_counter = 0
x = [time.time() for x in range(max_graph)]
y = np.zeros(max_graph)
messungen = 0
graph = 0
min_mess = 0
max_mess = 0
mess_alt = ''
mess_art = ''
display_c_1 = '#aaff00'       # light green
display_c_2 = '#00ff7f'       # dark green
DC_filter = 0
iz_filter = 0
scanner = 0
funktion_set = ''
cold_boot = 1
check_loop = 0
shot = 0
null_ref = 0.0
null_switch = 0
ntc_wert = 0.0
ntc_switch = 0
save_timer = int(round(time.time()))
scan_timer = int(round(time.time()))
save_intervall = 5
save_start = int(round(time.time())) + save_intervall
sa_flag = 0
sa_timer = 60
sa_intervall = 60
sa_start = 0
G_timer = 0
G_intervall = 0
G_start = 0
limit_switch= 0
limit_disable = 0
low_fail = 0
up_fail = 0
wb_row = 0
SC_card = 'NO'

try:
    output = 'IP='+argv[1]+' on PORT='+str(int(argv[2]))
    print(output)
    HOST = argv[1]
    PORT = int(argv[2])
except IndexError:
    config = configparser.ConfigParser()
    config.read('multimeter.ini')
    HOST = config['hw_settings']['HOST']
    PORT = config['hw_settings']['PORT']
    SCREEN = config['hw_settings']['SCREEN']
    SN_SHOW = config['hw_settings']['SN_SHOW']
    TEMP_TYPE = config['hw_settings']['TEMP_TYPE']
    TEMP_UNIT = config['hw_settings']['TEMP_UNIT']
    print("multimeter.ini File: HOST=" + HOST + ", PORT=" +  str(PORT) + "\n")
    TEMP_SET = "ROUT:"+TEMP_TYPE+"\nROUT:TEMP:UNIT "+TEMP_UNIT

instr=vxi11.Instrument(HOST)
instr.timeout = 60*1000
# instr.write("*RST; *CLS", encoding='utf-8')
instr.write("TRIGGER:SOURCE IMMEDIATE;TRIGGER:COUNT 1;SAMPLE:COUNT 1;TRIG:DEL:AUTO 1", encoding='utf-8')
print ('Set Date:' + time.strftime('%Y-%m-%d'))
print ('Set Time:' + time.strftime('%H:%M:%S'))
instr.write(':SYST:DATE ' + time.strftime('%Y%m%d'))
instr.write(':SYST:TIME ' + time.strftime('%H%M%S'))

leer = instr.ask("*IDN?", encoding='utf-8')
if SN_SHOW == '0':
    idn_text = []
    idn_text = leer.split(',')
    leer = leer.replace(str(idn_text[2]), "xxxxxxx")

if instr.ask("ROUTe:STATe?", encoding='utf-8') == 'OFF':
    print ("ScanCard installed: NO")
    SC_card = 'NO'
elif instr.ask("ROUTe:STATe?", encoding='utf-8') == 'ON':
    print ("ScanCard installed: YES")
    SC_card = 'YES'
print ("DMM Date:", instr.ask("SYSTem:DATE?", encoding='utf-8'))
print ("DMM Time:", instr.ask("SYSTem:TIME?", encoding='utf-8'))
# SC_card = 'NO'
if "SDM3045" in leer:
    out_text = "DMM 4½ Digits 60000 Counts" 
elif "SDM3055" in leer:
    out_text = "DMM 5½ Digits 240000 Counts" 
elif "SDM3065" in leer:
    out_text = "DMM 6½ Digits 2200000 Counts" 
print (out_text)
print ("Siglent IDN: "+instr.ask("IDN-SGLT-PRI?", encoding='utf-8'))
class Ui(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Ui, self).__init__(*args, **kwargs)
        uic.loadUi(SCREEN , self)        # Load the .ui file
        self.setWindowTitle(leer+'  - SC-Card available: '+SC_card)

        self.F1_Button.setFont(QFont('Noto Sans', 8))
        self.F1_Button.setProperty("text"," ")
        self.F1_Button.clicked.connect(self.f1_click)
        self.F2_Button.setFont(QFont('Noto Sans', 8))
        self.F2_Button.setProperty("text"," ")
        self.F2_Button.clicked.connect(self.f2_click)
        self.F3_Button.setFont(QFont('Noto Sans', 8))
        self.F3_Button.setProperty("text"," ")
        self.F3_Button.clicked.connect(self.f3_click)
        self.F4_Button.setFont(QFont('Noto Sans', 8))
        self.F4_Button.setProperty("text"," ")
        self.F4_Button.clicked.connect(self.f4_click)
        self.F5_Button.setFont(QFont('Noto Sans', 8))
        self.F5_Button.setProperty("text","Graph Off\nOn")
        self.F5_Button.clicked.connect(self.graphic)
        self.F6_Button.setFont(QFont('Noto Sans', 8))
        self.F6_Button.setProperty("text"," ")
        self.F6_Button.clicked.connect(self.f6_click)
        self.SCShot_Button.clicked.connect(self.scshot)
        self.SCShot_Button.setProperty("text","Live SC-Shot\nOn")
        self.SCShot_Button.setProperty("toolTip", "Screenshot On OFF")

        self.PTC_Button.setFont(QFont('Noto Sans', 8))
        self.PTC_Button.setText("Funktion\nNTC 10kΩ")
        self.PTC_Button.clicked.connect(self.ntc)
        self.PTC_Button.setVisible(False)

        self.lcdDual.setVisible(False)
        self.zeitText.setVisible(False)
        self.lcdText1.setVisible(True)
        self.lcdText1.setFont(QFont('DejaVu Sans Mono', 24))
        self.dbText.setVisible(False)
        self.offsetText.setVisible(False)

        self.LCD_Dot.setFont(QFont('DejaVu Sans Mono', 14))

        self.db_widget.setVisible(False)
        self.lcd_dial.setFont(QFont('DejaVu Sans Mono', 9))

        self.limit_widget.setVisible(True)
        self.limit_Button.setFont(QFont('Noto Sans', 8))
        self.limit_Button.setText("Limit Off\nOn")
        self.limit_Button.clicked.connect(self.limit)
        self.u_limit_calc.setProperty("toolTip", "Set upper limit: x(.,)xxx - p,n,u,µ,m,k,M,G")
        self.l_limit_calc.setProperty("toolTip", "Set lower limit: x(.,)xxx - p,n,u,µ,m,k,M,G")
        
        for i in range(len(DB_DBM_REF)):
            self.combobox_db.addItem(str(DB_DBM_REF[i]))
        self.combobox_db.setCurrentIndex(0)
        self.combobox_db.setStyleSheet("color: white; background-color: #5a5a5a; selection-background-color: blue;")
        self.combobox_db.currentIndexChanged.connect(self.db_change)
        self.db_widget.setVisible(False)

        self.dial.valueChanged.connect(self.rad)

        self.vdc_Button.clicked.connect(self.vdc)
        self.adc_Button.clicked.connect(self.adc)
        self.vac_Button.clicked.connect(self.vac)
        self.aac_Button.clicked.connect(self.aac)
        self.hz_Button.clicked.connect(self.hz)
        self.per_Button.clicked.connect(self.per)
        self.temp_Button.clicked.connect(self.temp)
        self.ohm_Button.clicked.connect(self.res)
        self.cont_Button.clicked.connect(self.cont)
        self.cap_Button.clicked.connect(self.cap)
        self.diod_Button.clicked.connect(self.diod)
        self.CH_lcd_Button_1.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_2.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_3.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_4.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_5.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_6.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_7.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_8.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_9.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_10.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_11.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_12.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_13.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_14.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_15.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.CH_lcd_Button_16.setStyleSheet("background-color: #aaff00; text-align: right;")
        self.scanner_widget.setVisible(False)
        for i in range(len(scanner_auswahl)):
            self.CH_comboBox_1.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_2.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_3.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_4.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_5.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_6.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_7.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_8.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_9.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_10.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_11.addItem(str(scanner_auswahl[i]))
            self.CH_comboBox_12.addItem(str(scanner_auswahl[i]))
        for i in range(len(scanner_auswahl_i)):
            self.CH_comboBox_13.addItem(str(scanner_auswahl_i[i]))
            self.CH_comboBox_14.addItem(str(scanner_auswahl_i[i]))
            self.CH_comboBox_15.addItem(str(scanner_auswahl_i[i]))
            self.CH_comboBox_16.addItem(str(scanner_auswahl_i[i]))

        config.read('channels.ini')
        for i in range (1,17):
            index_set = getattr(self, "CH_comboBox_" + str(i)).findText(config['channel_settings']['CH'+str(i)])
            getattr(self, "CH_comboBox_" + str(i)).setCurrentIndex(index_set)
            check_set = config['channel_settings']['CH_check'+str(i)]
            if check_set == "True":
                getattr(self, "CH_checkBox_" + str(i)).setChecked(True)
            elif check_set == "False":
                getattr(self, "CH_checkBox_" + str(i)).setChecked(False)

        self.CH_comboBox_1.currentIndexChanged.connect(self.combo_1)
        self.CH_comboBox_2.currentIndexChanged.connect(self.combo_2)
        self.CH_comboBox_3.currentIndexChanged.connect(self.combo_3)
        self.CH_comboBox_4.currentIndexChanged.connect(self.combo_4)
        self.CH_comboBox_5.currentIndexChanged.connect(self.combo_5)
        self.CH_comboBox_6.currentIndexChanged.connect(self.combo_6)
        self.CH_comboBox_7.currentIndexChanged.connect(self.combo_7)
        self.CH_comboBox_8.currentIndexChanged.connect(self.combo_8)
        self.CH_comboBox_9.currentIndexChanged.connect(self.combo_9)
        self.CH_comboBox_10.currentIndexChanged.connect(self.combo_10)
        self.CH_comboBox_11.currentIndexChanged.connect(self.combo_11)
        self.CH_comboBox_12.currentIndexChanged.connect(self.combo_12)
        self.CH_comboBox_13.currentIndexChanged.connect(self.combo_13)
        self.CH_comboBox_14.currentIndexChanged.connect(self.combo_14)
        self.CH_comboBox_15.currentIndexChanged.connect(self.combo_15)
        self.CH_comboBox_16.currentIndexChanged.connect(self.combo_16)

        self.SCconfig_Button.clicked.connect(self.config_write_channals)
        self.SCconfig_Button.setText("Save all Mode\nSettings")
        self.SCconfig_Button.setStyleSheet("background-color: #5a5a5a; color: #880000;")
#        self.SCrun_Button.setFont(QFont('Noto Sans', 7))
        self.SCrun_Button.setProperty("text","Scanner ON")
        self.SCrun_Button.clicked.connect(self.SCrun)
        self.SCloop_Button.setFont(QFont('Noto Sans', 7))
        self.SCloop_Button.setProperty("text","Scanner Loop\nSingle SLOW 120s")
        self.SCloop_Button.clicked.connect(self.scanner_loop)
        self.SCloop_all_Button.setFont(QFont('Noto Sans', 7))
        self.SCloop_all_Button.setProperty("text","Scanner Loop\nAll FAST")
        self.SCloop_all_Button.clicked.connect(self.scanner_loop_all)

        self.intervall_box.addItem('60 s')
        self.intervall_box.addItem('120 s')
        self.intervall_box.addItem('240 s')
        self.intervall_box.addItem('300 s')
        self.intervall_box.addItem('900 s')
        self.intervall_box.addItem('1800 s')
        self.intervall_box.setProperty("enabled", "1")
        self.intervall_box.setCurrentIndex(0)
        self.intervall_box.currentIndexChanged.connect(self.save_change)
        self.intervall_box.setStyleSheet("color: white; background-color: #5a5a5a; selection-background-color: blue;")

        self.Save_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
        self.Save_Button.clicked.connect(self.save)
        self.Save_Button.setProperty("toolTip", "Save Scan to Excel/LibreOffice File")
        
        self.G_intervall_box.addItem('0 s')
        self.G_intervall_box.addItem('1 s')
        self.G_intervall_box.addItem('5 s')
        self.G_intervall_box.addItem('10 s')
        self.G_intervall_box.addItem('15 s')
        self.G_intervall_box.addItem('30 s')
        self.G_intervall_box.addItem('60 s')
        self.G_intervall_box.addItem('120 s')
        self.G_intervall_box.addItem('240 s')
        self.G_intervall_box.addItem('300 s')
        self.G_intervall_box.addItem('900 s')
        self.G_intervall_box.setProperty("enabled", "1")
        self.G_intervall_box.setCurrentIndex(0)
        self.G_intervall_box.currentIndexChanged.connect(self.G_change)
        self.G_intervall_box.setStyleSheet("color: white; background-color: #5a5a5a; selection-background-color: #0000ff;")
        self.G_iText.setVisible(True)
        self.G_iText.setText("Graph/CSV Intervall")
#        font = QtGui.QFont()
#        font.setPointSize(8)
#        self.textEdit.setFont(font)
        self.textEdit.setStyleSheet("background-color: #464646; color: #ffffff;")
        self.Clear_Button.clicked.connect(self.clear)
        self.Clear_Button.setText("Clear Text")
        self.t_Save_Button.setStyleSheet("background-color: #5a5a5a; color: #880000;")
        self.t_Save_Button.setText("Save CSV")
        self.t_Save_Button.clicked.connect(self.t_save)
        self.t_Save_Button.setProperty("toolTip", "Save Text to CSV File")

        self.run_stop_Button.setText("STOP")
        self.run_stop_Button.setStyleSheet("background-color: #5a5a5a; color: #880000;")
        self.run_stop_Button.clicked.connect(self.runstop)
        self.run_stop_Button.setVisible(False)
        
        self.actionAbout.triggered.connect(self.about)
        self.actionExit.triggered.connect(self.exit)

        self.setFixedSize(766, 304)         # klein ohne SC
        self.graph_frame.setFixedWidth(746)
        self.graph_frame.setFixedHeight(459)
        self.graph_frame.setMaximumWidth(746)
        self.graph_frame.setMaximumHeight(459)
        self.graphWidget.setFixedWidth(739)
        self.graphWidget.setFixedHeight(453)
        self.graphWidget.setMaximumWidth(739)
        self.graphWidget.setMaximumHeight(453)
        
        self.pixmap = QPixmap('sdm3065.bmp')
        self.screenshot.setPixmap(self.pixmap)
        
        if SC_card == "YES":
            self.SC_Button.setVisible(True)
            self.SC_Button.clicked.connect(self.multi)
        elif SC_card == "NO":
            self.SC_Button.setVisible(True)
            self.SC_Button.clicked.connect(self.multi)
            self.intervall_box.setVisible(False)
            self.Save_Button.setVisible(False)
            self.SCloop_Button.setVisible(False)
            self.SCloop_all_Button.setVisible(False)
            self.SCrun_Button.setVisible(False)

        self.timer_single=QTimer()
        self.timer_single.start(250)
        self.timer_single.timeout.connect(self.update)
        
#        self.statusBar()
        self.vdc()
        self.show()

    def clear(self):
        global G_timer, G_intervall, G_start
        G_intervall = int(self.G_intervall_box.currentText().replace(' s', ''))
        G_start = int(round(time.time()))
        self.textEdit.clear()

    def t_save(self):
        fileName = ""
        options = QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save Log-File","dmmLogFile.csv","Alle Files (*);;Text Files (*.csv)", options=options)
        with open(fileName, 'w') as logFile:
            logFile.write(str(self.textEdit.toPlainText()))

    def combo_1(self, dx):
        self.CH_comboBox_1.setCurrentIndex(dx)
    def combo_2(self, dx):
        self.CH_comboBox_2.setCurrentIndex(dx)
    def combo_3(self, dx):
        self.CH_comboBox_3.setCurrentIndex(dx)
    def combo_4(self, dx):
        self.CH_comboBox_4.setCurrentIndex(dx)
    def combo_5(self, dx):
        self.CH_comboBox_5.setCurrentIndex(dx)
    def combo_6(self, dx):
        self.CH_comboBox_6.setCurrentIndex(dx)
    def combo_7(self, dx):
        self.CH_comboBox_7.setCurrentIndex(dx)
    def combo_8(self, dx):
        self.CH_comboBox_8.setCurrentIndex(dx)
    def combo_9(self, dx):
        self.CH_comboBox_9.setCurrentIndex(dx)
    def combo_10(self, dx):
        self.CH_comboBox_10.setCurrentIndex(dx)
    def combo_11(self, dx):
        self.CH_comboBox_11.setCurrentIndex(dx)
    def combo_12(self, dx):
        self.CH_comboBox_12.setCurrentIndex(dx)
    def combo_13(self, dx):
        self.CH_comboBox_13.setCurrentIndex(dx)
    def combo_14(self, dx):
        self.CH_comboBox_14.setCurrentIndex(dx)
    def combo_15(self, dx):
        self.CH_comboBox_15.setCurrentIndex(dx)
    def combo_16(self, dx):
        self.CH_comboBox_16.setCurrentIndex(dx)

    def about(self):
        QMessageBox.about(self, "About", "Siglent \t SDM3055, SDM3055-SC\n\nTCP Control Software\nVersion: 1.00\n\nDevelopment and bug reports:\nmartin@martin-bochum.de\n\nCopyright (C)  2022  Martin Müller\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\nSee the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public\nLicense along with this program (GPL.txt).\nIf not, see <https://www.gnu.org/licenses/>.")

    def config_write_channals(self):
        config.read('channels.ini')
        for i in range(1,16):
            config.set('channel_settings', 'CH'+str(i), getattr(self, "CH_comboBox_" + str(i)).currentText())
        for i in range(1,17):
            config.set('channel_settings', 'CH_check'+str(i), str(getattr(self, "CH_checkBox_" + str(i)).isChecked()))
        with open('channels.ini', 'w') as configfile:
            config.write(configfile)        

    def SCrun(self):
        global aci_first, TEMP_SET, format_date, format_time, wb_row, sa_timer, sa_intervall, sa_start, sa_flag, scan_loop_toggle, scan_loop, scanner_run, scanner_on, scanner_auswahl, scanner_auswahl_i, ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner, wert
        self.intervall_box.setVisible(False)
        self.Save_Button.setVisible(False)
        self.SCrun_Button.setVisible(True)
        self.offsetText.setVisible(False)
        self.null_off()
        aci_first = 0
        skip = 0
        if scan_loop == 0:
            self.SCloop_Button.setVisible(False)
            QMessageBox.about(self, "Info", "DISCONNECT Front Panel Cables !")
            self.SCloop_all_Button.setVisible(False)
        self.SCconfig_Button.setVisible(False)
        if scanner_run == 0:
            if DC_filter == 0:
                instr.write("VOLT:FILT ON", encoding='utf-8')
            instr.write("CONF:VOLT", encoding='utf-8')
            instr.write("TRIG:DEL:AUTO 1", encoding='utf-8')
            instr.write("ROUTe:SCAN ON", encoding='utf-8')
            instr.write(TEMP_SET, encoding='utf-8')
#            instr.write("ROUTe:FREQuency:APERture 0.1", encoding='utf-8')
#            instr.write("ROUTe:PERiod:APERture 0.1", encoding='utf-8')
            instr.write("ROUTe:FUNC SCAN", encoding='utf-8')
            instr.write("ROUTe:COUN 1", encoding='utf-8')
            self.lcdDual.setVisible(True)
            self.lcdText2.setVisible(False)
            self.lcdDual.setText("Scanning CH1...CH16")
            self.lcdNumber.setText("-.-----")
            self.lcdText1.setText(" --")
            
            for i in range (1,17):
                instr.write("ROUT:LIMI:LOW "+str(i), encoding='utf-8')
                instr.write("ROUT:LIMI:HIGH "+str(i), encoding='utf-8')
                m_ntc = 0
                m_per = 0
                w_t = 5
                n_c = i+1
                on_off = "OFF"
                if getattr(self, "CH_checkBox_" + str(i)).isChecked() == True:
                    on_off = "ON"
                if i <= 12:
                    if getattr(self, "CH_comboBox_" + str(i)).currentText() == "NTC" or getattr(self, "CH_comboBox_" + str(i)).currentText() == "PER" or getattr(self, "CH_comboBox_" + str(i)).currentText() == "FRQ" or getattr(self, "CH_comboBox_" + str(i)).currentText() == "TEMP":
                        if getattr(self, "CH_comboBox_" + str(i)).currentText() == "NTC":
                            instr.write("ROUT:CHAN "+str(int(i))+","+on_off+",2W,AUTO,SLOW", encoding='utf-8')
                            m_ntc = 1
                        elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "TEMP":
                            instr.write("ROUT:CHAN "+str(int(i))+","+on_off+","+getattr(self, "CH_comboBox_" + str(i)).currentText()+",AUTO,SLOW", encoding='utf-8')
                        elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "PER":
                            instr.write("ROUT:PER", encoding='utf-8')
                            instr.write("ROUT:CHAN "+str(int(i))+","+on_off+",FRQ,AUTO,SLOW", encoding='utf-8')
                            m_per = 1
                        elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "FRQ":
                            instr.write("ROUT:FREQ", encoding='utf-8')
                            instr.write("ROUT:CHAN "+str(int(i))+","+on_off+",FRQ,AUTO,SLOW", encoding='utf-8')
                            m_per = 0
                    elif getattr(self, "CH_comboBox_" + str(i)).currentText() != "PER" and getattr(self, "CH_comboBox_" + str(i)).currentText() != "NTC" and getattr(self, "CH_comboBox_" + str(i)).currentText() != "FRQ" and getattr(self, "CH_comboBox_" + str(i)).currentText() != "TEMP":
                            instr.write("ROUT:CHAN "+str(int(i))+","+on_off+","+getattr(self, "CH_comboBox_" + str(i)).currentText()+",AUTO,SLOW", encoding='utf-8')
                elif i >= 13:
                    instr.write("ROUT:CHAN "+str(int(i))+","+on_off+","+getattr(self, "CH_comboBox_" + str(i)).currentText()+",2A,SLOW", encoding='utf-8')
                if getattr(self, "CH_checkBox_" + str(i)).isChecked() == True:
                    if i >= 2 and getattr(self, "CH_checkBox_" + str(i-1)).isChecked() == False:
                        w_t = 6
                    instr.write("ROUTe:DEL MIN", encoding='utf-8')
                    instr.write("ROUT:LIMI:LOW "+str(i), encoding='utf-8')
                    instr.write("ROUT:LIMI:HIGH "+str(i), encoding='utf-8')
                    instr.write("ROUTe:STARt ON", encoding='utf-8')
                    self.warte(w_t, i," ")
                    instr.write("ROUTe:STARt OFF", encoding='utf-8')
                self.dbText.setVisible(True)
                self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
                if getattr(self, "CH_checkBox_" + str(i)).isChecked() == True:
                    dummy = instr.ask("ROUTe:DATA? "+str(i), encoding='utf-8')
                    dummy = dummy.replace(',', '')
                    dummy = dummy.replace('  ', ' ')
                    dummy_1 = dummy.split(' ')
                    dummy_1[1] = dummy_1[1].replace('OHM', 'Ω')
                    dummy_1[1] = dummy_1[1].replace('HZ', 'Hz')
                    dummy_1[1] = dummy_1[1].replace('S', 's')
                    wert = round(float(dummy_1[0]), 15)
                    dummy_a = list(self.check_wert(wert))
                    fo_string = komma[0].format(wert*dummy_a[1])
                    if len(dummy_1) == 3:
                        if "C" in dummy_1[2]:
                            dummy_1[1] = '°C  '
                        if "F" in dummy_1[2]  and dummy_a[0] == "":
                            dummy_1[1] = '°F  '
                        elif "F" in dummy_1[2]:
                            dummy_1[1] = 'F'
                        if "K" in dummy_1[2]:
                            dummy_1[1] = 'K   '
                    if wert >= 9.9E+34:
                        self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
                        fo_string = "Overload"
                        dummy_1[1] = ""
                        dummy_a[0] = ""
                    if wert >= 9.9E+37:
                        self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
                        fo_string = "Open"
                        dummy_1[1] = ""
                        dummy_a[0] = ""
                    dummy_1[1] = str(dummy_a[0])+str(dummy_1[1]).ljust(3, ' ')
                    if len(dummy_1[1]) == 3:
                        dummy_1[1] = dummy_1[1]+ " "
                    if getattr(self, "CH_comboBox_" + str(i)).currentText() != "NTC":
                        getattr(self, "CH_lcd_Button_" + str(i)).setText(fo_string+" "+dummy_1[1])
                        self.lcdNumber.setText(fo_string)
                        self.lcdText1.setText(dummy_1[1])
                        self.dbText.setText("Channel "+ str(i))
                        m_per = 0
                        instr.write("ROUT:FREQ", encoding='utf-8')
                    elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "NTC":
                        m_ntc = 0
                        ntc = self.temp_ntc(wert/1000)
                        fo_string = komma[0].format(ntc)
                        getattr(self, "CH_lcd_Button_" + str(i)).setText(fo_string+" °C  ")
                        self.lcdNumber.setText(fo_string)
                        self.lcdText1.setText(" °C")
                        self.dbText.setText("Channel "+ str(i))
                elif getattr(self, "CH_checkBox_" + str(i)).isChecked() == False:
                    getattr(self, "CH_lcd_Button_" + str(i)).setText("-.----- ----")

            if sa_flag == 1:
                w_wert = 2
                w_einheit = 3
                sa_timer = int(round(time.time()))
                sa_intervall = int(self.intervall_box.currentText().replace(' s', ''))
                sa_start = int(round(time.time())) + save_intervall
                now = datetime.now()
                worksheet.write(wb_row, 0, now, format_date)
                worksheet.write(wb_row, 1, now, format_time)
                for i in range (1,17):
                    if getattr(self, "CH_checkBox_" + str(i)).isChecked() == True:
                        full_txt = getattr(self, "CH_lcd_Button_" + str(i)).text()
                        full_txt = full_txt.split(' ')
                        if "Open" not in full_txt[0] and "-.-----" not in full_txt[0]:
                            worksheet.write(wb_row, w_wert, float(full_txt[0]))
                        if len(full_txt) >= 2:
                            worksheet.write(0, w_einheit, getattr(self, "CH_comboBox_" + str(i)).currentText())
                            worksheet.write(wb_row, w_einheit, full_txt[1])
                        w_wert += 2
                        w_einheit += 2
                    elif getattr(self, "CH_checkBox_" + str(i)).isChecked() == False:
                        full_txt = getattr(self, "CH_lcd_Button_" + str(i)).text()
                        full_txt = full_txt.split(' ')
                        worksheet.write(wb_row, w_wert, 0.00000)
                        if len(full_txt) >= 2:
                            worksheet.write(0, w_einheit, getattr(self, "CH_comboBox_" + str(i)).currentText())
                        w_wert += 2
                        w_einheit += 2
                        
                wb_row += 1

            if DC_filter == 0:
                instr.write("VOLT:FILT ON", encoding='utf-8')
            self.SCrun_Button.setProperty("text","Scanner ON")
            self.zeitText.setVisible(True)
            now = datetime.now()
            timestamp = "%02d.%02d.%04d - %02d:%02d:%02d" % (now.day, now.month, now.year, now.hour, now.minute, now.second)
            self.zeitText.setText("Last Scan: "+timestamp)
            self.lcdDual.setVisible(False)
            self.dbText.setVisible(False)
            self.lcdText2.setVisible(True)
            self.intervall_box.setVisible(True)
            self.Save_Button.setVisible(True)
            self.SCloop_Button.setVisible(True)
            self.SCloop_all_Button.setVisible(True)
            instr.write("ABORt\n*CLS\n*RST", encoding='utf-8')
            instr.write(funktion_set, encoding='utf-8')
            instr.write("TRIGger:DELay:AUTO ON", encoding='utf-8')
            self.SCconfig_Button.setVisible(True)

    def SCrun_all_in_one(self):
        global TEMP_SET, format_date, format_time, wb_row, sa_timer, sa_intervall, sa_start, sa_flag, scan_loop_toggle, scan_loop, scanner_run, scanner_on, scanner_auswahl, scanner_auswahl_i, ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner, wert
        self.intervall_box.setVisible(False)
        self.Save_Button.setVisible(False)
        self.SCrun_Button.setVisible(True)
        self.null_off()
        self.offsetText.setVisible(False)
        self.SCconfig_Button.setVisible(False)
        if scanner_run == 0:
            if DC_filter == 0:
                instr.write("VOLT:FILT ON", encoding='utf-8')
            instr.write("CONF:VOLT", encoding='utf-8')
            self.lcdDual.setVisible(True)
            self.lcdText2.setVisible(False)
            self.lcdDual.setText("Scanning CH01...CH16")
            self.lcdNumber.setText("-.-----")
            self.lcdText1.setText(" --")
            instr.write("ROUTe:SCAN ON", encoding='utf-8')
            instr.write(TEMP_SET, encoding='utf-8')
            instr.write("ROUTe:FUNC SCAN", encoding='utf-8')
            instr.write("ROUTe:COUN 1", encoding='utf-8')
            instr.write("ROUTe:FREQuency:APERture 1", encoding='utf-8')
            instr.write("ROUTe:PERiod:APERture 1", encoding='utf-8')
            for i in range (1,17):
                m_ntc = 0
                m_per = 0
                w_t = 3
                on_off = "OFF"
                if getattr(self, "CH_checkBox_" + str(i)).isChecked() == True:
                    on_off = "ON"
                    if i <= 12:
                        if getattr(self, "CH_comboBox_" + str(i)).currentText() == "NTC" or getattr(self, "CH_comboBox_" + str(i)).currentText() == "PER" or getattr(self, "CH_comboBox_" + str(i)).currentText() == "TEMP" or getattr(self, "CH_comboBox_" + str(i)).currentText() == "FRQ" or getattr(self, "CH_comboBox_" + str(i)).currentText() == "DIO" or getattr(self, "CH_comboBox_" + str(i)).currentText() == "CAP":
                            if getattr(self, "CH_comboBox_" + str(i)).currentText() == "NTC":
                                instr.write("ROUT:CHAN "+str(int(i))+","+on_off+",2W,AUTO,SLOW", encoding='utf-8')
                                m_ntc = 1
                            elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "PER":
                                instr.write("ROUT:PER", encoding='utf-8')
                                instr.write("ROUT:CHAN "+str(int(i))+","+on_off+",FRQ,AUTO,SLOW", encoding='utf-8')
                                m_per = 1
                            elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "FRQ":
                                instr.write("ROUT:FREQ", encoding='utf-8')
                                instr.write("ROUT:CHAN "+str(int(i))+","+on_off+",FRQ,AUTO,SLOW", encoding='utf-8')
                                m_per = 0
                            elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "TEMP":
                                instr.write("ROUT:CHAN "+str(int(i))+","+on_off+","+getattr(self, "CH_comboBox_" + str(i)).currentText()+",AUTO,SLOW", encoding='utf-8')
                                w_t = 4
                            elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "DIO":
                                instr.write("ROUT:CHAN "+str(int(i))+","+on_off+","+getattr(self, "CH_comboBox_" + str(i)).currentText()+",AUTO,SLOW", encoding='utf-8')
                                w_t = 5
                            elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "CAP":
                                instr.write("ROUT:CHAN "+str(int(i))+","+on_off+","+getattr(self, "CH_comboBox_" + str(i)).currentText()+",AUTO,SLOW", encoding='utf-8')
                                w_t = 4
                        elif getattr(self, "CH_comboBox_" + str(i)).currentText() != "PER" and getattr(self, "CH_comboBox_" + str(i)).currentText() != "NTC" and getattr(self, "CH_comboBox_" + str(i)).currentText() != "TEMP" and getattr(self, "CH_comboBox_" + str(i)).currentText() != "FRQ" and getattr(self, "CH_comboBox_" + str(i)).currentText() != "DIO" and getattr(self, "CH_comboBox_" + str(i)).currentText() != "CAP":
                            instr.write("ROUT:CHAN "+str(int(i))+","+on_off+","+getattr(self, "CH_comboBox_" + str(i)).currentText()+",AUTO,SLOW", encoding='utf-8')
                    elif i >= 13:
                        instr.write("ROUT:CHAN "+str(int(i))+","+on_off+","+getattr(self, "CH_comboBox_" + str(i)).currentText()+",2A,SLOW", encoding='utf-8')
            instr.write("ROUTe:DEL MIN", encoding='utf-8')
            instr.write("ROUT:LIMI:LOW 1", encoding='utf-8')
            instr.write("ROUT:LIMI:HIGH 16", encoding='utf-8')
            instr.write("ROUTe:STARt ON", encoding='utf-8')
            self.warte(30, 20,"CH 01...16")
            for i in range (1,13):
                if getattr(self, "CH_checkBox_" + str(i)).isChecked() == True:

                    self.dbText.setVisible(False)
                    self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
                    dummy = instr.ask("ROUTe:DATA? "+str(i), encoding='utf-8')
                    dummy = dummy.replace(',', '')
                    dummy = dummy.replace('  ', ' ')
                    dummy_1 = dummy.split(' ')
                    dummy_1[1] = dummy_1[1].replace('OHM', 'Ω')
                    dummy_1[1] = dummy_1[1].replace('HZ', 'Hz')
                    dummy_1[1] = dummy_1[1].replace('S', 's')
                    wert = round(float(dummy_1[0]), 15)
                    if getattr(self, "CH_comboBox_" + str(i)).currentText() == "PER":
                        wert = 1/wert
                        dummy_1[1] = 's'
                    dummy_a = list(self.check_wert(wert))
                    fo_string = komma[0].format(wert*dummy_a[1])
                    if len(dummy_1) == 3:
                        if "C" in dummy_1[2]:
                            dummy_1[1] = '°C  '
                        if "F" in dummy_1[2]  and dummy_a[0] == "":
                            dummy_1[1] = '°F  '
                        elif "F" in dummy_1[2]:
                            dummy_1[1] = 'F'
                        if "K" in dummy_1[2]:
                            dummy_1[1] = 'K   '
                    if wert >= 9.9E+34:
#                        self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
                        fo_string = "Overload"
                        dummy_1[1] = ""
                        dummy_a[0] = ""
                    if wert >= 9.9E+37:
#                        self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
                        fo_string = "Open"
                        dummy_1[1] = ""
                        dummy_a[0] = ""
                    dummy_1[1] = str(dummy_a[0])+str(dummy_1[1]).ljust(3, ' ')
                    if len(dummy_1[1]) == 3:
                        dummy_1[1] = dummy_1[1]+ " "
                    if getattr(self, "CH_comboBox_" + str(i)).currentText() != "NTC":
                        getattr(self, "CH_lcd_Button_" + str(i)).setText(fo_string+" "+dummy_1[1])
                        m_per = 0
                        instr.write("ROUT:FREQ", encoding='utf-8')
                    elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "NTC":
                        m_ntc = 0
                        ntc = self.temp_ntc(wert/1000)
                        fo_string = komma[0].format(ntc)
                        getattr(self, "CH_lcd_Button_" + str(i)).setText(fo_string+" °C  ")
                elif getattr(self, "CH_checkBox_" + str(i)).isChecked() == False:
                    getattr(self, "CH_lcd_Button_" + str(i)).setText("-.----- ----")
            self.lcdDual.setText("Scanning CH13...CH16")
            instr.write("ROUTe:DEL MIN", encoding='utf-8')
            instr.write("ROUTe:STARt OFF", encoding='utf-8')
            instr.write("ROUT:LIMI:LOW 13", encoding='utf-8')
            instr.write("ROUT:LIMI:HIGH 16", encoding='utf-8')
            instr.write("ROUTe:STARt ON", encoding='utf-8')
            self.warte(10,20,"CH 13...16")
            self.lcdNumber.setText("-.-----")
            self.lcdText1.setText(" --")
            instr.write("ROUTe:STARt OFF", encoding='utf-8')
            for i in range (13,17):
                if getattr(self, "CH_checkBox_" + str(i)).isChecked() == True:

                    self.dbText.setVisible(False)
                    self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
                    dummy = instr.ask("ROUTe:DATA? "+str(i), encoding='utf-8')
                    dummy = dummy.replace(',', '')
                    dummy = dummy.replace('  ', ' ')
                    dummy_1 = dummy.split(' ')
                    dummy_1[1] = dummy_1[1].replace('OHM', 'Ω')
                    dummy_1[1] = dummy_1[1].replace('HZ', 'Hz')
                    dummy_1[1] = dummy_1[1].replace('S', 's')
                    wert = round(float(dummy_1[0]), 15)
                    if getattr(self, "CH_comboBox_" + str(i)).currentText() == "PER":
                        wert = 1/wert
                        dummy_1[1] = 's'
                    dummy_a = list(self.check_wert(wert))
                    fo_string = komma[0].format(wert*dummy_a[1])
                    if len(dummy_1) == 3:
                        if "C" in dummy_1[2]:
                            dummy_1[1] = '°C  '
                        if "F" in dummy_1[2]  and dummy_a[0] == "":
                            dummy_1[1] = '°F  '
                        elif "F" in dummy_1[2]:
                            dummy_1[1] = 'F'
                        if "K" in dummy_1[2]:
                            dummy_1[1] = 'K   '
                    if wert >= 9.9E+34:
                        self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
                        fo_string = "Overload"
                        dummy_1[1] = ""
                        dummy_a[0] = ""
                    if wert >= 9.9E+37:
                        self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
                        fo_string = "Open"
                        dummy_1[1] = ""
                        dummy_a[0] = ""
                    dummy_1[1] = str(dummy_a[0])+str(dummy_1[1]).ljust(3, ' ')
                    if len(dummy_1[1]) == 3:
                        dummy_1[1] = dummy_1[1]+ " "
                    if getattr(self, "CH_comboBox_" + str(i)).currentText() != "NTC":
                        getattr(self, "CH_lcd_Button_" + str(i)).setText(fo_string+" "+dummy_1[1])
                        m_per = 0
                        instr.write("ROUT:FREQ", encoding='utf-8')
                    elif getattr(self, "CH_comboBox_" + str(i)).currentText() == "NTC":
                        m_ntc = 0
                        ntc = self.temp_ntc(wert/1000)
                        fo_string = komma[0].format(ntc)
                        getattr(self, "CH_lcd_Button_" + str(i)).setText(fo_string+" °C  ")
                elif getattr(self, "CH_checkBox_" + str(i)).isChecked() == False:
                    getattr(self, "CH_lcd_Button_" + str(i)).setText("-.----- ----")

            if sa_flag == 1:
                w_wert = 2
                w_einheit = 3
                sa_timer = int(round(time.time()))
                sa_intervall = int(self.intervall_box.currentText().replace(' s', ''))
                sa_start = int(round(time.time())) + save_intervall
                now = datetime.now()
                worksheet.write(wb_row, 0, now, format_date)
                worksheet.write(wb_row, 1, now, format_time)
                for i in range (1,17):
                    if getattr(self, "CH_checkBox_" + str(i)).isChecked() == True:
                        full_txt = getattr(self, "CH_lcd_Button_" + str(i)).text()
                        full_txt = full_txt.split(' ')
                        if "Open" not in full_txt[0] and "-.-----" not in full_txt[0]:
                            worksheet.write(wb_row, w_wert, float(full_txt[0]))
                        if len(full_txt) >= 2:
                            worksheet.write(0, w_einheit, getattr(self, "CH_comboBox_" + str(i)).currentText())
                            worksheet.write(wb_row, w_einheit, full_txt[1])
                        w_wert += 2
                        w_einheit += 2
                    elif getattr(self, "CH_checkBox_" + str(i)).isChecked() == False:
                        full_txt = getattr(self, "CH_lcd_Button_" + str(i)).text()
                        full_txt = full_txt.split(' ')
                        worksheet.write(wb_row, w_wert, 0.00000)
                        if len(full_txt) >= 2:
                            worksheet.write(0, w_einheit, getattr(self, "CH_comboBox_" + str(i)).currentText())
                        w_wert += 2
                        w_einheit += 2
                        
                wb_row += 1

            if DC_filter == 0:
                instr.write("VOLT:FILT OFF", encoding='utf-8')
            self.SCrun_Button.setProperty("text","Scanner ON")
            self.zeitText.setVisible(True)
            now = datetime.now()
            timestamp = "%02d.%02d.%04d - %02d:%02d:%02d" % (now.day, now.month, now.year, now.hour, now.minute, now.second)
            self.zeitText.setText("Last Scan: "+timestamp)
            self.lcdDual.setVisible(False)
            self.dbText.setVisible(False)
            self.lcdText2.setVisible(True)
            self.intervall_box.setVisible(True)
            self.Save_Button.setVisible(True)
            self.SCloop_Button.setVisible(True)
            instr.write("ABORt\n*CLS\n*RST", encoding='utf-8')
            instr.write(funktion_set, encoding='utf-8')
            instr.write("TRIGger:DELay:AUTO ON", encoding='utf-8')
            self.SCconfig_Button.setVisible(True)
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))

    def scanner_loop(self):
        global sa_intervall, scan_timer, scan_loop_toggle, scan_loop, scanner_run, scanner_on, scanner_auswahl, scanner_auswahl_i, ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner, wert
        if scan_loop == 0 and check_loop == 0:
            if self.intervall_box.currentIndex() == 0:
                self.intervall_box.setCurrentIndex(1)
            self.save_change()
            now = datetime.now()
            scan_timer = int(round(time.time())) + sa_intervall
            scanner_run = 0
            scan_loop = 1
            check_loop = 1
            self.SCloop_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            self.SCloop_all_Button.setVisible(False)
            self.SCrun_Button.setVisible(True)
            self.SCrun()
        elif scan_loop >= 1 and check_loop == 0:
            scanner_run = 0
            scan_loop = 0
            check_loop = 1
            self.SCloop_Button.setProperty("text","Scanner Loop\nSingle SLOW")
            self.SCloop_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            self.SCloop_all_Button.setVisible(True)
            self.SCrun_Button.setVisible(True)

    def scanner_loop_all(self):
        global sa_intervall, scan_timer, scan_loop_toggle, scan_loop, scanner_run, scanner_on, scanner_auswahl, scanner_auswahl_i, ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner, wert
        if scan_loop == 0 and check_loop == 0:
            now = datetime.now()
            scan_timer = int(round(time.time())) + sa_intervall
            scanner_run = 0
            scan_loop = 2
            check_loop = 1
            self.SCloop_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            self.SCloop_all_Button.setVisible(False)
            self.SCrun_Button.setVisible(False)
            self.SCrun_all_in_one()
        elif scan_loop >= 1 and check_loop == 0:
            scanner_run = 0
            scan_loop = 0
            check_loop = 1
            self.SCloop_Button.setProperty("text","Scanner Loop\nSingle SLOW")
            self.SCloop_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            self.SCloop_all_Button.setVisible(True)
            self.SCrun_Button.setVisible(True)

    def warte(self, zeit_s, i, b_text):
        global scan_timer, scan_loop_toggle, check_loop, scanner_run, scan_loop, save_timer, save_intervall, save_start, aci_first
        i_ein = i
        now = datetime.now()
        save_timer = int(round(time.time()))
        save_intervall = 1
        save_start = int(round(time.time())) + save_intervall
        save_loop = 0
        self.SCrun_Button.setVisible(True)
        self.SCrun_Button.setStyleSheet("background-color: #5a5a5a; color: #aa0000;")
        ze = 2
        if i_ein < 20 and i_ein != 17:
            ping_pong ="▻ ▻      "
            ba1 = ["█", "▇", "▆", "▅", "▄", "▃", "▂", "▁"]
            zwso = ""
            zwso = getattr(self, "CH_Text_" + str(i_ein)).text()
            getattr(self, "CH_Text_" + str(i_ein)).setStyleSheet("background-color: #ffffff; color: #000000;")
            while True:
                now = datetime.now()
                save_timer = int(round(time.time()))
                sleep(0.333)
                if save_timer >= save_start:
                    self.scanner_widget.repaint()
                    check_loop = 0
                    save_start = int(round(time.time())) + save_intervall
                    self.SCrun_Button.setProperty("text","CH 0"+str(i)+"\n"+str(int(zeit_s - save_loop)) + " s")
                    if i >= 10:
                        self.SCrun_Button.setProperty("text","CH "+str(i)+"\n"+str(int(zeit_s - save_loop)) + " s")
                    self.scanner_widget.repaint()
                    self.lcdDual.setText("Scanning Channel "+str(i)+" "+getattr(self, "CH_comboBox_" + str(i)).currentText())
                    if scan_loop == 1:
                        self.SCloop_Button.setProperty("text","Scanner Loop\n"+str(int(scan_timer - save_timer)) + " s")
                    zws = zwso+" "+ba1[int(zeit_s - save_loop)-(zeit_s-7)]
                    getattr(self, "CH_Text_" + str(i_ein)).setText(zws)
                    ping_pong = ping_pong[0:int(9-ze)]
                    ze += 2
                    self.scanner_widget.repaint()
                    self.frame.repaint()
                    save_loop += 1
                    if shot == 1:
                        instr.write("SCDP")
                        self.result_str = instr.read_raw()
                        self.pixmap.loadFromData(self.result_str)
                        self.screenshot.setPixmap(self.pixmap)
                if save_loop >= zeit_s:
                    self.SCrun_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
                    getattr(self, "CH_Text_" + str(i_ein)).setStyleSheet("background-color: #000000; color: #ffffff;")
                    getattr(self, "CH_Text_" + str(i_ein)).setText(zwso)
                    if getattr(self, "CH_comboBox_" + str(i)).currentText() == "ACI" and aci_first == 0:
                        instr.write("ROUTe:STARt OFF", encoding='utf-8')
                        aci_first = 1
                        instr.write("ROUTe:DEL MIN", encoding='utf-8')
                        instr.write("ROUT:LIMI:LOW "+str(i_ein), encoding='utf-8')
                        instr.write("ROUT:LIMI:HIGH "+str(i_ein), encoding='utf-8')
                        instr.write("ROUTe:STARt ON", encoding='utf-8')
                        self.warte(3, i_ein," ")
                    break
        elif i_ein == 20:
            while True:
                now = datetime.now()
                save_timer = int(round(time.time()))
                sleep(0.333)
                if save_timer >= save_start:
                    self.scanner_widget.repaint()
                    check_loop = 0
                    save_start = int(round(time.time())) + save_intervall
                    self.SCrun_Button.setProperty("text",b_text+"\n"+str(int(zeit_s - save_loop)) + " s")
                    self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
                    self.lcdNumber.setText("Countdown: "+ str(int(zeit_s - save_loop)))
                    self.lcdText1.setText("s")
                    self.scanner_widget.repaint()
                    if scan_loop == 2:
                        self.SCloop_Button.setProperty("text","Scanner Loop\n"+str(int(scan_timer - save_timer)) + " s")
                    self.scanner_widget.repaint()
                    self.frame.repaint()
                    save_loop += 1
                    if shot == 1:
                        instr.write("SCDP")
                        self.result_str = instr.read_raw()
                        self.pixmap.loadFromData(self.result_str)
                        self.screenshot.setPixmap(self.pixmap)
                if save_loop >= zeit_s:
                    self.SCrun_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
                    break

    def check_wert(self, zahl):
        if zahl < 0:
            zahl *= -1
        divisor = 1
        hugo = ''
        if zahl <= 0.0000000002:
            hugo = "p"
            divisor = 1000000000000
        elif zahl <= 0.0000002:
            hugo = "n"
            divisor = 1000000000
        elif zahl <= 0.0002:
            hugo = "µ"
            divisor = 1000000
        elif zahl <= 0.002:
            hugo = "µ"
            divisor = 1000000
        elif zahl <= 0.02:
            hugo = "m"
            divisor = 1000
        elif zahl <= 0.2:
            hugo = "m"
            divisor = 1000
        elif zahl <= 2:
            hugo = ""
            divisor = 1
        elif zahl >= 2000:
            hugo = "k"
            divisor = 0.001
        elif zahl >= 2000000:
            hugo = "M"
            divisor = 0.000001
        elif zahl > 9.9E+31:
            hugo = ""
            divisor = 1
        return(hugo, divisor)

    def save_change(self):
        global sa_timer, sa_intervall, sa_start
        sa_intervall = int(self.intervall_box.currentText().replace(' s', ''))
        sa_start = int(round(time.time()))

    def G_change(self):
        global G_timer, G_intervall, G_start
        G_intervall = int(self.G_intervall_box.currentText().replace(' s', ''))
        G_start = int(round(time.time()))

    def save(self):
        global format_date, format_time, sa_flag, sa_timer, sa_intervall, fileName, wb_row, wb_col, format_date, format_time, workbook, worksheet
        fileName = ""
        if sa_flag == 0:
            options = QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self,"Log-Datei speichern","dmmChannel.xlsx","Alle Files (*);;Text Files (*.xlsx)", options=options)
            if fileName:
                self.Save_Button.setStyleSheet("background-color: #5a5a5a; color: #aa0000;")
                sa_flag = 1
                workbook = xlsxwriter.Workbook(fileName)
                worksheet = workbook.add_worksheet()
                worksheet.set_column('A1:AH', 12)

                worksheet.write(0,0, 'Date')
                worksheet.write(0,1, 'Time')
                worksheet.write(0,2, 'Channel 01')
                worksheet.write(0,4, 'Channel 02')
                worksheet.write(0,6, 'Channel 03')
                worksheet.write(0,8, 'Channel 04')
                worksheet.write(0,10, 'Channel 05')
                worksheet.write(0,12, 'Channel 06')
                worksheet.write(0,14, 'Channel 07')
                worksheet.write(0,16, 'Channel 08')
                worksheet.write(0,18, 'Channel 09')
                worksheet.write(0,20, 'Channel 10')
                worksheet.write(0,22, 'Channel 11')
                worksheet.write(0,24, 'Channel 12')
                worksheet.write(0,26, 'Channel 13')
                worksheet.write(0,28, 'Channel 14')
                worksheet.write(0,30, 'Channel 15')
                worksheet.write(0,32, 'Channel 16')

                wb_row = 1
                format_date = workbook.add_format({'num_format': 'dd.mm.yyyy'})
                format_time = workbook.add_format({'num_format': 'hh:mm:ss'})
#                self.SCloop_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
                self.SCloop_all_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
                self.SCrun_Button.setVisible(False)
            elif fileName == '':
                sa_flag = 0
                return 0
        elif sa_flag == 1:
            sa_flag = 0
            self.Save_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            workbook.close()

    def scshot(self):
        global shot, graph, scanner
        if shot == 0:
            shot = 1
            self.SCShot_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            self.SCShot_Button.setProperty("text","Live SC-Shot\nOff")
            self.setFixedSize(1262, 304)        # breit mit SC
            self.graph_frame.setFixedWidth(1241)
            self.graph_frame.setFixedHeight(459)
            self.graph_frame.setMaximumWidth(1241)
            self.graph_frame.setMaximumHeight(459)
            self.graphWidget.setFixedWidth(1234)
            self.graphWidget.setFixedHeight(453)
            self.graphWidget.setMaximumWidth(1234)
            self.graphWidget.setMaximumHeight(453)
            if graph == 1 or scanner == 1:
                self.setFixedSize(1262, 776)
            elif graph == 0 and scanner == 0:
                self.setFixedSize(1262, 304)
        elif shot == 1:
            shot = 0
            self.SCShot_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            self.SCShot_Button.setProperty("text","Live SC-Shot\nOn")
            self.setFixedSize(766, 304)         # klein ohne SC
            self.graph_frame.setFixedWidth(746)
            self.graph_frame.setFixedHeight(459)
            self.graph_frame.setMaximumWidth(746)
            self.graph_frame.setMaximumHeight(459)
            self.graphWidget.setFixedWidth(739)
            self.graphWidget.setFixedHeight(453)
            self.graphWidget.setMaximumWidth(739)
            self.graphWidget.setMaximumHeight(453)
            if graph == 1 or scanner == 1:
                self.setFixedSize(766, 776)
            elif graph == 0 and scanner == 0:
                self.setFixedSize(766, 304)

    def exit(self):
        self.close()

    def db_change(self, dx):
        self.combobox_db.setCurrentIndex(dx)
        
    def ntc(self):
        global ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner
        if ntc_switch == 0 and check_loop == 0:
            self.res()
            self.PTC_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            ntc_switch = 1
            check_loop = 1
            self.lcdDual.setVisible(True)
            self.F1_Button.setVisible(False)
        if ntc_switch == 1 and check_loop == 0:
            self.PTC_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            check_loop = 1
            ntc_switch = 0
            self.F1_Button.setVisible(True)
            self.PTC_Button.setVisible(False)
            self.lcdDual.setVisible(False)
            instr.write(funktion_set , encoding='utf-8')
#            self.res()

    def runstop(self):
        global run_stop, check_loop
        if run_stop == 1 and check_loop == 0:
            self.run_stop_Button.setText("STOP")
            self.run_stop_Button.setStyleSheet("background-color: #5a5a5a; color: #880000;")
            run_stop = 0
            check_loop = 1
        if ntc_switch == 0 and check_loop == 0:
            self.run_stop_Button.setText("RUN")
            self.run_stop_Button.setStyleSheet("background-color: #5a5a5a; color: #00aa00;")
            run_stop = 1
            check_loop = 1

    def temp_ntc(self, wert_temp):
        ntcNominal = 10000  #         // Widerstand des NTC bei Nominaltemperatur
        tempNominal = 25    #         // Temperatur bei der der NTC den angegebenen Widerstand hat
        bCoefficient = 3977 #         // Beta Coefficient (B25 aus Datenblatt des NTC)
        serienWiederstand = 0   # // Wert des Widerstandes der mit dem NTC in Serie geschaltet ist
        temp = (wert_temp*1000) / ntcNominal      # (R/Ro)
        temp = np.log(temp)                      # ln(R/Ro)
        temp /= bCoefficient                  # 1/B * ln(R/Ro)
        temp += 1.0 / (tempNominal + 273.15)  # + (1/To)
        temp = 1.0 / temp                     # Invertieren
        temp -= 273.15                        # Umwandeln in °C
        return (temp)
    
    def multi(self):
        global graph, scanner, shot
        if scanner == 0:
            scanner = 1
            self.SC_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            self.scanner_widget.setVisible(True)
            self.graph_frame.setVisible(False)
            self.setFixedSize(766, 776)         # hoch ohne SC
            self.graph_frame.setFixedWidth(746)
            self.graph_frame.setFixedHeight(459)
            self.graph_frame.setMaximumWidth(746)
            self.graph_frame.setMaximumHeight(459)
            self.graphWidget.setFixedWidth(739)
            self.graphWidget.setFixedHeight(453)
            self.graphWidget.setMaximumWidth(739)
            self.graphWidget.setMaximumHeight(453)
            if shot == 1:
                self.setFixedSize(1262, 776)        # breit und hoch mit SC
                self.graph_frame.setFixedWidth(1241)
                self.graph_frame.setFixedHeight(459)
                self.graph_frame.setMaximumWidth(1241)
                self.graph_frame.setMaximumHeight(459)
                self.graphWidget.setFixedWidth(1234)
                self.graphWidget.setFixedHeight(453)
                self.graphWidget.setMaximumWidth(1234)
                self.graphWidget.setMaximumHeight(453)
        elif scanner == 1:
            scanner = 0
            self.scanner_widget.setVisible(False)
            self.graph_frame.setVisible(True)
            self.SC_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            if graph == 1 and shot == 1:
                self.setFixedSize(1262, 776)
            if graph == 1 and shot == 0:
                self.setFixedSize(766, 776)
            if graph == 0 and shot == 0:
                self.setFixedSize(766, 304)
            if graph == 0 and shot == 1:
                self.setFixedSize(1262, 304)

    def buttons_off(self):
        global save_timer, save_intervall, save_start, scanner_run, scanner_on, scanner_auswahl, scanner_auswahl_i, ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, CAP_display, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner
        self.vdc_Button.setStyleSheet("background:rgb(255,255,255)")
        self.vac_Button.setStyleSheet("background:rgb(255,255,255)")
        self.per_Button.setStyleSheet("background:rgb(255,255,255)")
        self.hz_Button.setStyleSheet("background:rgb(255,255,255)")
        self.adc_Button.setStyleSheet("background:rgb(255,255,255)")
        self.aac_Button.setStyleSheet("background:rgb(255,255,255)")
        self.ohm_Button.setStyleSheet("background:rgb(255,255,255)")
        self.diod_Button.setStyleSheet("background:rgb(255,255,255)")
        self.cap_Button.setStyleSheet("background:rgb(255,255,255)")
        self.cont_Button.setStyleSheet("background:rgb(255,255,255)")
        self.temp_Button.setStyleSheet("background:rgb(255,255,255)")
        self.db_widget.setVisible(False)

    def limit(self):
        global wert_limit, limit_switch, low_fail, up_fail, upper, lower, upper_val, lower_val, wert, funktion
        kill_txt = ['V', 'A', 'F', 'Hz', 's', '♪', ' ', 'Ω', '↓', '↑', 'C', 'F', 'K', '°', 'D', 's']
        if limit_switch == 0:
          self.u_limit_calc_num.setVisible(True)
          self.l_limit_calc_num.setVisible(True)
          if self.u_limit_calc.text() == "" and self.l_limit_calc.text() == "":
            self.u_limit_calc.setText(str(round(wert+(wert/100*0.025),4)) + funktion)
            self.l_limit_calc.setText(str(round(wert-(wert/100*0.025),4)) + funktion)
          if self.u_limit_calc.text() != "" and self.l_limit_calc.text() != "":
            self.limit_Button.setText("Limit On\nOff")
            self.limit_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            upper = self.u_limit_calc.text()
            lower = self.l_limit_calc.text()
            upper = upper.replace(',', '.')
            lower = lower.replace(',', '.')
            for i in range(len(kill_txt)):
                upper = upper.replace(kill_txt[i], '')
            for i in range(len(kill_txt)):
                lower = lower.replace(kill_txt[i], '')
            if "G" not in lower and "M" not in lower and "k" not in lower and "m" not in lower and "µ" not in lower and "u" not in lower and "n" not in lower and "p" not in lower:
                lower_val = round(float(lower),9)
            if "G" not in upper and "M" not in upper and "k" not in upper and "m" not in upper and "µ" not in upper and "u" not in upper and "n" not in upper and "p" not in upper:
                upper_val = round(float(upper),9)
            if "G" in lower:
                lower = lower.replace('G', '')
                lower_val = round(float(lower)*1e+9,9)
            if "G" in upper:
                upper = upper.replace('G', '')
                upper_val = round(float(upper)*1e+9,9)
            if "M" in lower:
                lower = lower.replace('M', '')
                lower_val = round(float(lower)*1e+6,9)
            if "M" in upper:
                upper = upper.replace('M', '')
                upper_val = round(float(upper)*1e+6,9)
            if "k" in lower:
                lower = lower.replace('k', '')
                lower_val = round(float(lower)*1e+3,9)
            if "k" in upper:
                upper = upper.replace('k', '')
                upper_val = round(float(upper)*1e+3,9)
            if "m" in lower:
                lower = lower.replace('m', '')
                lower_val = round(float(lower)*1e-3,9)
            if "m" in upper:
                upper = upper.replace('m', '')
                upper_val = round(float(upper)*1e-3,9)
            if "µ" in lower or "u" in lower:
                lower = lower.replace('u', '')
                lower = lower.replace('µ', '')
                lower_val = round(float(lower)*1e-6,9)
            if "µ" in upper or "u" in upper:
                upper = upper.replace('u', '')
                upper = upper.replace('µ', '')
                upper_val = round(float(upper)*1e-6,9)
            if "n" in lower:
                lower = lower.replace('n', '')
                lower_val = round(float(lower)*1e-9,10)
            if "n" in upper:
                upper = upper.replace('n', '')
                upper_val = round(float(upper)*1e-9,10)
            if "p" in lower:
                lower = lower.replace('p', '')
                lower_val = round(float(lower)*1e-12,13)
            if "p" in upper:
                upper = upper.replace('p', '')
                upper_val = round(float(upper)*1e-12,13)
#            print (upper_val,lower_val) 
            instr.write('CALCulate:LIMit:CLEar')
            instr.write('CALC:LIM:LOW '+ str(lower_val))
            instr.write('CALC:LIM:UPP '+ str(upper_val))
            lower_val = float(instr.ask('CALC:LIM:LOW?'))
            upper_val = float(instr.ask('CALC:LIM:UPP?'))
            instr.write('CALCulate:LIMit:STATe ON')
            instr.write('INITiate')
            limit_switch = 1
        elif limit_switch == 1:
            self.u_limit_calc_num.setVisible(False)
            self.l_limit_calc_num.setVisible(False)
            self.u_limit_calc.setStyleSheet("background-color: #464646; color: #ffffff; border: 1px solid white;")
            self.l_limit_calc.setStyleSheet("background-color: #464646; color: #ffffff; border: 1px solid white;")
            instr.write('CALCulate:LIMit:STATe OFF')
            instr.write('CALC:CLE:IMM')
            instr.write('CALCulate:LIMit:CLEar')
            limit_switch = 0
            low_fail = 0
            up_fail = 0
            self.limit_Button.setText("Limit Off\nOn")
            self.limit_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            self.u_limit_calc_num.setProperty("text", "")
            self.l_limit_calc_num.setProperty("text", "")    
            self.u_limit_calc.setProperty("text", "")
            self.l_limit_calc.setProperty("text", "")    
            self.u_limit_calc.setProperty("placeholderText", "Upper Limit")
            self.l_limit_calc.setProperty("placeholderText", "Lower Limit")

    def limit_off(self):
        global limit_switch, low_fail, up_fail, upper, lower, upper_val, lower_val, wert, funktion
        self.u_limit_calc_num.setVisible(False)
        self.l_limit_calc_num.setVisible(False)
        self.u_limit_calc.setStyleSheet("background-color: #464646; color: #ffffff; border: 1px solid white;")
        self.l_limit_calc.setStyleSheet("background-color: #464646; color: #ffffff; border: 1px solid white;")
        instr.write('CALCulate:LIMit:STATe OFF')
        instr.write('CALC:CLE:IMM')
        instr.write('CALCulate:LIMit:CLEar')
        limit_switch = 0
        low_fail = 0
        up_fail = 0
        self.limit_Button.setText("Limit Off\nOn")
        self.limit_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
        self.u_limit_calc_num.setProperty("text", "")
        self.l_limit_calc_num.setProperty("text", "")    
        self.u_limit_calc.setProperty("text", "")
        self.l_limit_calc.setProperty("text", "")    
        self.u_limit_calc.setProperty("placeholderText", "Upper Limit")
        self.l_limit_calc.setProperty("placeholderText", "Lower Limit")

    def f1_click(self):
        global db_switch, db_bak, fi_start, null_ref, null_switch, check_loop, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, wert
        if funktion_raw == 'VOLT' and check_loop == 0:
            if db_switch == 0:
                check_loop = 1
                db_switch = 1
            elif db_switch == 1:
                check_loop = 1
                db_switch = 0
        if funktion_raw == 'VOLT:AC' and check_loop == 0:
            if db_switch == 0:
                check_loop = 1
                db_switch = 1
            elif db_switch == 1:
                check_loop = 1
                db_switch = 0

    def f2_click(self):
        global check_loop, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, rad, komma, komma_plus, nk, mess_art
#        print ("F2:"+funktion_raw)
        if funktion_raw == 'TEMP':
            nk = 2
            instr.write("UNIT:TEMP C", encoding='utf-8')

    def f3_click(self):
        global check_loop, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, wert
        if funktion_raw == 'TEMP':
            nk = 2
            instr.write("UNIT:TEMP F", encoding='utf-8')
        if funktion_raw == 'VOLT' and check_loop == 0:
            if DC_filter == 0:
                check_loop = 1
                DC_filter = 1
                instr.write("VOLT:FILT ON", encoding='utf-8')
            elif DC_filter == 1:
                check_loop = 1
                DC_filter = 0
                instr.write("VOLT:FILT OFF", encoding='utf-8')
        if funktion_raw == 'CURR' and check_loop == 0:
            if DC_filter == 0:
                check_loop = 1
                DC_filter = 1
                instr.write("CURR:FILT ON", encoding='utf-8')
            elif DC_filter == 1:
                check_loop = 1
                DC_filter = 0
                instr.write("CURR:FILT OFF", encoding='utf-8')

    def f4_click(self):
        global null_ref, null_switch, check_loop, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, wert
        if funktion_raw == 'TEMP':
            nk = 3
            instr.write("UNIT:TEMP K", encoding='utf-8')
        if funktion_raw == 'VOLT' and check_loop == 0:
            if iz_filter == 0:
                check_loop = 1
                iz_filter = 1
                instr.write("VOLT:DC:IMP 10G", encoding='utf-8')
            elif iz_filter == 1:
                check_loop = 1
                iz_filter = 0
                instr.write("VOLT:DC:IMP 10M", encoding='utf-8')
                instr.write("CONF:"+funktion_raw+" AUTO", encoding='utf-8')
                self.rad()

    def f6_click(self):
        global null_ref, null_switch, check_loop, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, wert
        if null_switch == 0:
            instr.write(funktion_raw+":NULL:STAT ON", encoding='utf-8')
            null_ref = wert
            null_switch = 1
        elif null_switch == 1:
            instr.write(funktion_raw+":NULL:STAT OFF", encoding='utf-8')
            null_switch = 0

    def null_off(self):
        global null_ref, null_switch, check_loop, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, wert
        instr.write(funktion_raw+":NULL:STAT OFF", encoding='utf-8')
        null_switch = 0

    def get_funktion(self):
        global check_loop, run_stop, db_switch, db_bak, null_ref, null_switch, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, CAP_display, DC_filter, iz_filter, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, wert
        if dot_on == 0:
            dot_on = 1
            self.LCD_Dot.setProperty("text", "●") # ● ◉ █
        elif dot_on == 1:
            dot_on = 0
            self.LCD_Dot.setProperty("text", "◉")
        funktion = instr.ask("CONFigure?", encoding='utf-8')
        scan_text = funktion.split(' ')
        scan_text[0] = scan_text[0].replace('\"', '')
        funktion = scan_text[0]
        funktion_raw = funktion
        bereich = ""
        if len(scan_text) > 1:
            scan_text[1] = scan_text[1].replace('\"', '')
            werte = scan_text[1].split(',')
            scan_text[1] = werte[0]
            bereich_raw = round(float(scan_text[1]), 9)
            hugo = self.check_wert(bereich_raw)
            bereich_raw_auto = str(int(bereich_raw * hugo[1]))+hugo[0]
#            print(hugo, bereich_raw)
        if null_switch == 0:
            self.F6_Button.setProperty("text","Rel. Off\nOn")
            self.F6_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
        elif null_switch == 1:
            self.F6_Button.setProperty("text","Rel. On\nOff")
            self.F6_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
        if funktion != "RES":
            self.F1_Button.setVisible(True)
            self.PTC_Button.setVisible(False)
        if funktion == "VOLT":
            if db_switch == 0:
                self.F1_Button.setProperty("text","dBM Off\nOn")
                self.F1_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
                self.db_widget.setVisible(False)
                self.dbText.setVisible(False)
            if db_switch == 1:
                self.F1_Button.setProperty("text","dBM On\nOff")
                self.F1_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
                self.db_widget.setVisible(True)
                self.dbText.setVisible(True)
            mess_art = 'DC Voltage'
            nk = 0
            bereich = "Auto "+str(bereich_raw_auto) + "V"
            self.F4_Button.setProperty("text"," ")
            if int(self.dial.value()) > 0:
                bereich = "Manual " + VDC[int(self.dial.value())]
            if bereich_raw == 0.2:
                nk = 2
                funktion="mV DC"
                if iz_filter == 0 and int(self.dial.value()) > 0:
                    self.F4_Button.setProperty("text","Input Z 10M\n10G")
                    self.F4_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
                elif iz_filter == 1 and int(self.dial.value()) > 0:
                    self.F4_Button.setProperty("text","Input Z 10G\n10M")
                    self.F4_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            elif bereich_raw == 2.0:
                nk = 0
                funktion="V DC"
                if iz_filter == 0 and int(self.dial.value()) > 0:
                    self.F4_Button.setProperty("text","Input Z 10M\n10G")
                    self.F4_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
                elif iz_filter == 1 and int(self.dial.value()) > 0:
                    self.F4_Button.setProperty("text","Input Z 10G\n10M")
                    self.F4_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            elif bereich_raw == 20.0:
                nk = 1
                funktion="V DC"
            elif bereich_raw == 200.0:
                nk = 2
                funktion="V DC"
            elif bereich_raw == 1000.0:
                nk = 3
                funktion="V DC"
            self.F2_Button.setProperty("text","")
            if DC_filter == 0:
                self.F3_Button.setProperty("text","Filter Off\nOn")
                self.F3_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            if DC_filter == 1:
                self.F3_Button.setProperty("text","Filter On\nOff")
                self.F3_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
        elif funktion == "CURR":
            mess_art = 'DC Current'
            nk = 0
            bereich = "Auto "+str(bereich_raw_auto) + "A"
            self.F4_Button.setProperty("text"," ")
            if int(self.dial.value()) > 0:
                bereich = "Manual " + ADC[int(self.dial.value())]
            if bereich_raw == 0.0002:
                nk = 2
                funktion="µA DC"
            elif bereich_raw == 0.002:
                nk = 0
                funktion="mA DC"
            elif bereich_raw == 0.02:
                nk = 1
                funktion="mA DC"
            elif bereich_raw == 0.2:
                nk = 2
                funktion="mA DC"
            elif bereich_raw == 2.0:
                nk = 0
                funktion="A DC"
            elif bereich_raw == 10.0:
                nk = 1
                funktion="A DC"
            self.F1_Button.setProperty("text"," ")
            self.F2_Button.setProperty("text","")
            if DC_filter == 0:
                self.F3_Button.setProperty("text","Filter Off\nOn")
                self.F3_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            elif DC_filter == 1:
                self.F3_Button.setProperty("text","Filter On\nOff")
                self.F3_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
        elif funktion == "VOLT:AC":
            self.db_widget.setVisible(True)
            if db_switch == 0:
                self.F1_Button.setProperty("text","dBM Off\nOn")
                self.F1_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
                self.db_widget.setVisible(False)
                self.dbText.setVisible(False)
            if db_switch == 1:
                self.F1_Button.setProperty("text","dBM On\nOff")
                self.F1_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
                self.db_widget.setVisible(True)
                self.dbText.setVisible(True)
            mess_art = 'AC Voltage'
            nk = 0
            bereich = "Auto "+str(bereich_raw_auto) + "V"
            if int(self.dial.value()) > 0:
                bereich = "Manual " + VAC[int(self.dial.value())]
            if bereich_raw == 0.2:
                nk = 2
                funktion="mV AC"
            elif bereich_raw == 2.0:
                nk = 0
                funktion="V AC"
            elif bereich_raw == 20.0:
                nk = 1
                funktion="V AC"
            elif bereich_raw == 200.0:
                nk = 2
                funktion="V AC"
            elif bereich_raw == 750.0:
                nk = 2
                funktion="V AC"
            self.F2_Button.setProperty("text","")
            self.F3_Button.setProperty("text"," ")
            self.F4_Button.setProperty("text"," ")
        elif funktion == "FREQ":
            mess_art = 'Frequency'
            nk = 0
            bereich = VAC[int(self.dial.value())]
            if int(self.dial.value()) > 0:
                bereich = "Manual " + VAC[int(self.dial.value())]
            funktion="Hz"
            self.F1_Button.setProperty("text"," ")
            self.F2_Button.setProperty("text","")
            self.F3_Button.setProperty("text"," ")
            self.F4_Button.setProperty("text"," ")
        elif funktion == "PER":
            mess_art = 'Period'
            nk = 0
            bereich = VAC[int(self.dial.value())]
            if int(self.dial.value()) > 0:
                bereich = "Manual " + VAC[int(self.dial.value())]
            funktion="ms"
            self.F1_Button.setProperty("text"," ")
            self.F2_Button.setProperty("text","")
            self.F3_Button.setProperty("text"," ")
            self.F4_Button.setProperty("text"," ")
        elif funktion == "CURR:AC":
            mess_art = 'AC Current'
            nk = 0
            bereich = "Auto "+str(bereich_raw_auto) + "A"
            self.F4_Button.setProperty("text"," ")
            if int(self.dial.value()) > 0:
                bereich = "Manual " + AAC[int(self.dial.value())]
            if bereich_raw == 0.0002:
                nk = 2
                funktion="µA AC"
            elif bereich_raw == 0.002:
                nk = 0
                funktion="mA AC"
            elif bereich_raw == 0.02:
                nk = 1
                funktion="mA AC"
            elif bereich_raw == 0.2:
                nk = 2
                funktion="mA AC"
            elif bereich_raw == 2.0:
                nk = 0
                funktion="A AC"
            elif bereich_raw == 10.0:
                nk = 1
                funktion="A AC"
            self.F1_Button.setProperty("text"," ")
            self.F2_Button.setProperty("text","")
            self.F2_Button.setProperty("text","")
            self.F3_Button.setProperty("text"," ")
            self.F4_Button.setProperty("text"," ")
        elif funktion == "TEMP":
            mess_art = 'Temperature'
            self.F2_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            self.F3_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            self.F4_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            self.dial.setRange(0,9)
            self.dial.setProperty("toolTip", "Sensor " + str(TEMP_RDT_TYPE))
            self.lcd_dial.setProperty("text", TEMP_RDT_TYPE[int(self.dial.value())])
            bereich = TEMP_RDT_TYPE[int(self.dial.value())]
            temp_unit = instr.ask("UNIT:TEMPerature?", encoding='utf-8')
            if temp_unit == 'C':
                funktion="°"+temp_unit
                self.F2_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            elif temp_unit == 'F':
                funktion="°"+temp_unit
                self.F3_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            elif temp_unit == 'K':
                funktion=temp_unit
                self.F4_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
#            self.F1_Button.setVisible(False)
            self.F1_Button.setProperty("text"," ")
#            self.PTC_Button.setVisible(True)
            self.F2_Button.setProperty("text","Unit\n°C")
            self.F3_Button.setProperty("text","Unit\n°F")
            self.F4_Button.setProperty("text","Unit\nK")
        elif funktion == "RES":
            mess_art = '2 Wire Resistance'
            nk = 0
            bereich = "Auto "+str(bereich_raw_auto) + "Ω"
            if bereich_raw == 2000:
                bereich = "Auto "+str(bereich_raw/1000) + "kΩ"
            elif bereich_raw == 20000:
                bereich = "Auto "+str(bereich_raw/1000) + "kΩ"
            elif bereich_raw == 200000:
                bereich = "Auto "+str(bereich_raw/1000) + "kΩ"
            elif bereich_raw >= 2000000:
                bereich = "Auto "+str(bereich_raw/1000000) + "MΩ"
            if int(self.dial.value()) > 0:
                bereich = "Manual " + RES_display[int(self.dial.value())]
            if bereich_raw == 200.0:
                nk = 2
                funktion="Ω"
            elif bereich_raw == 2000.0:
                nk = 0
                funktion="kΩ"
            elif bereich_raw == 20000.0:
                nk = 1
                funktion="kΩ"
            elif bereich_raw == 200000.0:
                nk = 2
                funktion="kΩ"
            elif bereich_raw == 2000000.0:
                nk = 0
                funktion="MΩ"
            elif bereich_raw == 10000000.0:
                nk = 1
                funktion="MΩ"
            elif bereich_raw == 100000000.0:
                nk = 2
                funktion="MΩ"
            self.F1_Button.setVisible(False)
            self.PTC_Button.setVisible(True)
            self.F1_Button.setProperty("text"," ")
            self.F2_Button.setProperty("text","")
            self.F3_Button.setProperty("text"," ")
            self.F4_Button.setProperty("text"," ")
        elif funktion == "CAP":
            mess_art = 'Capacitance'
            nk = 0
            bereich = "Auto "+str(bereich_raw_auto) + "F"
            if int(self.dial.value()) > 0:
                bereich = "Manual " + CAP_display[int(self.dial.value())]
            if bereich_raw == 0.000000002:
                nk = 2
                funktion="nF"
            elif bereich_raw == 0.00000002:
                nk = 3
                funktion="nF"
            elif bereich_raw == 0.0000002:
                nk = 4
                funktion="nF"
            elif bereich_raw == 0.000002:
                nk = 1
                funktion="µF"
            elif bereich_raw == 0.00002:
                nk = 1
                funktion="µF"
            elif bereich_raw == 0.0002:
                nk = 1
                funktion="mF"
            elif bereich_raw == 0.01:
                nk = 2
                funktion="mF"
            self.F1_Button.setProperty("text"," ")
            self.F2_Button.setProperty("text","")
            self.F3_Button.setProperty("text"," ")
            self.F4_Button.setProperty("text"," ")
        elif funktion == "CONT":
            mess_art = 'Continuity'
            nk = 4
            bereich = "♪ < "+str(self.dial.value())+" Ω"
            funktion="Ω"
            if wert < self.dial.value():
                funktion="Ω ♪"
            self.F1_Button.setProperty("text"," ")
            self.F2_Button.setProperty("text","")
            self.F3_Button.setProperty("text"," ")
            self.F4_Button.setProperty("text"," ")
            self.F6_Button.setProperty("text"," ")
        elif funktion == "DIOD":
            mess_art = 'Diode'
            nk = 4
            bereich = "♪ < "+str(self.dial.value()/10)+" V"
            funktion="V DC"
            if wert < self.dial.value()/10:
                funktion="V ♪"
            self.F1_Button.setProperty("text"," ")
            self.F2_Button.setProperty("text","")
            self.F3_Button.setProperty("text"," ")
            self.F4_Button.setProperty("text"," ")
            self.F6_Button.setProperty("text"," ")

    def graphic(self):
        global G_timer, G_intervall, G_start, shot, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, wert

        if int(graph) == 0:
            self.F5_Button.setProperty("text","Graph On\nOff")
            self.F5_Button.setStyleSheet("background-color: #5a5a5a; color: #80ff80;")
            G_start = int(round(time.time())) + G_intervall
            if shot == 1:
                self.setFixedSize(1262, 776)
                self.graph_frame.setFixedWidth(1241)
                self.graph_frame.setFixedHeight(459)
                self.graph_frame.setMaximumWidth(1241)
                self.graph_frame.setMaximumHeight(459)
                self.graphWidget.setFixedWidth(1234)
                self.graphWidget.setFixedHeight(453)
                self.graphWidget.setMaximumWidth(1234)
                self.graphWidget.setMaximumHeight(453)
            elif shot == 0:
                self.setFixedSize(766, 776)         # klein ohne SC
                self.graph_frame.setFixedWidth(746)
                self.graph_frame.setFixedHeight(459)
                self.graph_frame.setMaximumWidth(746)
                self.graph_frame.setMaximumHeight(459)
                self.graphWidget.setFixedWidth(739)
                self.graphWidget.setFixedHeight(453)
                self.graphWidget.setMaximumWidth(739)
                self.graphWidget.setMaximumHeight(453)


            now = datetime.now()
            timestamp1 = "%02d:%02d:%02d" % (now.hour, now.minute, now.second)

            pen = pg.mkPen(color=(0, 0, 0), width=2)
            self.graphWidget.setBackground((170, 255, 0))
            self.graphWidget.setTitle("Siglent SDM 3055-SC ", color="b", size="10pt")
            styles = {"color": "#000", "font-size": "10px"}
            styles1 = {"color": "#000", "font-size": "14px"}
            axis = pg.DateAxisItem(orientation='bottom')
            self.graphWidget.setAxisItems({"bottom": axis})
            self.graphWidget.setLabel("left", funktion, **styles1)
            self.graphWidget.setLabel("bottom", "Time", **styles)
            self.graphWidget.showGrid(x=True, y=True, alpha=1.0)
            self.graphWidget.enableAutoRange()
            self.graphWidget.hideButtons()
            x_str = [timestamp1 for x_str in range(max_graph)]
            self.graphWidget.clear()
            mess_alt = funktion_raw
            xy_counter = max_graph -1
            messungen = 0
            max_mess = 0
            min_mess = 0
            x = [time.time() for x in range(max_graph)]

            y = np.zeros(max_graph)
            x[xy_counter] = time.time()
            y[xy_counter] = wert
            self.G_intervall_box.setVisible(False)
            self.G_iText.setVisible(False)
            graph = 1
        elif int(graph) == 1:
            xy_counter = 0
            messungen = 0
            mess_alt = ''
            self.F5_Button.setProperty("text","Graph Off\nOn")
            self.F5_Button.setStyleSheet("background-color: #5a5a5a; color: #ffffff;")
            self.G_intervall_box.setVisible(True)
            self.G_iText.setVisible(True)
            graph = 0
            if scanner == 1 and shot == 1:
                self.setFixedSize(1262, 776)
            if scanner == 1 and shot == 0:
                self.setFixedSize(766, 776)
            if scanner == 0 and shot == 0:
                self.setFixedSize(766, 304)
            if scanner == 0 and shot == 1:
                self.setFixedSize(1262, 304)

    def rad(self):
        global VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        self.dial.setNotchesVisible(True)
        rad = self.dial.value()
#        print ("CONF:"+funktion_raw, rad)
        if funktion_raw == "VOLT" and rad < 10:
            if int(rad) == 0:
                instr.write("CONF:"+funktion_raw, encoding='utf-8')
            elif int(rad) >= 1:
                instr.write("CONF:"+funktion_raw+" "+VDC[rad], encoding='utf-8')
            self.lcd_dial.setProperty("text", VDC[int(self.dial.value())])
        elif funktion_raw == "VOLT:AC" and rad < 10:
            if int(rad) == 0:
                instr.write("CONF:"+funktion_raw, encoding='utf-8')
            elif int(rad) >= 1:
                instr.write("CONF:"+funktion_raw+" "+VAC[rad], encoding='utf-8')
            self.lcd_dial.setProperty("text", VAC[int(self.dial.value())])
        elif funktion_raw == "CURR" and rad < 10:
            if int(rad) == 0:
                instr.write("CONF:"+funktion_raw, encoding='utf-8')
            elif int(rad) >= 1:
                instr.write("CONF:"+funktion_raw+" "+ADC[rad], encoding='utf-8')
            self.lcd_dial.setProperty("text", ADC[int(self.dial.value())])
        elif funktion_raw == "CURR:AC" and rad < 10:
            if int(rad) == 0:
                instr.write("CONF:"+funktion_raw, encoding='utf-8')
            elif int(rad) >= 1:
                instr.write("CONF:"+funktion_raw+" "+AAC[rad], encoding='utf-8')
            self.lcd_dial.setProperty("text", AAC[int(self.dial.value())])
        elif funktion_raw == "CAP" and rad < 10:
            if int(rad) == 0:
                instr.write("CONF:"+funktion_raw, encoding='utf-8')
            elif int(rad) >= 1:
                instr.write("CONF:"+funktion_raw+" "+CAP[rad], encoding='utf-8')
            self.lcd_dial.setProperty("text", CAP_display[int(self.dial.value())])
        elif funktion_raw == "PER" and rad < 10:
            if int(rad) == 0:
                instr.write("CONF:"+funktion_raw+"\n"+funktion_raw+":VOLT:RANGE", encoding='utf-8')
            elif int(rad) >= 1:
                instr.write("CONF:"+funktion_raw+"\n"+funktion_raw+":VOLT:RANGE "+VAC[rad], encoding='utf-8')
            self.lcd_dial.setProperty("text", VAC[int(self.dial.value())])
        elif funktion_raw == "FREQ" and rad < 10:
            if int(rad) == 0:
                instr.write("CONF:"+funktion_raw+"\n"+funktion_raw+":VOLT:RANGE", encoding='utf-8')
            elif int(rad) >= 1:
                instr.write("CONF:"+funktion_raw+"\n"+funktion_raw+":VOLT:RANGE "+VAC[rad], encoding='utf-8')
            self.lcd_dial.setProperty("text", VAC[int(self.dial.value())])
        elif funktion_raw == "RES" and rad < 10:
            if int(rad) == 0:
                instr.write("CONF:"+funktion_raw+"\n"+funktion_raw+":RANGE", encoding='utf-8')
            elif int(rad) >= 1:
                instr.write("CONF:"+funktion_raw+"\n"+funktion_raw+":RANGE "+RES[rad].replace('Ω', ''), encoding='utf-8')
            self.lcd_dial.setProperty("text", RES_display[int(self.dial.value())])
        elif funktion_raw == "CONT":
            self.lcd_dial.setProperty("text", str(self.dial.value())+' Ω')
            instr.write("CONT:THR:VAL "+str(int(self.dial.value())), encoding='utf-8')
        elif funktion_raw == "DIOD":
            self.lcd_dial.setProperty("text", str(self.dial.value()/10)+' V')
            instr.write("DIOD:THR:VAL "+str(int(self.dial.value())/10), encoding='utf-8')
        elif funktion_raw == "TEMP" and rad < 10:
            if int(rad) <= 7:
                instr.write("CONF:"+funktion_raw+" THER,"+TEMP_RDT_TYPE[rad], encoding='utf-8')
                funktion_set = "CONF:"+funktion_raw+" THER,"+TEMP_RDT_TYPE[rad]
            elif int(rad) >= 8:
                instr.write("CONF:"+funktion_raw+" RTD,"+TEMP_RDT_TYPE[rad], encoding='utf-8')
                funktion_set = "CONF:"+funktion_raw+" RTD,"+TEMP_RDT_TYPE[rad]
            self.lcd_dial.setProperty("text", TEMP_RDT_TYPE[int(self.dial.value())])

    def vdc(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        self.limit_widget.setVisible(True)
        self.buttons_off()
        self.limit_off()
        db_switch = 0
        self.vdc_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,5)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(VDC))
        self.lcd_dial.setProperty("text", VDC[int(self.dial.value())])
        instr.write("CONF:VOLT", encoding='utf-8')
        instr.write("TRIGger:DELay:AUTO ON", encoding='utf-8')
        instr.write("VOLT:FILT ON", encoding='utf-8')
        sleep(0.1)
        instr.write("VOLT:FILT OFF", encoding='utf-8')
        funktion_set = "CONF:VOLT"

    def adc(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        db_switch = 0
        self.limit_widget.setVisible(True)
        self.limit_off()
        self.buttons_off()
        self.adc_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,6)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(ADC))
        self.lcd_dial.setProperty("text", ADC[int(self.dial.value())])
        instr.write("CONF:CURR:DC", encoding='utf-8')
        instr.write("TRIGger:DELay:AUTO ON", encoding='utf-8')
        funktion_set = "CONF:CURR"

    def vac(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        db_switch = 0
        self.limit_widget.setVisible(True)
        self.limit_off()
        self.buttons_off()
        self.vac_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,5)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(VAC))
        self.lcd_dial.setProperty("text", VAC[int(self.dial.value())])
        instr.write("CONF:VOLT:AC", encoding='utf-8')
        instr.write("TRIGger:DELay:AUTO ON", encoding='utf-8')
        funktion_set = "CONF:VOLT:AC"

    def aac(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        db_switch = 0
        self.limit_widget.setVisible(True)
        self.limit_off()
        self.buttons_off()
        self.aac_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,4)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(AAC))
        self.lcd_dial.setProperty("text", AAC[int(self.dial.value())])
        instr.write("CONF:CURR:AC", encoding='utf-8')
        instr.write("TRIGger:DELay:AUTO ON", encoding='utf-8')
        funktion_set = "CONF:CURR:AC"

    def hz(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        db_switch = 0
        self.limit_widget.setVisible(True)
        self.limit_off()
        self.buttons_off()
        self.hz_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,5)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(VAC))
        self.lcd_dial.setProperty("text", VAC[int(self.dial.value())])
        instr.write("CONF:FREQ", encoding='utf-8')
        funktion_set = "CONF:FREQ"

    def per(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        db_switch = 0
        self.limit_widget.setVisible(True)
        self.limit_off()
        self.buttons_off()
        self.per_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,5)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(VAC))
        self.lcd_dial.setProperty("text", VAC[int(self.dial.value())])
        instr.write("CONF:PER", encoding='utf-8')
        funktion_set = "CONF:PER"

    def res(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        db_switch = 0
        self.limit_widget.setVisible(True)
        self.limit_off()
        self.buttons_off()
        self.ohm_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,7)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(RES_display))
        self.lcd_dial.setProperty("text", RES_display[int(self.dial.value())])
        instr.write("CONF:RES AUTO", encoding='utf-8')
        instr.write("TRIGger:DELay:AUTO ON", encoding='utf-8')
        funktion_set = "CONF:RES"

    def cont(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        db_switch = 0
        self.limit_widget.setVisible(False)
        self.limit_off()
        self.buttons_off()
        self.cont_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,20)
        self.dial.setValue(4)
        self.dial.setProperty("toolTip", "Range 0 Ω ... 20 Ω")
        self.lcd_dial.setProperty("text", str(self.dial.value())+' Ω')
        instr.write("CONT:THR:VAL "+str(self.dial.value())+"\nCONT:VOL:STAT HIGH\nCONF:CONT", encoding='utf-8')
        instr.write("TRIGger:DELay 0.1", encoding='utf-8')
        funktion_set = "CONF:CONT"

    def cap(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        self.limit_widget.setVisible(True)
        db_switch = 0
        self.limit_off()
        self.buttons_off()
        self.cap_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,7)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(CAP))
        self.lcd_dial.setProperty("text", str(self.dial.value()))
        instr.write("CONF:CAP", encoding='utf-8')
        instr.write("TRIGger:AUTO ON", encoding='utf-8')
        funktion_set = "CONF:CAP"

    def temp(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        self.limit_widget.setVisible(True)
        db_switch = 0
        self.limit_off()
        self.buttons_off()
        nk = 2
        self.temp_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,9)
        self.dial.setValue(0)
        self.dial.setProperty("toolTip", "Range " + str(TEMP_RDT_TYPE))
        self.lcd_dial.setProperty("text", TEMP_RDT_TYPE[int(self.dial.value())])
        instr.write("CONF:TEMP THER,KITS90", encoding='utf-8')
        instr.write("TRIGger:DELay:AUTO ON", encoding='utf-8')
        funktion_set = "CONF:TEMP THER,KITS90"

    def diod(self):
        global db_switch, VDC, VAC, AC, AAC, RES, TEMP_RDT_TYPE, CAP, leer, scan_text, funktion, bereich, dot_on, funktion_raw, funktion_set, rad
        self.limit_widget.setVisible(False)
        db_switch = 0
        self.limit_off()
        self.buttons_off()
        self.diod_Button.setStyleSheet("background-color:" + display_c_1 + ";")
        self.dial.setRange(0,20)
        self.dial.setValue(20)
        self.dial.setProperty("toolTip", "Range 0.0 V ... 2.0 V")
        self.lcd_dial.setProperty("text", str(self.dial.value()/10)+' V')
        instr.write("DIOD:THR:VAL "+str(self.dial.value()/10)+"\nDIOD:VOL:STAT HIGH\nCONF:DIOD", encoding='utf-8')
        instr.write("TRIGger:DELay 0.1", encoding='utf-8')
        funktion_set = "CONF:DIOD"

    def limit_show(self):
        global wert_limit, wert_raw, limit_switch, limit_disable, low_fail, up_fail, upper, lower, upper_val, lower_val, db_switch, db_bak, ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner, wert
        if limit_switch == 0 and limit_disable == 0:
            self.u_limit_calc.setProperty("placeholderText", str(round(wert_raw+(wert_raw/100*0.025),2)) + '↑')
            self.l_limit_calc.setProperty("placeholderText", str(round(wert_raw-(wert_raw/100*0.025),2)) + '↓')
            self.u_limit_calc.setStyleSheet("background-color: #484848; color: #ffffff; border: 1px solid white;")
            self.l_limit_calc.setStyleSheet("background-color: #484848; color: #ffffff; border: 1px solid white;")
        if limit_switch == 1 and limit_disable == 0:
            self.l_limit_calc.setProperty("text", str(lower_val) + '↓')
            self.u_limit_calc.setProperty("text", str(upper_val) + '↑')
            if up_fail == 0:
                self.u_limit_calc_num.setStyleSheet("background-color: #a2a2a2; color: #000000; border: 1px solid white;")
            elif up_fail > 0:
                self.u_limit_calc_num.setStyleSheet("background-color: #ffa2a2; color: #000000; border: 1px solid white;")
            if low_fail == 0:
                self.l_limit_calc_num.setStyleSheet("background-color: #a2a2a2; color: #000000; border: 1px solid white;")
            elif low_fail > 0:
                self.l_limit_calc_num.setStyleSheet("background-color: #ffa2a2; color: #000000; border: 1px solid white;")
            if wert_raw >= upper_val:
                up_fail = up_fail + 1
                self.u_limit_calc_num.setStyleSheet("background-color: #ff0000; color: #000000; border: 1px solid white;")
                self.u_limit_calc_num.setProperty("text", str(up_fail))
            elif wert_raw <= lower_val:
                low_fail = low_fail + 1
                self.l_limit_calc_num.setStyleSheet("background-color: #ff0000; color: #000000; border: 1px solid white;")
                self.l_limit_calc_num.setProperty("text", str(low_fail))

    def update(self):
        global run_stop, G_timer, G_intervall, G_start, scan_timer, scan_loop_toggle, scan_loop, wert_limit, wert_raw, limit_switch, limit_disable, low_fail, up_fail, upper, lower, upper_val, lower_val, db_switch, db_bak, ntc_wert, ntc_switch, f1_start, null_ref, null_switch, shot, check_loop, cold_boot, HOST, PORT, SCREEN, SN_SHOW, VDC, VAC, AC, AAC, RES, RES_display, TEMP_RDT_TYPE, CAP, DC_filter, iz_filter, leer, scan_text, funktion, bereich, bereich_raw, dot_on, funktion_raw, funktion_set, rad, komma, komma_plus, nk, mess_alt, x, y, messungen, graph, xy_counter, datetimes, pen, max_mess, min_mess, mess_art, scanner, wert
        now = datetime.now()
        save_timer = int(round(time.time()))
        G_timer = int(round(time.time()))
        if f1_start == 1:
            self.f1_click()
            f1_start = 0
        self.timer_single.stop()
        now = datetime.now()
        timestamp = "%02d:%02d:%02d" % (now.hour, now.minute, now.second)
        self.get_funktion()
        if cold_boot == 0 and funktion_raw != mess_alt and graph == 1:
            self.graphic()
        if cold_boot == 0 and funktion_raw != mess_alt and ntc_switch == 1:
            self.F1_Button.setVisible(True)
            self.ntc()
        if cold_boot == 0 and funktion_raw != mess_alt and null_switch == 1:
            self.f6_click()
        wert = round(float(instr.ask("READ?", encoding='utf-8')), 12)
        wert_raw = wert
        if funktion == 'Hz':
            nk = 1
            if wert >= 10000000:
                nk = 2
                funktion = 'M'+funktion
            elif wert >= 1000000:
                nk = 1
                funktion = 'M'+funktion
            elif wert >= 100000:
                nk = 3
                funktion = 'k'+funktion
            elif wert >= 10000:
                nk = 2
                funktion = 'k'+funktion
            elif wert >= 1000:
                nk = 1
                funktion = 'k'+funktion
            elif wert >= 100:
                nk = 3
            elif wert >= 10:
                nk = 2
        if funktion == 'ms':
            funktion = 's'
            nk = 1
            if wert >= 0.01:
                nk = 2
                funktion = 'm'+funktion
            elif wert >= 0.001:
                nk = 1
                funktion = 'm'+funktion
            elif wert >= 0.0001:
                nk = 3
                funktion = 'µ'+funktion
            elif wert >= 0.00001:
                nk = 2
                funktion = 'µ'+funktion
            elif wert >= 0.000001:
                nk = 1
                funktion = 'µ'+funktion
            elif wert >= 0.000000001:
                nk = 2
                funktion = 'n'+funktion
        if "M" not in funktion and "k" not in funktion and "m" not in funktion and "u" not in funktion and "µ" not in funktion and "n" not in funktion and "p" not in funktion:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
            wert_limit = ""
        elif "p" in funktion:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
            wert = round(wert*1000000000000, 5)
            wert_limit = "p"
        elif "n" in funktion:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
            wert = round(wert*1000000000, 5)
            wert_limit = "n"
        elif "u" in funktion:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
            wert = round(wert*1000000, 5)
            wert_limit = "u"
        elif "µ" in funktion:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
            wert = round(wert*1000000, 5)
            wert_limit = "u"
        elif "m" in funktion:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
            wert = round(wert*1000, 5)
            wert_limit = "m"
        elif "k" in funktion:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
            wert = round(wert/1000, 5)
            wert_limit = "k"
        elif "M" in funktion:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 60))
            wert = round(wert/1000000, 5)
            wert_limit = "M"
        fo_string = komma[nk].format(wert)
        if wert == 9.9E+31:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
            fo_string = "Open/Range ?"
        if wert == 9.9E+34:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
            fo_string = "Overload ?"
        if wert >= 9.9e+37:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
            fo_string = "Open"
        if wert >= 9.8e+40:
            self.lcdNumber.setFont(QFont('DejaVu Sans Mono', 36))
            fo_string = "Overload ?"
        if ntc_switch == 1:
            self.limit_widget.setVisible(False)
            self.F6_Button.setProperty("text"," ")
            dummy = self.temp_ntc(wert)
            wert = dummy
            self.lcdDual.setVisible(True)
            self.lcdDual.setText("Temp. NTC 10kΩ  "+fo_string+" "+funktion)
            ntc_fo_string = fo_string+" "+funktion
            fo_string = komma[2].format(dummy)
            mess_art = 'Temperature NTC 10kΩ'
            funktion = '°C'
        self.lcdNumber.setProperty("text", fo_string)
        self.lcdText2.setProperty("text", bereich)
        self.lcdText1.setProperty("text", funktion)
        if cold_boot == 1:
            cold_boot = 0
        if null_switch == 1:
            self.offsetText.setVisible(True)
            self.offsetText.setProperty("text", "Rel.0 = "+str(null_ref)+" "+funktion)
        elif null_switch == 0:
            self.offsetText.setVisible(False)
#        print ("Check ",mess_alt, funktion_raw)
        mess_alt = funktion_raw
        self.limit_show()
        if db_switch == 1:
            ref_ohm = int(self.combobox_db.currentText())
            zw = ((wert)**2)/(float(ref_ohm)*0.001)
            if zw != 0.0:
                self.db_widget.setVisible(True)
                zw = ((wert)**2)/(float(ref_ohm)*0.001)
                db = round(10*log10(zw),3)
                self.dbText.setVisible(True)
                self.dbText.setProperty("text", str(db) + 'dBm ' + str(int(ref_ohm)) + 'Ω')
            elif zw == 0.0:
                self.dbText.setVisible(False)
        elif db_switch == 0:
            self.dbText.setVisible(False)
        if int(graph) == 0 and int(G_timer - G_start) >= 0:
            G_start = int(round(time.time())) + G_intervall
            if null_switch == 0 and db_switch == 0:
                if ntc_switch == 1:
                    self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion + "; Temperature NTC 10kΩ, " + ntc_fo_string)
                elif ntc_switch == 0:
                    self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion)
            if null_switch == 1 and db_switch == 0:
                self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion + "; Rel.0 = "+str(null_ref))
            elif null_switch == 0 and db_switch == 1:
                self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion + "; " + self.dbText.text())
            elif null_switch == 1 and db_switch == 1:
                self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion + "; Rel.0 = "+str(null_ref) + "; " + self.dbText.text())
        elif int(graph) == 1 and int(G_timer - G_start) >= 0:
            G_start = int(round(time.time())) + G_intervall
            if null_switch == 0 and db_switch == 0:
                if ntc_switch == 1:
                    self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion + "; Temperature NTC 10kΩ, " + ntc_fo_string)
                elif ntc_switch == 0:
                    self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion)
            if null_switch == 1 and db_switch == 0:
                self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion + "; Rel.0 = "+str(null_ref))
            elif null_switch == 0 and db_switch == 1:
                self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion + "; " + self.dbText.text())
            elif null_switch == 1 and db_switch == 1:
                self.textEdit.append(timestamp + "; " + fo_string.replace(".", ",") + "; " + funktion + "; Rel.0 = "+str(null_ref) + "; " + self.dbText.text())
            messungen += 1
            if wert > max_mess:
                max_mess = wert + (wert * 0.25)
            if wert < min_mess:
                min_mess = wert - ((wert * 0.25) * -1)
            self.graphWidget.setYRange(min_mess, max_mess, padding=0)
            if int(messungen) >= 1:
                self.graphWidget.clear()
                x[:-1] = x[1:]
                x[-1] = time.time()
#                x_str[:-1] = x_str[1:]
#                x_str[-1] = time.time()
                y[:-1] = y[1:]
                y[-1] = wert
            if null_switch == 1:
                self.graphWidget.setTitle(mess_art+" Rel.0 = "+str(null_ref)+" "+funktion, color="b", size="10pt")
            elif null_switch == 0:
                self.graphWidget.setTitle(mess_art+" "+funktion, color="b", size="10pt")
            self.graphWidget.plot(x[:max_graph-1],y[:max_graph-1], pen=pen)
#            self.graphWidget.plot(list(xdict.keys())[:max_graph-1],y[:max_graph-1], pen=pen)
            self.graphWidget.show()

        if scan_loop == 1 and int(scan_timer - save_timer) == 0:
            scan_timer = int(round(time.time())) + sa_intervall
            self.SCrun()
        if scan_loop == 1 and save_timer <= scan_timer:
            self.SCloop_Button.setProperty("text","Scanner Loop\nOFF..."+str(int(scan_timer - save_timer)) + " s")
            self.SCrun_Button.setVisible(False)
        if scan_loop == 2 and int(scan_timer - save_timer) == 0:
            scan_timer = int(round(time.time())) + sa_intervall
            self.SCrun_all_in_one()
        if scan_loop == 2 and save_timer <= scan_timer:
            self.SCloop_Button.setProperty("text","Scanner Loop\nOFF..."+str(int(scan_timer - save_timer)) + " s")
            self.SCrun_Button.setVisible(False)
        if shot == 1:
            instr.write("SCDP")
            self.result_str = instr.read_raw()
            self.pixmap.loadFromData(self.result_str)
            self.screenshot.setPixmap(self.pixmap)

        check_loop = 0
        self.timer_single.start(0)

EXIT_CODE_REBOOT = -11231351
def ende():
    global sa_flag
    instr.write("ABORt\n*CLS\n*RST", encoding='utf-8')
#    instr.write("*RST", encoding='utf-8')
    instr.close()
    if sa_flag == 1:
        sa_flag = 0
        workbook.close()

def main():
    exitCode = 0
    while True:
        try: app = QtWidgets.QApplication(sys.argv)
        except RuntimeError: app = QApplication.instance()
        app.aboutToQuit.connect(ende)
        window = Ui()
        exitCode = app.exec_()
        if exitCode != EXIT_CODE_REBOOT: break
    return exitCode

main()

