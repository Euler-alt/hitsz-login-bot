#!/bin/bash
while true; do
  /opt/conda/bin/python /home/dev/AutoLogin/autologin.py -u xxxxxxxx -p xxxxxx -t 60
  echo "脚本异常退出，5秒后重启..."
  sleep 5
done
