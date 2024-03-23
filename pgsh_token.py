import requests

# 输入手机号
phone_number = input('请输入手机号码：')

# 发送验证码
url = "https://userapi.qiekj.com/common/sms/sendCode"
data = {
    'phone': phone_number,
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

# 提示用户查看手机，并输入收到的验证码
verify_code  = input('请查看手机验证码，并输入：')

# 使用验证码进行登录操作，获取token
url2 = "https://userapi.qiekj.com/user/reg"
headers2 = headers
headers2["Content-Length"] = "49"

data2 = {
    'channel': 'android_app',
    'phone': phone_number,
    'verify': verify_code
}

response2 = requests.post(url2, headers=headers2, data=data2)
token = response2.json()['data']['token']

print(f'Token: {token}')