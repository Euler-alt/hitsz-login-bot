#!/bin/bash

# 获取当前脚本所在目录（确保软链接指向真实路径）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/toggle_v2ray.sh"
LINK_NAME="$HOME/.local/bin/v2"

# 创建 ~/.local/bin 如果不存在
mkdir -p "$HOME/.local/bin"

# 删除旧的软连接（如果存在）
if [ -L "$LINK_NAME" ]; then
  echo "旧的软连接已存在，正在移除..."
  rm "$LINK_NAME"
fi

# 创建新的软连接
ln -s "$TARGET" "$LINK_NAME"
echo "✅ 软连接创建成功：$LINK_NAME -> $TARGET"

# 确保 ~/.local/bin 在 PATH 中
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
  echo "✅ 已将 ~/.local/bin 添加至 PATH（下次终端生效或运行 source ~/.bashrc）"
else
  echo "ℹ️  ~/.local/bin 已在 PATH 中"
fi
