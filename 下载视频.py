import youtube_dl

def download_video(url, output_dir):
    ydl_opts = {
        'outtmpl': output_dir + '/%(title)s.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 输入下载链接和保存文件夹
url = input("请输入要下载的视频链接：")
output_dir = input("请输入保存视频的文件夹路径：")

# 调用函数下载视频
download_video(url, output_dir)
