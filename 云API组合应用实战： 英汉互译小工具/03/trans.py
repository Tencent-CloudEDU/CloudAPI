# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'trans.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
import json
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1208, 849)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(40, 60, 821, 301))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(40, 460, 1111, 341))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(900, 70, 251, 281))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 161, 18))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 410, 161, 18))
        self.label_2.setObjectName("label_2")
        # MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.trans)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "点击翻译"))
        self.label.setText(_translate("MainWindow", "输入英语或中文"))
        self.label_2.setText(_translate("MainWindow", "翻译结果"))


class mywindow(QtWidgets.QWidget, Ui_MainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.setupUi(self)

    def trans(self):
        content = self.textEdit.toPlainText()

        if content:
            contentList = content.split("\n")
            resultData = []
            for inputData in contentList:
                SecretId = "AKIDNbigT4ylqjQxMdDcN7jAPSKVehy9F5mI"
                SecretKey = "VpYt6A2ykNp6Gl6HJCtPkt43b3NWTHvP"
                cred = credential.Credential(SecretId, SecretKey)

                client = tmt_client.TmtClient(cred, "ap-guangzhou")

                # 进行语种识别
                req = models.LanguageDetectRequest()
                '''
                    Text	是	String	待识别的文本
                    ProjectId	是	Integer	项目id
                '''
                params = """{
                            "Text": "%s",
                            "ProjectId": 1
                        }""" % (inputData)

                req.from_json_string(params)

                resp = client.LanguageDetect(req)

                # 进行英汉互译
                fromLang = json.loads(resp.to_json_string())["Lang"]
                toLang = None
                if fromLang == "en":
                    toLang = "zh"
                elif fromLang == "zh":
                    toLang = "en"
                else:
                    self.textEdit_2.setText("请输入英文或者中文，本软件暂不支持其他语言的翻译！")
                    break

                if toLang:
                    req = models.TextTranslateRequest()

                    '''
                        SourceText	是	String	待翻译的文本
                        Source	是	String	源语言，参照Target支持语言列表
                        Target	是	String
                        ProjectId	是	Integer	项目id
                    '''
                    params = """{
                                "SourceText": "%s",
                                "Source": "%s",
                                "Target": "%s",
                                "ProjectId": 1
                            }""" % (inputData, fromLang, toLang)

                    req.from_json_string(params)

                    resp = client.TextTranslate(req)

                    resultData.append(json.loads(resp.to_json_string())["TargetText"])
            self.textEdit_2.setText("\n".join(resultData))

import sys
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
