from fastapi import FastAPI, Request
from .internal.docker import docker as docker_class

app = FastAPI()
docker = docker_class()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/docker")
async def root(request: Request, ealps_cid: str, ealps_sid: str, service_name: str):
    result = await docker.deploy(ealps_sid, ealps_cid, service_name, request.client.host)
    if result.result:
        return result
    else:
        return result
