# -*- coding: utf-8 -*-

SecretId = "AKIDGRSHz3e17HVaVEeEWddR4Wr1zmNld5yk"
SecretKey = "rY5VmsobGoBM2YsFWcXG0c3HMI2f6OVU"

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.cvm.v20170312 import cvm_client, models

try:
    # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey
    cred = credential.Credential(SecretId, SecretKey)

    # 实例化要请求产品(以cvm为例)的client对象，clientProfile是可选的。
    client = cvm_client.CvmClient(cred, "ap-guangzhou")

    # 实例化一个cvm实例信息查询请求对象,每个接口都会对应一个request对象。
    req = models.DescribeInstancesRequest()


    '''
    Array of Filter
        Name	String	是	需要过滤的字段。
        Values	Array of String	是	字段的过滤值。
    '''
    # # 填充请求参数,这里request对象的成员变量即对应接口的入参。
    # # 你可以通过官网接口文档或跳转到request对象的定义处查看请求参数的定义。
    # respFilter = models.Filter()  # 创建Filter对象, 以zone的维度来查询cvm实例。
    # respFilter.Name = "zone"
    # respFilter.Values = ["ap-shanghai-1", "ap-shanghai-2"]
    # req.Filters = [respFilter]  # Filters 是成员为Filter对象的列表

    # 这里还支持以标准json格式的string来赋值请求参数的方式。下面的代码跟上面的参数赋值是等效的。
    params = '''{
        "Filters": [
            {
                "Name": "zone",
                "Values": ["ap-guangzhou-1", "ap-guangzhou-2", "ap-guangzhou-3"]
            }
        ]
    }'''
    req.from_json_string(params)

    # 通过client对象调用DescribeInstances方法发起请求。注意请求方法名与请求对象是对应的。
    # 返回的resp是一个DescribeInstancesResponse类的实例，与请求对象对应。
    resp = client.DescribeInstances(req)

    # 输出json格式的字符串回包
    print(resp.to_json_string())

    # 也可以取出单个值。
    # 你可以通过官网接口文档或跳转到response对象的定义处查看返回字段的定义。
    print(resp.TotalCount)

except TencentCloudSDKException as err:
    print(err)