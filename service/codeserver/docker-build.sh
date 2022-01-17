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
docker build -t code-server-c-program .

#mkdir -p ./save/{classid}/{userid}
