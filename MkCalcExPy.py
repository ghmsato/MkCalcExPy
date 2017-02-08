#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import random

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

import MainWindowUi

#
# DIV mode
#

# return 1 or 0 based on threshold value
# i: current position
# v: threshold value
def f(i, v):
    if i < v:
        return 1
    else:
        return 0

# make random array of flags
# l: length of array
# v: number of 1 values in the array
# https://ja.wikipedia.org/wiki/%E3%83%95%E3%82%A3%E3%83%83%E3%82%B7%E3%83%A3%E3%83%BC_-_%E3%82%A4%E3%82%A7%E3%83%BC%E3%83%84%E3%81%AE%E3%82%B7%E3%83%A3%E3%83%83%E3%83%95%E3%83%AB
def randsort_f(l, v):
    a = [0] * l
    for i in range(l):
        j = random.randint(0, i)
        if j != i:
            a[i] = a[j]
        a[j] = f(i, v)
    return a

# make one item from parameters
# a: number of digits for dividend
# b: number of digits for divider
# f: flag 0 -- no remainder, 1 -- with remainder
def mkdivitem(a, b, f):
    x = random.randint(10 ** (a - 1), 10 ** a - 1)
    if b == 1 and f == 1:
        y = random.randint(2, 9)
    else:
        y = random.randint(10 ** (b - 1), 10 ** b - 1)
    if f == 0:
        r = int(x / y)
        if y * r < 10 ** (a - 1):
            r = r + 1
        x = y * r
        s = 0
    else:
        r = int(x / y)
        s = x - y * r
        if s == 0:
            high = min(y - 1, 10 ** a - 1 - x)
            if high < 3:
                s = 1
            else:
                s = random.randint(1, high)
            x = y * r + s
    return [x, y, r, s]

# make string for display
# i: number
# a: number of digits for dividend
# b: number of digits for divider
# f: flag 0 -- no remainder, 1 -- with remainder
def mkdivitemstr(i, a, b, f):
    r = mkdivitem(a, b, f)
    s = '(' + str(i) + ')\t'
    s = s + str(r[0]) + ' ÷ ' + str(r[1])
    s = s + '\t=  ' + str(r[2])
    if f == 1 and r[3] != 0:
        s = s + '\t... ' + str(r[3])
    return s

#
# MUL mode
#
def mkmulitem(a, b):
    x = random.randint(10 ** (a - 1), 10 ** a - 1)
    if int(x / 10) * 10 == x:
        x = x + random.randint(1, 9)
    y = random.randint(10 ** (b - 1), 10 ** b - 1)
    if int(y / 10) * 10 == y:
        y = y + random.randint(1, 9)
    return [x, y, x * y]

def mkmulitemstr(i, a, b, c, d):
    r = mkmulitem(a + c, b + d)
    sx = str(r[0])
    if c != 0:
        pos = len(sx) - c
        sx = sx[:pos] + '.' + sx[pos:]
    sy = str(r[1])
    if d != 0:
        pos = len(sy) - d
        sy = sy[:pos] + '.' + sy[pos:]
    sr = str(r[2])
    if (c + d) != 0:
        pos = len(sr) - (c + d)
        sr = sr[:pos] + '.' + sr[pos:]
    s = '(' + str(i) + ')\t' + sx + ' × ' + sy
    s = s + '\t=  ' + sr
    return s


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = MainWindowUi.Ui_MainWindow()
        self.ui.setupUi(self)
        # DIV mode
        self.ui.groupBox_3.setVisible(False)
        self.ui.div_res_no.clicked.connect(self.changeCheckedDiv)
        self.ui.div_res_yes.clicked.connect(self.changeCheckedDiv)
        self.ui.div_res_mix.clicked.connect(self.changeCheckedDiv)
        self.ui.horizontalSlider.valueChanged[int].connect(self.changeValueSlider)
        self.ui.div_num_v.valueChanged[int].connect(self.changeValueV)
        self.ui.div_num_l.valueChanged[int].connect(self.changeValueL)
        self.ui.div_generate.clicked.connect(self.divsubmit)
        # MUL mode
        self.ui.groupBox_5.setVisible(False)
        self.ui.mul_no.clicked.connect(self.changeCheckedMul)
        self.ui.mul_yes.clicked.connect(self.changeCheckedMul)
        self.ui.mul_generate.clicked.connect(self.mulsubmit)
        # show
        self.setWindowTitle('算数問題作成')
        self.show()

    #
    # Callbacks (DIV mode)
    #
    # callback function for checking any of radio button
    def changeCheckedDiv(self):
        if self.ui.div_res_mix.isChecked():
            self.ui.groupBox_3.setVisible(True)
        else:
            self.ui.groupBox_3.setVisible(False)

    # callback function for changing slider
    def changeValueSlider(self, value):
        if self.ui.div_res_mix.isChecked():
            self.ui.div_num_v.setValue(value)

    # callback function for changing value of rate
    def changeValueV(self, value):
        if self.ui.div_res_mix.isChecked():
            self.ui.horizontalSlider.setValue(value)

    # callback function for changing value of result items
    def changeValueL(self, value):
        self.ui.horizontalSlider.setRange(1, value)
        self.ui.div_num_v.setRange(1, value)

    # callback function for clicking "Generate" button
    def divsubmit(self):
        a = self.ui.div_num_a.value()
        b = self.ui.div_num_b.value()
        l = self.ui.div_num_l.value()
        v = self.ui.div_num_v.value()
        if self.ui.div_res_no.isChecked():
            f = 0
        elif self.ui.div_res_yes.isChecked():
            f = 1
        else:
            f = 2
        if a < b:
            msg = QMessageBox.critical(self, 'エラー', '割る数が大きすぎます')
            return
        else:
            result_window = ResultWindowDiv(a, b, l, f, v)
            winlist.append(result_window)

    #
    # Callbacks (MUL mode)
    #
    # callback function for checking radio button
    def changeCheckedMul(self):
        if self.ui.mul_yes.isChecked():
            self.ui.groupBox_5.setVisible(True)
        else:
            self.ui.groupBox_5.setVisible(False)

    # callback function for clicking "Generate" button
    def mulsubmit(self):
        a = self.ui.mul_num_a.value()
        b = self.ui.mul_num_b.value()
        l = self.ui.mul_num_l.value()
        if self.ui.mul_yes.isChecked():
            c = self.ui.mul_num_c.value()
            d = self.ui.mul_num_d.value()
        else:
            c = 0
            d = 0
        if (a + c) > 9 or (b + d) > 9:
            msg = QMessageBox.critical(self, 'エラー', '桁が大きすぎます')
            return
        else:
            result_window = ResultWindowMul(a, b, c, d, l)
            winlist.append(result_window)


class ResultWindowDiv(QTextEdit):
    def __init__(self, a, b, l, f, v):
        super(ResultWindowDiv, self).__init__()
        if (a + b) == 2:
            self.resize(400, 600)
            bt = '\t'
        elif (a + b) < 9:
            self.resize(500, 600)
            bt = '\t\t'
        elif (a + b) < 14:
            self.resize(600, 600)
            bt = '\t\t\t'
        else:
            self.resize(600, 600)
            bt = '\t\t\t\t'
        if f != 0:
            self.resize(self.width() + 100, 600)
        font = QFont()
        font.setFamily("Meiryo UI")
        font.setPointSize(12)
        self.setFont(font)
        if f == 2:
            far = randsort_f(l, v)
        else:
            far = [f] * l
        self.append('番号\t問題' + bt + '答')
        for i in range(l):
            self.append(mkdivitemstr(i, a, b, far[i]))
        self.setWindowTitle('作成された問題')
        self.show()

class ResultWindowMul(QTextEdit):
    def __init__(self, a, b, c, d, l):
        super(ResultWindowMul, self).__init__()
        if (a + b + c + d) == 2:
            self.resize(400, 600)
            bt = '\t'
        elif (a + b + c + d) < 9:
            self.resize(500, 600)
            bt = '\t\t'
        elif (a + b + c + d) < 14:
            self.resize(600, 600)
            bt = '\t\t\t'
        elif (a + b + c + d) == 18 and (c + d) != 0:
            self.resize(900, 600)
            bt = '\t\t\t\t\t'
        else:
            self.resize(800, 600)
            bt = '\t\t\t\t'
        font = QFont()
        font.setFamily("Meiryo UI")
        font.setPointSize(12)
        self.setFont(font)
        self.append('番号\t問題' + bt + '答')
        for i in range(l):
            self.append(mkmulitemstr(i, a, b, c, d))
        self.setWindowTitle('作成された問題')
        self.show()

if __name__ == '__main__':
    winlist = [] # necessary to keep result window visible
    app = QApplication(sys.argv)
    main_window = MainWindow()
    winlist.append(main_window)
    sys.exit(app.exec_())
