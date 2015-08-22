#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import sys
import re
import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
from string import split
import locale
print locale.getpreferredencoding() # 'cp1251' - для win rus

text_frag1 = u"""гагара арара мамалыга гагаузы татары Кака нанайцы алидада
Мимино бибигон Титикака тамтам Арарат прапрадед кукушка Вовочка чеченцы
татами гогот хохот кваква кокотка кокошник папаха цаца бугага кукуруза
Лубумбаши уксусу ромбабаы"""
class AddBookWindow(QWidget):
    def __init__(self, parent=None):
        super(AddBookWindow, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowSystemMenuHint)
        self.setWindowModality(Qt.WindowModal)
        self.window = loadUi("addBook.ui")
        self.window.buttonBox.clicked.connect(self.close)
        self.window.show()
        print u"работает"

    def openFile(self, filename):
        print filename
        file = open(filename)
        data = file.read()
        #print data
        data1 = data.decode('utf8')
        #self.text = unicode(data ,'utf-8')
        self.text = re.sub("\n", " ", data1)#убераем все переводы коретки
        self.window.textEdit.setText(self.text)
        #print data

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QWidget.__init__(self)
        self.text_frag = re.sub("\n", " ", text_frag1)#убераем все переводы коретки
        self.old_text = ""#текст котороый мы уже напечатали
        self.key_frag = 0#
        self.key_tupe = 0
        self.words = split(self.text_frag)#массив из слов из текста
        self.word_count = 0# какое слово мы набераем
        self.error_count = 0#количество ошибок
        self.block = False# блокировка счетчика ошибок
        self.i = 0
        self.speed = {}
        self.speed2 = {}

        self.speed[0] = time.time()
        self.window = loadUi("gui_key.ui")
        self.window.main_label.setText(self.text_frag)
        self.window.lineEdit.textChanged.connect(self.line_edit_text_changed)
        #self.connect(self.menubar.openFile, SIGNAL('triggered()'), self.showDialog)
        open_file = QAction(QIcon('open.png'), u'Открыть', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Открыть новый файл')

        self.connect(open_file, SIGNAL('triggered()'), self.showDialog)
        self.window.menu.addAction(open_file)
        self.window.show()

    def line_edit_text_changed(self, text): #обработка нажатий клавиш
        self.i = len(self.old_text+text)
        timer=time.time()
        #print timer
        #self.window.time.display(time.time())

        self.text = unicode(text)
       # print self.text_frag[:len(self.old_text+text)]+"=="+self.old_text+text
        print len(self.old_text+text)
        print len(self.text_frag)
        if self.text_frag[:len(self.old_text+text)] == self.old_text + self.text and len(self.old_text+text) < len(self.text_frag):#подсвечиваем букву
            self.block = False
            self.window.main_label.setText(self.text_frag[:len(self.old_text+text)]+"<font color=red>"+self.text_frag[len(self.old_text+self.text)]+"</font>"+self.text_frag[len(self.old_text+self.text)+1:])
        elif self.block == False:
            self.block = True
            self.error_count = self.error_count+1
            self.window.error_count.display(self.error_count)


        #print text+"=="+self.words[self.word_count] #отладка старвниваем что получили с тем что надо
        if self.text == self.words[self.word_count]+" ":#стираем из стоки и заносим в переменную
            self.clearWord()

        self.averageSpeed(timer)
        if len(self.old_text+self.text) >= len(self.text_frag):
            self.andText()



    def andText(self):
          # говрим об окончании текста
        text_finish = u"<center>текст окончен</center> Среднаяя скорость %s"%self.netto
        self.window.main_label.setText(text_finish)
        self.old_text = self.old_text + self.text
        self.word_count = self.word_count + 1
        self.window.lineEdit.setText("")

    def averageSpeed(self, timer):
        if self.i == 1:
            self.speed[0] = timer
        elif len(self.old_text+self.text) == len(self.text_frag):
            self.speed[1] = timer - self.speed[0]
            print self.speed[1]
            netto1 = len(self.text_frag) / self.speed[1]
            self.netto = netto1 * 60
            self.window.speed.display(self.netto)
            self.window.time.display(self.speed[1])
            print self.netto

    def clearWord(self):

        self.old_text = self.old_text + self.text
        self.word_count = self.word_count + 1
        self.window.lineEdit.setText("")

    def showDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        textBook=AddBookWindow(self)
        textBook.openFile(filename)
        print filename
        #textBook.text(filename)

app = QApplication(sys.argv)
mw = MainWindow()
app.exec_()
__author__ = 'smoksmk'
