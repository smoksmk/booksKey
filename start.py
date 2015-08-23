#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import sys
import re
import time
import os.path
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
from string import split
import locale
print locale.getpreferredencoding() # 'cp1251' - для win rus
reload(sys)
sys.setdefaultencoding('utf8')

text_frag1 = u"""гагара арара мамалыга гагаузы татары Кака нанайцы алидада
Мимино бибигон Титикака тамтам Арарат прапрадед кукушка Вовочка чеченцы
татами гогот хохот кваква кокотка кокошник папаха цаца бугага кукуруза
Лубумбаши уксусу ромбабаы"""
class AddBookWindow(QWidget):
    def __init__(self, parent=None):
        self.defaultSumbol = 500
        self.passageStart = 0
        super(AddBookWindow, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowSystemMenuHint)
        self.setWindowModality(Qt.WindowModal)
        self.window = loadUi("addBook.ui")
        buttonBoxes  = self.window.buttonBox
        self.window.connect(buttonBoxes, SIGNAL('accepted ()'), self.editBook)
        self.window.connect(buttonBoxes, SIGNAL('rejected ()'), self.closeWindow)
        self.window.show()

    def closeWindow(self):
        print "OK"
        self.window.close()

    def openFile(self, filename):

        file = open(filename)
        data = file.read()
        file = unicode(filename)
        (dirName, self.fileName1) = os.path.split(file)#извеняйте у меня кризис на названия переменных
        data1 = data.decode('utf8')
        data1 = re.sub("^\s+|\n|\r|\s+$", ' ', data1)
        data1 = re.sub("^\s+|  |\s+$", " ", data1)
        self.text = data1
        sumbol = len(data)
        self.window.lineEdit.setText(str(self.defaultSumbol))
        self.window.fileName.setText(self.fileName1)
        self.window.simbol.setText(str(sumbol))
        self.window.textEdit.setText(self.text)
        passageInt = sumbol//self.defaultSumbol
        self.window.passage.setText(str(passageInt))

    def editBook(self):
        print "OK"
        text = self.window.textEdit.toPlainText()
        lenSumbol = self.window.lineEdit.text()
        komment = self.window.koment.text()
        text = unicode(text)
        passageInt = len(text)//int(lenSumbol)
        i = 0
        y = 0
        textPassage = ""
        passageInt2 = 0
        if passageInt == 0: passageInt = 1
        if len(text)>=lenSumbol: #В случае того если у нас текст меньше чем задано
                passageInt2 = len(text)
                print "сиволов мало"
        else:
            for i in range(passageInt):

                print str(self.passageStart) +"<="+ str(len(text))
                if self.passageStart <= len(text)-int(lenSumbol)-int(lenSumbol):
                    for y in range(0, int(lenSumbol)):
                        #if text[self.passageStart+int(lenSumbol)+y] >= len(text)-1000: break
                        if text[self.passageStart+int(lenSumbol)+y]==".":
                            passageInt2 = self.passageStart+int(lenSumbol)+y+1
                            break
                        elif y == int(lenSumbol)-1:
                            passageInt2 = self.passageStart+int(lenSumbol)+y+1
                else:
                    passageInt2=len(text)
                    break
                if passageInt2 == self.passageStart: passageInt2=len(text)
                print self.passageStart
                print passageInt2
                textPassage = textPassage + "<passege"+str(i)+">"+text[self.passageStart:passageInt2]

                self.passageStart = int(passageInt2+1)


        textPassage = textPassage + "<passege"+str(i)+">"+text[self.passageStart:]
        self.window.textEdit.setText(textPassage)
        writeText = u"<filename>"+self.fileName1+"<passeges>"+str(i)+"<komment>"+komment+textPassage
        self.saveBook(writeText)


    def saveBook(self,text):
        # text = text.encode('utf8')
        open('book/'+self.fileName1,'w').write(text)
        self.window.close()

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
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home/smok')
        textBook=AddBookWindow(self)
        filename1 = unicode(filename)
        textBook.openFile(filename1)
        #print filename
        #textBook.text(filename)

app = QApplication(sys.argv)
mw = MainWindow()
app.exec_()
__author__ = 'smoksmk'
