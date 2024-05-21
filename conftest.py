import pytest

from common.common_yaml import CommonYaml


@pytest.fixture(scope='function')
def set():
    print('开始')
    yield
    print('结束')


# 每次执行会话前（用例执行前）清空extract.yaml文件
# 前置
@pytest.fixture(scope='session',autouse=True)
def clear_yaml():
    CommonYaml().clear_yaml_token()
