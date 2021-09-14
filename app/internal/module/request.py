import aiohttp
import asyncio


class request_class:
    async def request(self, url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as resp:

                    await resp.text()
                    return True
            except aiohttp.client_exceptions.ClientConnectorError:
                # 接続に失敗したとき
                return False
            except aiohttp.client_exceptions.ClientResponseError:
                # 接続に成功したが、値がおかしいとき
                return True
            except UnicodeError:
                # URLがおかしいとき
                return False
            except aiohttp.client_exceptions.InvalidURL:
                # httpが欠落しているとき
                return await self.request(f"http://{url}")
            except Exception:
                # その他の例外
                return False

    async def start_check(self, url: str, timeout: int = 60):
        for loop in range(timeout):
            if await self.request(url):
                return True
            await asyncio.sleep(1)
        return False


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    hoge = request_class()
    result = loop.run_until_complete(hoge.request("127.0.0.1"))
    print(result)
