def generate_sparse_ips(second_octet_range=(0, 255), step=128, output_file="iplist2.txt"):
    with open(output_file, "w") as f:
        for second_octet in range(second_octet_range[0], second_octet_range[1] + 1):
            total_hosts = 256 * 256  # 每个 B 类段有 2^16 个主机地址
            for offset in range(0, total_hosts, step):
                third_octet = (offset // 256) % 256
                fourth_octet = offset % 256
                ip = f"10.{second_octet}.{third_octet}.{fourth_octet}"
                f.write(ip + "\n")
    print(f"已生成 {output_file}")

if __name__ == "__main__":
    generate_sparse_ips(step=999)
