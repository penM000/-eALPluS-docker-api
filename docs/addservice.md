# サービスの追加方法
serviceフォルダにサービス名にしたいフォルダを作成し、內部に
「docker-compose.yml」を必ず含んでください。
また、「docker-compose.sh」が存在する場合

1. docker-compose.sh
1. docker-compose.yml

の順番に実行されます。

例えば下記のような場合はカレントディレクトリにユーザごとフォルダを生成し、
個別にマウントを行うことができます。

**注:コマンド実行時のカレントディレクトリは、スクリプト、及びymlファイルが配置されている場所です。**

**注:docker-compose.shは初回アクセス時、ymlファイルの変更後のアクセス時に実行されます。**

**注:永続化されていない領域は様々な要因によって容易に揮発します。**



```bash
#!/bin/bash
# docker-conpose.shは、docker-conpose.ymlより先に実行されるスクリプトです。
# 実行時下記の名称に完全一致する場合、置き換わります。
# {automatic_allocation_port}=自動的に割り当てられるポート番号
# {userid} = 学籍番号に置換される
# {classid} = 授業コードに置換される
# ユーザーごとにフォルダを作成したい場合は
# mkdir -p ./save/{classid}/{userid}
# としてください。この場合下記のように置き換わり実行されます。
# mkdir -p ./save/AB12345/12A34567B
mkdir -p ./save/{classid}/{userid}
```

```yml
# {servicename} 親フォルダ名 この場合はjupyterlab
# {automatic_allocation_port}=自動的に割り当てられるポート番号
# {userid} = 学籍番号に置換される
# {classid} = 授業コードに置換される
version: '3'
services:
  notebook:
    image: code-server-c-program
    ports:
      - '{automatic_allocation_port}:8080'
    command: code-server --auth none /home/coder
    volumes:
      - $PWD/save/{classid}/{userid}:/home/jovyan/{userid}
```
