import requests
import os
import shutil

def fetch_song_data():
    url = "https://music.liuzhijin.cn/"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Google Chrome\";v=\"122\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
    }
    data = {
        "input": "把回忆拼好给你",
        "filter": "name",
        "type": "netease",
        "page": 1
    }
    response = requests.post(url, headers=headers, data=data)  
    return response.json()

def download_song(song_data):
    song_url = song_data['url']
    song_title_author = '{}_{}'.format(song_data['title'], song_data['author'])
    response = requests.get(song_url, stream=True)
    file_path = 'D:/'+ song_title_author + '.mp3'
    if response.status_code == 200:
        with open(file_path, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    else:
        print('Unable to download song')
        return
    upload_to_webdav(file_path, song_title_author + '.mp3')

def upload_to_webdav(local_file, remote_file_name):
    url = "https://cloud.masterke.cn/dav/" + remote_file_name
    auth = ('music', 'masterke@123')

    with open(local_file, 'rb') as f:
        file_data = f.read()

    response = requests.put(url, data=file_data, auth=auth)

    if response.status_code == 201:
        print("Upload successful.")
    else:
        print("Upload failed, returned code:", response.status_code)

def main():
    musics = [""]
    song_data_list = fetch_song_data()['data']
    song_data_list = song_data_list[:1]
    for song_data in song_data_list:
        download_song(song_data)

if __name__ == "__main__":
    main()