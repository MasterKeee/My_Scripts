import requests
import pandas as pd
from time import sleep


def CET4(name, sfzh):
    params = {
        "km": "1",
        "xm": item[1]['姓名'],
        "no": item[1]['身份证号'],
        "source": "pc"
    }
    response = requests.get(
        "https://cachecloud.neea.cn/api/latest/results/cet", headers=headers, params=params)
    if response.status_code == 200:
        json_data = response.json()
        print(json_data)
        return json_data


def CET6(name, sfzh):
    params = {
        "km": "2",
        "xm": item[1]['姓名'],
        "no": item[1]['身份证号'],
        "source": "pc"
    }
    response = requests.get(
        "https://cachecloud.neea.cn/api/latest/results/cet", headers=headers, params=params)
    if response.status_code == 200:
        json_data = response.json()
        return json_data


headers = {
    "authority": "cachecloud.neea.cn",
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://cjcx.neea.edu.cn",
    "referer": "https://cjcx.neea.edu.cn/",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}
df = pd.read_excel("C:/Users/kejio/Desktop/CET.xlsx",
                   dtype={'姓名': str, '身份证号': str, '四级': str, '六级': str})
for item in df.iterrows():
    sfzh = item[1]['身份证号']
    name = item[1]['姓名']
    json_data = CET4(name, sfzh)
    if json_data['code'] == 0:
        df.at[item[0], '四级'] = json_data['score']
        df.to_excel("C:/Users/kejio/Desktop/CET.xlsx", index=False)
        print(f"查询成功，{name}的四级成绩为{json_data['score']}，保存成功")
    elif json_data['code'] == 404 and json_data['msg'] == '您所提供的考试科目或个人信息有误，请核实后再查询。':
        json_data = CET6(name, sfzh)
        if json_data['code'] == 0:
            df.at[item[0], '六级'] = json_data['score']
            df.to_excel("C:/Users/kejio/Desktop/CET.xlsx", index=False)
            print(f"查询成功，{name}的六级成绩为{json_data['score']}，保存成功")
    sleep(0.5)
