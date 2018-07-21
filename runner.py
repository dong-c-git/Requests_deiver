#coding:utf-8

import unittest
import time
from common import HTMLTestRunner_jpg
import os

curpath = os.path.dirname(os.path.realpath(__file__))
report_path = os.path.join(curpath,"report")
if not os.path.exists(report_path):os.mkdir(report_path)
case_path = os.path.join(curpath,"case")

def add_case(casepath=case_path,rule="test*.py"):
    """加载所有的测试用例"""
    #定义discover参数
    discover = unittest.defaultTestLoader.discover(casepath,pattern=rule)
    return discover

def run_case(all_case,reportpath=report_path):
    """执行所有测试用例，并把所有测试用例写进测试报告"""
    htmlreport = reportpath+r"\result.html"
    print("测试报告生成地址：%s" %reportpath)
    fp = open(htmlreport,"wb")
    runner = HTMLTestRunner_jpg.HTMLTestRunner(stream=fp,
                                               verbosity=2,
                                               title="测试报告",
                                               description="用例执行情况")

    #调用 add_case函数返回值
    runner.run(all_case)
    fp.close()
if __name__=="__main__":
    cases = add_case()
    run_case(cases)




