SecretId = "AKIDGRSHz3e17HVaVEeEWddR4Wr1zmNld5yk"
SecretKey = "rY5VmsobGoBM2YsFWcXG0c3HMI2f6OVU"

'''
Timestamp	Integer	是	当前 UNIX 时间戳，可记录发起 API 请求的时间。例如1529223702，如果与当前时间相差过大，会引起签名过期错误。
Nonce	Integer	是	随机正整数，与 Timestamp 联合起来，用于防止重放攻击。
SecretId	String	是	在云API密钥上申请的标识身份的 SecretId，一个 SecretId 对应唯一的 SecretKey ，而 SecretKey 会用来生成请求签名 Signature。
Action	是	String	公共参数，本接口取值：DescribeRegions
Version	是	String	公共参数，本接口取值：2017-03-12
'''
import time
uri = "cvm.tencentcloudapi.com"
paramDict = {
    "Action":"DescribeRegions",
    "Version":"2017-03-12",
    "SecretId":SecretId,
    "Nonce":123456,
    "Timestamp":int(time.time()),
}

tempList = []
tempDict = {}
for eveKey, eveValue in paramDict.items():
    tempLowerData = eveKey.lower()
    tempList.append(tempLowerData)
    tempDict[tempLowerData] = eveKey
tempList.sort()

resultList = []
for eveData in tempList:
    tempStr = str(tempDict[eveData]) + "=" + str(paramDict[tempDict[eveData]])
    resultList.append(tempStr)

sourceStr = "&".join(resultList)

requestStr = "%s%s%s%s%s"%("GET", uri, "/", "?", sourceStr)

import sys
if sys.version_info[0] > 2:
    signStr = requestStr.encode("utf-8")
    SecretKey = SecretKey.encode("utf-8")

import hashlib
digestmod = hashlib.sha1

import hmac
hashed = hmac.new(SecretKey, signStr, digestmod)

import binascii
base64Data = binascii.b2a_base64(hashed.digest())[:-1]

if sys.version_info[0] > 2:
    base64Data = base64Data.decode()

import urllib.parse
base64Data = urllib.parse.quote(base64Data)

url = "https://" + uri + "/" + "?" + sourceStr + "&Signature=" + base64Data
print(url)

import urllib.request
import json
for eveData in json.loads(urllib.request.urlopen(url).read().decode("utf-8"))["Response"]["RegionSet"]:
    print(eveData)