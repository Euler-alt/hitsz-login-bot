import json
import os
import time

import requests
import re
import jsvm
import logging
import argparse

CALLBACK = "jQuery112405302136813850036_1751349120222"
HOST = "net.hitsz.edu.cn"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
log = logging.getLogger()

def _time_stamp():
    return str(int(time.time() * 1000))


class LoginRobot:
    def __init__(self,username,password,host):
        self.password = password
        self.username = username
        self.host = host
        self.running = True


    def check_net(self,retries = 3,delay=2,url="http://connect.rom.miui.com/generate_204"):
        for attempt in range(1, retries + 1):
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 204:
                    return True
            except Exception as e:
                log.warning(f"[!] 第 {attempt} 次检查网络失败：{e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    log.error("[!] 检查网络失败，请检查网络连接。")
                    return False
    def tick_login(self,tick=30):
        while self.running:
            try:
                if not self.check_net():
                    log.info("[!] 网络未连接，正在尝试...")
                    self.login()
            except Exception as e:
                log.error(f"[X] tick_login 内部异常: {e}", exc_info=True)
            time.sleep(tick)


    def login(self):
        ip, acid,login = self.getView()
        if not login:
            log.info("[!] 网络未登录，开始尝试登录...")
            challenge = self.get_challenge()
            encrypted_password, checksum, info = self.get_cryption(challenge,ip,acid)
            self.authenticate(encrypted_password,checksum,ip,info)
        else:
            log.info("[✓] 当前已登录。")


    def getView(self, retries=3, delay=2):
        for attempt in range(1, retries + 1):
            try:
                resp = requests.get(f"https://{self.host}/srun_portal_pc?ac_id=1&theme=basic4", timeout=5)
                break  # 成功了就跳出重试
            except Exception as e:
                log.warning(f"[!] 第 {attempt} 次获取页面失败：{e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    log.error("[!] 获取页面失败，请检查网络连接。")
                    return "", "", False

        html_text = resp.text
        def is_logged_in(html_text):
            # 如果页面含有登录页面特有的字段，判定为未登录
            login_indicators = [
                'id="username"',  # 用户名输入框
                'id="password"',  # 密码输入框
                '验证码',  # 登录页一般有验证码
                '统一身份认证',  # 登录按钮文字
                '本地用户登录',
                'btn-login',  # 登录按钮的class/id
            ]
            for indicator in login_indicators:
                if indicator in html_text:
                    return False  # 未登录
            return True  # 已登录

        if is_logged_in(html_text):
            return "","",True
        else:
            ip_match = re.search(r'ip\s*:\s*"([^"]*)"', html_text)
            acid_match = re.search(r'acid\s*:\s*"([^"]*)"', html_text)
            ip = ip_match.group(1) if ip_match else ""
            acid = acid_match.group(1) if acid_match else ""
            return ip, acid, False  # 未登录，返回ip和acid用于登录


    def get_challenge(self,retries=3, delay=2):
        parameter = {
            "callback": CALLBACK,
            "username": self.username,
            "_": _time_stamp()
        }
        url = f"https://{self.host}/cgi-bin/get_challenge"

        for attempt in range(1, retries + 1):
            try:
                response = requests.get(url, params=parameter, timeout=5)
                jsonp_text = response.text
                json_str = re.search(r'\((.*)\)', jsonp_text).group(1)
                data = json.loads(json_str)
                if data["error"] == "ok":
                    return data["challenge"]
                else:
                    raise ValueError(f"get_challenge returned error: {data}")

            except Exception as e:
                log.warning(f"[!] 第 {attempt} 次获取 challenge 失败：{e}")
                if attempt < retries:
                    time.sleep(delay)
                else:
                    log.error(f"[X] 最终尝试失败，无法获取 challenge。")
                    raise  # 或者 raise e 让外层捕获

    def get_cryption(self, cha:str,ip:str,acid:str):
        """
        :param acid:
        :param ip:
        :param cha:
        :return:  password, chksum, info
        """

        login_info = {
            "username": self.username,
            "password": self.password,
            "ip": ip,
            "acid": acid,
            "enc_ver": "srun_bx1"
        }

        info_encode = jsvm.info_encode()
        md5 = jsvm.new_md5()
        sha1 = jsvm.new_sha1()

        info = info_encode.call("value", login_info, cha)
        hmd5 = md5.call("md5", self.password, cha)

        chkstr = cha + self.username
        chkstr += cha + hmd5
        chkstr += cha + acid
        chkstr += cha + ip
        chkstr += cha + "200"
        chkstr += cha + "1"
        chkstr += cha + info

        chksum = sha1.call("sha1", chkstr)
        encrypted_password = "{MD5}" + hmd5

        return encrypted_password, chksum, info


    def authenticate(self,password_cription,checksum,ip,info,callback=CALLBACK,url="https://"+HOST+"/cgi-bin/srun_portal",retries=3,time_out=1):
        param = {
            "callback": callback,
            "action": "login",
            "username": self.username,
            "password": password_cription,
            "os": "Windows 10",
            "name": "Windows",
            "nas_ip": "",
            "double_stack": 0,
            "chksum": checksum,
            "info": info,
            "ac_id" : 1,
            "ip" : ip,
            "n" : "200",
            "type" : "1",
            "captchaVal":"",
            "_" : _time_stamp(),
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        for attempt in range(1, retries + 1):
           try :
                resp = requests.get(url,params=param,timeout =3,headers=headers)
                status,text =resp.status_code, resp.text
                if status == 200:
                    if "Authentication success,Welcome" or "Login is successful" in text:
                        log.info("[✓] 登录成功。")
                        return True
                    else:
                        return False
           except Exception as e:
                log.warning(f"[!] 第 {attempt} 次尝试登录失败：{e}")
                if attempt < retries:
                    time.sleep(time_out)
                else:
                    log.error(f"[X] 登录失败，请检查用户名密码。")
                    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="网络登录机器人")
    parser.add_argument("--username", "-u", help="用户名", required=False)
    parser.add_argument("--password", "-p", help="密码", required=False)
    parser.add_argument("--tick", "-t", type=int, default=60 * 5, help="检测间隔秒，默认300秒")

    args = parser.parse_args()

    # 优先使用命令行参数，没有时退回环境变量
    userName = args.username if args.username else os.getenv("userName")
    passWord = args.password if args.password else os.getenv("password")

    if not userName or not passWord:
        print("错误：请通过 --username 和 --password 提供用户名和密码，或者设置环境变量 userName 和 password")
        exit(1)
    loginRobot = LoginRobot(userName,passWord,HOST)
    loginRobot.tick_login(tick=60*5)