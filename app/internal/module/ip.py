from ipaddress import (
    ip_interface, ip_address)
import time
import socket
import os
import psutil
import netifaces as ni
from functools import lru_cache
from typing import List


class ip:
    def __init__(self):
        self.cache_timer = time.time()

    def get_ip_address(self, client_ip: str = "0.0.0.0") -> List[str]:
        if time.time() - self.cache_timer > 10:
            self.cache_get_ip_address.cache_clear()
            self.cache_timer = time.time()
        return self.cache_get_ip_address(client_ip)

    @lru_cache(maxsize=128)
    def cache_get_ip_address(self, client_ip: str = "0.0.0.0") -> List[str]:
        """
        概要:
            このAPIが動作しているIPアドレスから、
            引数で渡されたIPアドレスと同一ネットワーク上のものを検索する。
        返り値:
            ipアドレスのリスト
        """
        if os.name == "nt":
            # Windows
            return socket.gethostbyname_ex(socket.gethostname())[2]
            pass
        else:
            # それ以外
            result = []
            address_list = psutil.net_if_addrs()
            for nic in address_list.keys():
                try:
                    temp = ni.ifaddresses(nic)[ni.AF_INET][0]
                    ip_adress = temp['addr']
                    subnet = temp['netmask']
                    ip = ip_interface(f"{ip_adress}/{subnet}")
                    if ip_address(client_ip) in ip.network:
                        return [str(ip.ip)]
                    if ip_adress not in ["127.0.0.1"]:
                        result.append(str(ip_adress))
                except KeyError as err:
                    # print(err)
                    err
                    pass
            return result
