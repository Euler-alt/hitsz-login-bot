import ipaddress

def generate_ip_list_with_second_octet_range(network_str, second_octet_range=(240, 255), step=128, output_file="iplist.txt"):
    net = ipaddress.ip_network(network_str)
    count = 0
    with open(output_file, "w") as f:
        for i, ip in enumerate(net.hosts()):
            octets = str(ip).split(".")
            second_octet = int(octets[1])
            if second_octet < second_octet_range[0] or second_octet > second_octet_range[1]:
                continue
            if count % step == 0:
                f.write(str(ip) + "\n")
            count += 1
    print(f"已写入 {output_file}")

if __name__ == "__main__":
    generate_ip_list_with_second_octet_range("10.0.0.0/8", second_octet_range=(240, 255), step=128)
