import pytest

from common.common_requests import CommonRequests
from common.common_yaml import CommonYaml


class TestWeixin:

    request = CommonRequests()
    yaml = CommonYaml()

    @pytest.mark.parametrize('caseinfo', yaml.read_yaml_testcase('/testcase/test_weixin/get_token.yaml'))
    def test_01_get_token(self, caseinfo):
        name = caseinfo['name']
        print(name)
        method = caseinfo['request']['method']
        url = caseinfo['request']['url']
        data = caseinfo['request']['data']
        validate = caseinfo['validate']

        res = self.request.send_request(url=url, data=data, method=method)
        self.yaml.write_yaml_token({'access_token': res.json()['access_token']})
        print(res.json())

    @pytest.mark.parametrize('caseinfo', yaml.read_yaml_testcase('/testcase/test_weixin/edit_flag.yaml'))
    def test_02_edit_flag(self, caseinfo):
        name = caseinfo['name']
        print(name)
        method = caseinfo['request']['method']
        url = caseinfo['request']['url']+self.yaml.read_yaml_token('access_token')
        data = caseinfo['request']['data']
        validate = caseinfo['validate']
        res = self.request.send_request(url=url, data=data, method=method)
        print(res.json())


