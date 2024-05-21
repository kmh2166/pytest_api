import json
import requests
# 导入adapters，处理接口重试
from requests.adapters import HTTPAdapter

from common.common_yaml import CommonYaml
from common.deal_with_response import deal_with_res


class CommonRequests:
    # 构造函数，初始化session，封装requests
    def __init__(self, headers=None, timeout=None):
        self.session = requests.Session()
        # 在session实例上挂载adapter实例，目的就是请求异常时，自动重试
        self.session.mount("http://", HTTPAdapter(max_retries=3))
        self.session.mount("https://", HTTPAdapter(max_retries=3))

        # 公共请求头设置，把对应的值设置好
        self.session.headers = headers
        self.timeout = timeout
        # 调用获取yaml里的url，把测试域名拿出来，下面做拼接接口用
        self.url = CommonYaml().get_url()

    # 定义公共方法
    def send_request(self, url, data=None, method="get", **kwargs):
        method = str(method).lower()
        if method == "get":
            res = self.session.get(self.url + url, params=data, **kwargs)
        elif method == "post":
            if data:
                data = json.dumps(data)
            res = self.session.post(self.url + url, data=data, **kwargs)
        deal_with_res(data, res)
        return res

    def get_request(self, url, params=None, **kwargs):
        res = self.session.get(self.url + url, params=params, timeout=self.timeout, **kwargs)
        deal_with_res(params, res)
        return res

    def post_request(self, url, data=None, json=None, **kwargs):
        # 如果传入的是表单，那接口就传data，适用一些接口是form-data格式的
        if data:
            res = self.session.post(self.url + url, data=data, timeout=self.timeout, **kwargs)
            # 调用处理报文的方法，把接口信息加入到测试报告
            deal_with_res(data, res)
            return res
        # 如果传入的json，就传入json，适用大部分接口
        if json:
            res = self.session.post(self.url + url, json=json, timeout=self.timeout, **kwargs)
            # 调用处理报文的方法，把接口信息加入到测试报告
            deal_with_res(json, res)
            return res
        # 有些post接口是什么也不传的，兼容这种情况
        res = self.session.post(self.url + url, timeout=self.timeout, **kwargs)
        # 调用处理报文的方法，把接口信息加入到测试报告
        deal_with_res(json, res)
        return res

    # 魔法函数
    def __del__(self):
        """
        当实例被销毁时，释放掉session所持有的连接
        :return:
        """
        if self.session:
            self.session.close()


if __name__ == '__main__':
    get_res = CommonRequests().send_request("/cgi-bin/token",CommonYaml().read_yaml_testcase('/testcase/test_weixin/get_token.yaml')[0]['request']['data'])
    print(get_res.text, "\n")
