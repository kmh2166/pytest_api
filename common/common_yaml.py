import yaml
from common.tools import get_project_path, sep


class CommonYaml:

    # token保存文件地址
    token_yaml_path = '/config/token.yaml'

    # 使用构造函数，初始化yaml文件，把yaml文件读取出来
    def __init__(self):
        # 用tools里的get_project_path()获取项目路径
        self.project_path = get_project_path()
        # 使用with——open方法读取yaml文件内容
        # open里的project_path + sep(["config", "environment.yaml"）用于把yaml文件路径拼出来
        with open(self.project_path + sep(["config", "environment.yaml"], add_sep_before=True), "r",
                  encoding="utf-8") as env_file:
            # 使用yaml.load方法把读取出的文件转化为列表或字典，方便后续取值
            # Loader=yaml.FullLoader意思为加载完整的YAML语言，避免任意代码执行
            self.env = yaml.load(env_file, Loader=yaml.FullLoader)

    def get_username_password(self, user):
        """
        读取配置文件里的账号密码
        :param user: 需要取哪一个账号的就输入对应的名称，比如我想去york的账密，user就传“york”
        :return:
        """
        # 直接return出来对应的账号密码
        return self.env["user"][f"{user}"]["username"], self.env["user"][f"{user}"]["password"]

    def get_url(self):
        """
        测试地址
        :return:
        """
        # 直接return出来对应的测试域名
        return self.env["test_url"]

    def get_mysql_config(self):
        """
        获取数据库配置
        :return:
        """
        # 直接return出来对应yaml里的数据库参数，输出字典
        return self.env["mysql"]

    # yaml文件读取
    def read_yaml_testcase(self, yaml_path):
        with open(self.project_path + yaml_path, mode='r', encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value

    # yaml文件读取
    def read_yaml_token(self, key):
        with open(self.project_path + self.token_yaml_path, mode='r', encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[key]

    # yaml文件写入
    def write_yaml_token(self, data):
        with open(self.project_path + self.token_yaml_path, mode='a', encoding='utf-8') as f:
            yaml.dump(data, stream=f, allow_unicode=True)

    # yaml文件清空
    def clear_yaml_token(self):
        with open(self.project_path + self.token_yaml_path, mode='w', encoding='utf-8') as f:
            f.truncate()


# 测试一下
if __name__ == "__main__":
    getConfig = CommonYaml()
    print(getConfig.get_username_password("york"))
    print(getConfig.get_url())
    print(getConfig.get_mysql_config())

