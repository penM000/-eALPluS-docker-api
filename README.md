# eALPluS-docker-api
デフォルトのサブネットだと枯渇
docker network create --driver overlay --ingress --subnet=10.0.0.0/16 --gateway=10.0.0.1 --opt com.docker.network.mtu=1400 ingress
```docker swarm init --default-addr-pool 10.0.0.0/8 --default-addr-pool-mask-length 16```
