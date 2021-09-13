import psutil
import random
import asyncio
from typing import List, Dict

from functools import wraps, partial


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


class port:
    def __init__(self):
        self.port_candidate = []
        pass

    async def get_listen_status(self) -> List[int]:
        net_status = await async_wrap(psutil.net_connections)()
        listen_ports = [int(conn.laddr.port) for conn in net_status
                        if conn.status == 'LISTEN']

        listen_ports = sorted(set(listen_ports))
        return listen_ports

    async def get_used_port(self) -> List[int]:
        """
        現在利用中のportと割り当て済みのport一覧作成
        """
        used_ports = await self.get_listen_status()
        used_ports.extend(self.port_candidate)
        used_ports = sorted(set(used_ports))
        return used_ports

    async def check_port_available(self, port: int) -> bool:
        used_ports = await self.get_used_port()
        if (port in used_ports):
            return False
        else:
            return True

    async def scan_available_port(self, start_port: int, mode: str = "random") -> int:
        """
        概要:
            このAPIが動作しているコンピューターの空きポートを検索する関数
        動作モード:
            random: ポート割当はランダム
            countup: 最初からきれいにポートを割り当てる
        返り値:
            割当可能なポート番号(int)
        """
        port_offset = 0
        used_ports = await self.get_used_port()
        available_port_count = (65535 - start_port) - len(
            [1 for x in used_ports if x >= start_port])
        if available_port_count < 10:
            raise Exception("利用可能なport上限を超えました")
        while True:
            if mode == "random":
                port_candidate = random.randint(start_port, 65535)
            elif mode == "countup":
                port_candidate = start_port + port_offset
            if port_candidate in used_ports:
                port_offset += 1
                continue
            else:
                self.port_candidate.append(port_candidate)
                print(self.port_candidate)
                return port_candidate
