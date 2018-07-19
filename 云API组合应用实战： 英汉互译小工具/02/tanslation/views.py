from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


SecretId = "AKIDNbigT4ylqjQxMdDcN7jAPSKVehy9F5mI"
SecretKey = "VpYt6A2ykNp6Gl6HJCtPkt43b3NWTHvP"

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException

from tencentcloud.tmt.v20180321 import tmt_client, models
import json

def tanslationFun(inputData):
    try:

        while True:

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
            }"""%(inputData)

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
                print("请输入英文或者中文，本软件暂不支持其他语言的翻译！")

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
                }"""%(inputData, fromLang, toLang)

                req.from_json_string(params)

                resp = client.TextTranslate(req)

                return json.loads(resp.to_json_string())["TargetText"]

    except TencentCloudSDKException as e:
        return None
@csrf_exempt
def indexPage(request):

    getContent = request.POST.get("content","")



    if getContent:
        contentList = getContent.split("\r\n")
        tempList = []
        for eveContent in contentList:
            returnContent = tanslationFun(eveContent)
            tempList.append(returnContent)

        returnContent = "\n".join(tempList)

    return render(request, "index.html", locals())
