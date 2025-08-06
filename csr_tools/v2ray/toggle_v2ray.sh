#!/bin/bash

# 获取脚本所在目录
get_script_dir() {
  SOURCE="${BASH_SOURCE[0]}"
  while [ -L "$SOURCE" ]; do
    DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
  done
  DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
  echo "$DIR"
}

SCRIPT_DIR=$(get_script_dir)

# 解析参数，默认 config.json，拼接成绝对路径
CONFIG="$SCRIPT_DIR/JA01F-config.json"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -A1)
      CONFIG="$SCRIPT_DIR/JA01F-config.json"
      shift
      ;;
    -A2)
      CONFIG="$SCRIPT_DIR/US01C-config.json"
      shift
      ;;
    -Jap)
      CONFIG="$SCRIPT_DIR/US01G-config.json"
      shift
      ;;
    *)
      echo "未知参数: $1"
      echo "用法: $0 [-A1] [-A2] [-Jap]"
      exit 1
      ;;
  esac
done

pids=$(ps aux | grep "[v]2ray run" | awk '{print $2}')

if [ -z "$pids" ]; then
  echo "v2ray 未运行，尝试启动配置 $CONFIG ..."
  nohup "$SCRIPT_DIR/v2ray" run -c "$CONFIG" > "$SCRIPT_DIR/v2ray.log" 2>&1 &
  sleep 1
  new_pid=$(pgrep -f "v2ray run -c $CONFIG")
  if [ -n "$new_pid" ]; then
    echo "v2ray 启动成功，PID: $new_pid"
  else
    echo "⚠️ v2ray 启动失败，请查看日志 $SCRIPT_DIR/v2ray.log："
    tail -n 20 "$SCRIPT_DIR/v2ray.log"
  fi
else
  echo "v2ray 正在运行，PID(s): $pids，停止中..."
  kill $pids
  sleep 2
  pids=$(pgrep -f "v2ray run -c $CONFIG")
  if [ -n "$pids" ]; then
    echo "v2ray 未停止，强制杀死 PID(s): $pids ..."
    kill -9 $pids
  else
    echo "v2ray 已成功停止。"
  fi
fi
