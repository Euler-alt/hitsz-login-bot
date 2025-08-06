# 进入工作目录
mkdir -p ~/v2ray && cd ~/v2ray

# 下载 V2Ray 最新 release（国内可试试代理）
curl -LO https://github.com/v2fly/v2ray-core/releases/latest/download/v2ray-linux-64.zip

# 解压
apt update && apt install -y unzip
unzip v2ray-linux-64.zip
chmod +x v2ray v2ctl
