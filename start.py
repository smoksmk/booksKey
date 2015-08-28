#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import sys
import re
import time
import os
import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import *
from string import split, strip
import locale
print locale.getpreferredencoding() # 'cp1251' - для win rus
reload(sys)
sys.setdefaultencoding('utf8')

class Users(QWidget):
    def __init__(self):
        self.defaultUser = "guest"
        self.info = {}
        self.getText = ""

    def getUserData(self, user="smok"):
        file = open("users/"+user)
        self.getText = file.read()
        self.info = json.loads(self.getText)
        return self.info

    def writeUserData(self, user, data):
        self.info = json.dumps(data)
        open("users/"+user, "w").write(self.info)



class Categories(QWidget):
    def __init__(self):
        self.categories={}
        self.categories = os.listdir("book")
        print self.categories
        for i in range(len(self.categories)):
            book = QAction(self.categories[i], self)
            book.setStatusTip(u'Открыть новый файл')
            self.connect(book, SIGNAL('triggered()'), self.printCotigory(i))
            self.window.menu_3.addAction(book)

    def printCotigory(self, g=0):
        print g

class ParseBook(QWidget):
    def __init__(self):
        self.book = ""
        global countPassegs

    def parseFrag(self, filename=u"text2.txt", frag=0):
        print filename
        # filename = unicode(filename1)
        global countPassegs

        file = open("book/"+filename)
        data1 = file.read()
        file.close()
        re2 = re.compile(u"<passeges>"+"(.*?)"+"<komment>", re.IGNORECASE)
        countPassegs = re2.findall(data1)
        if int(countPassegs[0]) == 0: frag = 0
        re1 = re.compile(u"<passege"+str(frag)+">"+"(.*?)"+"<passege"+str(int(frag)+1)+">", re.IGNORECASE)
        result = re1.findall(data1)
        result1 = result[0]
        # result1 = self.listmerge3(result)
        result1 = result1.decode('utf8')
        return result1


class AddBookWindow(QWidget):
    def __init__(self, parent=None):
        self.defaultSumbol = 300
        self.passageStart = 0
        super(AddBookWindow, self).__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.WindowSystemMenuHint)
        self.setWindowModality(Qt.WindowModal)
        self.window = loadUi("addBook.ui")
        self.window.lineEdit.setText(str(self.defaultSumbol))
        buttonBoxes = self.window.buttonBox
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
        data1 = re.sub(r'\s+', " ", data1)
        self.text = data1
        sumbol = len(data)

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
        self.fileName1 = self.window.fileName.text()
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
        writeText = u"<filename>"+self.fileName1+"<passeges>"+str(i)+"<komment>"+komment+textPassage+"<passege"+str(i+1)+">"
        self.saveBook(writeText)


    def saveBook(self,text):
        # text = text.encode('utf8')

        open('book/'+self.fileName1,'w').write(text)
        self.window.close()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        QWidget.__init__(self)

        self.userInfo = Users().getUserData()
        # print self.userInfo
        self.text_frag = re.sub("\n", " ", ParseBook().parseFrag(self.userInfo["defaultBook"], self.userInfo[self.userInfo["defaultBook"]]))#убераем все переводы коретки
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
        new_book = QAction(QIcon('new.png'), u"Создать", self)
        new_book.setShortcut("Ctrl+N")
        new_book.setStatusTip("Создать новый словарь")

        test = QAction(QIcon('new.png'), u"Тест", self)
        test.setShortcut("Ctrl+T")
        test.setStatusTip("Тестируем функции")

        open_file = QAction(QIcon('open.png'), u'Открыть', self)
        open_file.setShortcut('Ctrl+O')
        open_file.setStatusTip('Открыть новый файл')

        next1 = self.window.next
        next1.setShortcut('Ctrl+Right')
        receiver1 = lambda taskType=self.userInfo[self.userInfo["defaultBook"]]: self.getFrag(self.userInfo["defaultBook"],taskType+1)
        self.connect(next1, SIGNAL('clicked()'), receiver1)

        self.connect(test, SIGNAL('triggered()'), Users().getUserData)
        self.connect(new_book, SIGNAL('triggered()'), self.newBook)
        self.connect(open_file, SIGNAL('triggered()'), self.showDialog)

        self.categories={}
        self.categories = os.listdir("book")
        print self.categories
        for i in range(len(self.categories)):# получаем список книг
            book = QAction(QIcon('new.png'), str(self.categories[i]), self, checkable=True)
            book.setStatusTip('Открыть новый файл'+str(i))
            # book.triggered.connect(self.getFrag("5"))
            receiver = lambda taskType=self.categories[i]: self.getFrag(taskType, self.userInfo[taskType])
            self.connect(book, SIGNAL('triggered()'), receiver)
            self.window.menu_3.addAction(book)


        self.window.menu.addAction(new_book)
        self.window.menu.addAction(open_file)
        self.window.menu.addAction(test)

        self.window.show()



    def getFrag(self, book, frag): # Получаем отрывок
        print "OK"
        print book
        print frag
        global countPassegs
        print countPassegs
        self.window.lineEdit.setEnabled(True)
        self.window.lineEdit.setFocus()
        if int(countPassegs[0]) == 0: frag = 0
        self.userInfo["defaultBook"] = book
        print self.userInfo.has_key(book)
        if self.userInfo.has_key(book) == False:
            print "Небыло такого значения"
            h3 = {book:0}
            self.userInfo.update(h3)
            print self.userInfo
        print frag
        frag = ParseBook().parseFrag(book, frag)
        # Сбрасываем на начало
        self.old_text = ""
        self.word_count = 0

        self.text_frag = frag
        self.words = split(frag)
        self.window.main_label.setText(frag)

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


        print text+"=="+self.words[self.word_count] #отладка старвниваем что получили с тем что надо
        if self.text == self.words[self.word_count]+" ":#стираем из стоки и заносим в переменную
            self.clearWord()

        self.averageSpeed(timer)
        if len(self.old_text+self.text) >= len(self.text_frag):# Говорим о окончании фрагмента
            self.andText()



    def andText(self):
          # говрим об окончании текста
        netto = str(self.netto)
        text_finish = u"<center>текст окончен</center> Среднаяя скорость %s"%netto[:5]
        self.window.main_label.setText(text_finish)
        self.old_text = self.old_text + self.text
        self.word_count = self.word_count + 1
        self.window.lineEdit.setText("")
        self.window.lineEdit.setEnabled(False)
        self.window.next.setFocus()
        print self.userInfo["defaultBook"]
        self.userInfo[self.userInfo["defaultBook"]]+=1
        Users().writeUserData(self.userInfo["name"], self.userInfo)

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

    def newBook(self):
        AddBookWindow(self)


    def showDialog(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '/home/smok')
        if filename != "":
            textBook=AddBookWindow(self)
            filename1 = unicode(filename)
            textBook.openFile(filename1)
        #print filename
        #textBook.text(filename)

app = QApplication(sys.argv)
mw = MainWindow()
app.exec_()
__author__ = 'smoksmk'
