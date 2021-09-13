from typing import List
import string
import random
from .module.command import command
from .module.port import port
from .module.ip import ip
import pathlib
from dataclasses import dataclass
import hashlib
import json


class docker(command, ip, port):
    def __init__(self):
        command.__init__(self)
        ip.__init__(self)
        port.__init__(self)
        self.service_cache = None
        pass

    def add_service_cache(self, classid, userid, service_name, port):
        """
        classid,useridをキーとしてdocker-compose.ymlのハッシュ値とportを保存
        """
        if self.service_cache is None:
            try:
                with open("service_cache.json") as f:
                    self.service_cache = json.load(f)
            except BaseException:
                self.service_cache = {}
        yml = self.select_service(service_name)
        yml_data = self.load_yml(yml)
        service_hash = hashlib.sha3_512(yml_data.encode("utf-8")).hexdigest()
        self.service_cache[f"{classid}/{userid}"] = {"port": int(port),
                                                     "hash": service_hash}
        with open("service_cache.json", "w") as f:
            json.dump(self.service_cache, f, indent=4, sort_keys=True)

    def get_port_from_service_cache(
            self, classid, userid, service_name) -> int:
        """
        classid,useridをキーとしてdocker-compose.ymlのハッシュ値に変更がなければ、前回の割当portを返す
        """
        if self.service_cache is None:
            try:
                with open("service_cache.json") as f:
                    self.service_cache = json.load(f)
            except BaseException:
                self.service_cache = {}
        if f"{classid}/{userid}" not in self.service_cache:
            return None
        yml = self.select_service(service_name)
        yml_data = self.load_yml(yml)
        service_hash = hashlib.sha3_512(yml_data.encode("utf-8")).hexdigest()
        if self.service_cache[f"{classid}/{userid}"]["hash"] == service_hash:
            return self.service_cache[f"{classid}/{userid}"]["port"]
        else:
            return None

    def GetRandomStr(self, num) -> str:
        # 英数字をすべて取得
        dat = string.digits + string.ascii_lowercase + string.ascii_uppercase

        # 英数字からランダムに取得
        return ''.join([random.choice(dat) for i in range(num)])

    def get_yml_list(self) -> List[pathlib.PosixPath]:
        service_path = pathlib.Path("./service")
        yml_list = []
        yml_list.extend(service_path.glob('**/docker-compose.yml'))
        yml_list.extend(service_path.glob('**/docker-compose.yaml'))
        return yml_list

    def get_yml_list_str(self) -> str:
        yml_list = self.get_yml_list()
        result = []
        for yml in yml_list:
            result.append(str(yml.parent.name))
        return result

    def select_service(self, service_name) -> pathlib.PosixPath:
        yml_list = self.get_yml_list()
        for yml in yml_list:
            if yml.parent.name == service_name:
                return yml
        return False

    def load_yml(self, path: str) -> str:
        try:
            with open(path) as f:
                result = f.read()
            return result
        except BaseException:
            return False

    def write_yml(self, path: str, data: str) -> bool:
        try:
            with open(path, "w") as f:
                f.write(data)
            return True
        except BaseException:
            return False

    def make_yml(
            self,
            yml_path: pathlib.PosixPath,
            port,
            userid,
            class_id) -> pathlib.PosixPath:
        yml = self.load_yml(yml_path)
        yml = yml.replace("{automatic_allocation_port}", str(port))
        yml = yml.replace("{userid}", userid)
        yml = yml.replace("{classid}", class_id)
        filename = f"{self.GetRandomStr(10)}.yml"
        new_yml_path = yml_path.parent / filename
        self.write_yml(new_yml_path, yml)
        return new_yml_path

    async def deploy_service(self, yml_path: pathlib.PosixPath, service_name):
        cmd = f"docker stack deploy -c {yml_path.name} {service_name}"
        result = await self.run(cmd, yml_path.parent)
        return result

    @dataclass
    class docker_result_class:
        result: bool
        service_list: list = ""
        ip: str = "0.0.0.0"
        port: int = 0
        message: str = ""
        stdout: str = ""
        stderr: str = ""

    async def deploy(self, userid, classid, service_name, client_ip):
        # サービスの存在を確認
        service_path = self.select_service(service_name)
        if not service_path:
            return self.docker_result_class(
                result=False,
                message="指定されたサービスが見つかりません。",
                service_list=self.get_yml_list_str())
        # 前回の立ち上げからサービスファイルが変更なければそのまま
        cache_port = self.get_port_from_service_cache(
            classid, userid, service_name)
        if cache_port is not None:
            return self.docker_result_class(
                result=True,
                message="キャッシュを利用",
                ip=self.get_ip_address(client_ip)[0],
                port=cache_port,)
        # 新規or サービスファイルに変更があったとき
        _port = await self.scan_available_port(50000)
        new_yml = self.make_yml(service_path, _port, userid, classid)
        result = await self.deploy_service(new_yml, f"{classid}-{userid}")
        new_yml.unlink()
        self.port_candidate.remove(_port)
        if result.returncode != 0:
            return self.docker_result_class(
                result=False,
                message="docker 実行中にエラーが生じました",
                stdout=result.stdout,
                stderr=result.stderr)
        self.add_service_cache(classid, userid, service_name, _port)
        return self.docker_result_class(
            result=True,
            ip=self.get_ip_address(client_ip)[0],
            port=_port,)


if __name__ == "__main__":
    hoge = docker()
    test = hoge.get_yml_list()
    print(test)
    print(hoge.make_yml(test[0], 1000, "dasd", "fgadsfa"))