#!/bin/bash
nohup ./auto.sh > autologin.log 2>&1 &
echo "AutoLogin 脚本已在后台启动，日志输出到 autologin.log"