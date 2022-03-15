# セットアップ方法
## 実行環境の作成

### python3のインストール
本システムはfastapiを用いるため、python3.6以上が必要です。
```bash
sudo apt install python3-pip
```

### dockerのインストール
dockerのインストールを行います。
dockerコマンドがsudoなしで実行できるように変更を行ってください。
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo groupadd docker
sudo usermod -aG docker $USER
# 再ログイン後にsudoなしで実行できることを確認
docker ps
```

### dockerの設定
docker swarmの設定を行います。
初期状態ではingressのサブネットマスクが24なため、
ポート開放可能数が250個ほどに制限されます。
それ以上のポートを利用する場合はingressを削除し、再度手動で作成し直します。
```bash
docker swarm init
# 250以上ポート転送をする場合
docker network rm ingress
docker network create \
    --driver overlay \ 
    --ingress \
    --subnet=10.0.0.0/16 \
    --gateway=10.0.0.1 \
    --opt com.docker.network.mtu=1400 \
    ingress
```

## eALPluS-docker-apiの実行

### レポジトリのクローン
eALPluS-docker-apiをレポジトリから取得します。
```bash
git clone https://github.com/penM000/eALPluS-docker-api
```

### eALPluS-docker-apiの実行
下記コマンドで実行が可能です。
この場合、ターミナルの終了とともにapiも終了するため、
systemdやtmuxなどで実行を持続させることを推奨します。
```bash
cd eALPluS-docker-api
./start.sh
```

### 動作確認
実行後、下記のように応答があれば動作しています。
```bash
curl 127.0.0.1:10001
# 応答
{"message":"Hello Bigger Applications!"}
```

## eALPluSに登録


```bash
http://{IPアドレス}:{ポート番号}/docker?ealps_sid&ealps_cid&service_name=jupyterlab
```
