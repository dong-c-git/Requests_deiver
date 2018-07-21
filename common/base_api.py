# coding:utf-8

import json,os,requests
# import sys
# sys.path.append('C:/Users/Administrator/Desktop/Reqwebdriver')

from common.readexcel import ExcelUtil
from common.writeexcel import copy_excel,Write_excel

def send_requests(s,testdata):
    """封装requests请求"""
    method = testdata["method"]
    url = testdata["url"]
    #url后边params参数
    try:
        params = eval(testdata["params"])
    except:
        params = None
    #请求头部的heraders
    try:
        headers = eval(testdata["headers"])
        print("请求头部：%s"%headers)
    except:
        headers = None
    #post请求body类型：
    type = testdata["type"]

    test_nub = testdata["id"]
    print("*******正在执行用例：-----  %s  ----**********"%test_nub)
    print("请求方式：%s, 请求url:%s" % (method, url))
    print("请求params：%s" % params)

    #post请求body内容
    try:
        bodydata = eval(testdata["body"])
    except:
        bodydata = {}

    #判断data数据还是json数据
    if type =="data":
        body = bodydata
    elif type =="json":
        body = json.dumps(bodydata)
    else:
        body = bodydata
    if method =="post":print("post请求body类型为：%s,body内容为：%s"%(type,body))
    verify = False
    res = {}
    try:
        r = s.request(method = method,
                      url = url,
                      headers = headers,
                      data = body,
                      verify = verify)
        print("页面返回信息：%s" % r.content.decode("utf-8"))
        res["id"] = testdata["id"]
        res["rowNum"] =testdata["rowNum"]
        res["statuscode"] = str(r.status_code) #状态码转成str
        res["text"] = r.content.decode("utf-8")
        res["times"] = str(r.elapsed.total_seconds())    #接口请求时间转成str
        if res["statuscode"] != "200":
            res["error"] = res["text"]
        else:
            res["error"] = ""
        if testdata["checkpoint"] in res["text"]:
            res["result"] = "pass"
            print ("用例测试结果：%s------>%s"%(test_nub,res["result"]))
        else:
            res["result"] = "fail"
        res["msg"]=""
        return res
    except  Exception as msg:
        res["msg"] = str(msg)
        return res



def write_result(result,filename="result.xlsx"):
    """返回结果行数：row_nub"""
    print (result)
    row_nub = result["rowNum"]
    # #写入statuscode
    wt = Write_excel(filename)
    wt.write(row_nub,8,result["statuscode"])    #第八列写入返回状态码
    wt.write(row_nub,9,result["times"])         #耗时
    wt.write(row_nub,10,result["error"])        #状态码非200时候返回结果
    wt.write(row_nub,11,result["result"])       #返回结果是fail还是pass
    wt.write(row_nub,12,result["msg"])          #抛异常

if __name__=="__main__":
    data = ExcelUtil("debug_api.xlsx","Sheet1").dict_data()
    print (data[0])
    s = requests.session()
    res = send_requests(s,data[0])
    copy_excel("debug_api.xlsx","debug_api2.xlsx")
    write_result(res,filename="debug_api2.xlsx")







