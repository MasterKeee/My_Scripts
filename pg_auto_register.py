import requests
import time
import json
import pandas as pd
import os
import re

# 把变量存在青龙中
class QL:
    def __init__(self, address: str, id: str, secret: str) -> None:
        """
        初始化
        """
        self.address = address
        self.id = id
        self.secret = secret
        self.valid = True
        self.login()
    def login(self) -> None:
        """
        登录
        """
        url = f"{self.address}/open/auth/token?client_id={self.id}&client_secret={self.secret}"
        try:
            rjson = requests.get(url).json()
            if(rjson['code'] == 200):
                self.auth = f"{rjson['data']['token_type']} {rjson['data']['token']}"
            else:
                self.log(f"登录失败：{rjson['message']}")
        except Exception as e:
            self.valid = False
            self.log(f"登录失败：{str(e)}")

    def log(self, content: str) -> None:
        """
        日志
        """
        print(content)
    def addEnvs(self, envs: list) -> bool:
        """
        新建环境变量
        """
        url = f"{self.address}/open/envs"
        headers = {"Authorization": self.auth,"content-type": "application/json"}
        try:
            rjson = requests.post(url, headers=headers, data=json.dumps(envs)).json()
            if(rjson['code'] == 200):
                self.log(f"\033[32m【5】新建环境变量成功：{len(envs)}\033[0m")
                return True
            else:
                self.log(f"新建环境变量失败：{rjson['message']}")
                return False
        except Exception as e:
            self.log(f"新建环境变量失败：{str(e)}")
            return False
        
# 登录接码平台
response = requests.get('http://api.sqhyw.net:90/api/logins?username=kejiovo&password=kejiovo.')
rjson = response.json()
if (response.status_code == 200) & (rjson['message'] == "登录成功"):
    jiema_token = rjson['token']
    print(f"接码登录成功🎉\n============\n用户ID：{rjson['data'][0]['id']}\n余额：{rjson['data'][0]['money']}\ntoken：{jiema_token}\n登录IP：{rjson['data'][0]['ip']}\n============")

for i in range(1,70):
    flag = 1
    print(f"\033[31m⌛️本次运行注册第{i}个...\033[0m")
    ip = requests.get('https://myip.ipip.net/').text
    print(ip)
    # 获取手机号
    response = requests.get(f'http://api.sqhyw.net:90/api/get_mobile?token={jiema_token}&project_id=31570')
    rjson = response.json()
    if (response.status_code == 200) & (rjson['message'] == "ok"):
        mobile = rjson['mobile']
        print(f"\033[32m【1】获取手机号:{mobile}\033[0m")
        print(rjson)

    # 发送验证码
    url = "https://userapi.qiekj.com/common/sms/sendCode"
    data = {
        'phone': mobile,
        'template': 'reg'
    }

    headers = {
        "Authorization":"",
        "Version":"1.50.0",
        "channel":"android_app",
        "phoneBrand":"OnePlus",
        "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8",
        "Content-Length":"30",
        "Host":"userapi.qiekj.com",
        "Connection":"Keep-Alive",
        "Accept-Encoding":"gzip",
        "User-Agent":"okhttp/3.14.9"
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200 and response.json()['code'] == 0:
        print('\033[32m【2】发送验证码成功\033[0m')
        print(response.text)
    else:
        print('验证码发送失败✖')
        
    # 获取验证码
    times = 1
    while True:
        response = requests.get(f'http://api.sqhyw.net:90/api/get_message?token={jiema_token}&project_id=31570&phone_num={mobile}')
        data = json.loads(response.text)
        if 'code' not in data:
            if times == 10:
                print(f"验证码获取失败，下一個账号...")
                flag = 0
                break   
            time.sleep(5)
            print(f"第{times}次获取，等待5秒...")
            times+=1
            continue

        code = data['code']
        print(f"\033[32m【3】从接码平台获取到验证码:{code}\033[0m")
        print(data)
        break
    if not flag:
        continue
    # 使用验证码进行登录操作，获取token
    url2 = "https://userapi.qiekj.com/user/reg"
    headers2 = headers
    headers2["Content-Length"] = "49"

    data2 = {
        'channel': 'android_app',
        'phone': mobile,
        'verify': code
    }

    response2 = requests.post(url2, headers=headers2, data=data2)
    token = response2.json()['data']['token']
    print(f"\033[32m【4】获取token成功:{token}\033[0m")
    print(response2.text)


    address = "http://10.1.1.2:5700"
    client_id = "ahI_LKu4-R5z"
    client_secret = "J9CPDRmlspMUJ35r8Tk2EBg-"
    ql = QL(address, client_id, client_secret)
    envs = ql.addEnvs([{"name": "pgsh2", "value": f"{token}#{mobile}#UID_yPTyHAGdYDZ0nwpuhuA6udlxpAk4"}])

    # 手机号码和token存起来
    # 创建一个字典，它包含我们想要存入Excel的数据
    data = {'手机号': [mobile],
            'token': [token]}
    df = pd.DataFrame(data)
    file_name = 'D:/pgsh.xlsx'
    # 判断文件是否已存在
    if os.path.isfile(file_name):
        # 如果文件已存在，读入原文件并在底部追加新数据
        df_old = pd.read_excel(file_name)
        df = pd.concat([df_old, df])
    # 将数据写入文件，如果文件不存在将会新建
    df.to_excel(file_name, index=False)
    account_number = df.shape[0]
    print(f"\033[32m【6】第{account_number}个注册成功:[手机号：{mobile}][token：{token}]\033[0m")
    
    # 开关数据网络切换IP
    print(f"\033[32m【7】切换IP中...\033[0m")
    response = requests.get('http://192.168.42.1:9999/click?x=683&y=1091')
    print(f"✖关闭数据网络")
    time.sleep(1)
    response = requests.get('http://192.168.42.1:9999/click?x=683&y=1091')
    print(f"✔开启数据网络")
    time.sleep(3)
    old_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ip)[0]
    ip = requests.get('https://myip.ipip.net/').text
    new_ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ip)[0]
    print(f"IP变动:{old_ip} => {new_ip}")