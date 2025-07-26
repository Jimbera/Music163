import hashlib
from urllib.parse import urlparse, parse_qs
import os
from lxml import etree
import requests
from tqdm import tqdm

# 在这里填入网易云歌单分享链接
url = str(input("歌单分享链接"))  #"https://music.163.com/m/playlist?id=2492467414&creatorId=621118881"

parsed_url = urlparse(url)
query_params = parse_qs(parsed_url.query)

playlist_id = query_params.get('id')
user_id = query_params.get('creatorId')

cookies = {
    'NMTID': '00OsjFxYs1P9RGLpkNShgkZZfSkok8AAAGODzJfKw',
    '_iuqxldmzr_': '32',
    '_ntes_nnid': '738cda36775317a42251a24e570421fc,1709651943723',
    '_ntes_nuid': '738cda36775317a42251a24e570421fc',
    'WEVNSM': '1.0.0',
    'WNMCID': 'oxbbjw.1709651944555.01.0',
    'WM_TID': 'glGlKf31W%2F1FFBQEVQfRvUHqHk0osZXT',
    'ntes_utid': 'tid._.%252B%252Fi2PtWDIq9ABgRBRBKVvASrCxhtr9Z6._.0',
    'sDeviceId': 'YD-NPkO6O3x1i9AB1UAFVPEkoQU3I1SOfNg',
    'WM_NI': 'p9Fn0Gf85fqVExC9YGQZ3Nw6Y9hiNH8CCciGynIi4LVtJ%2BjyCQ7gQAfdtXGC49A7%2F%2Bb0SOdk6ubisEe8FlAaE%2FMOyqHNSy9euPJgooJjT5OBF%2FMF3fAVlrAZmjo9QRUYcEk%3D',
    'WM_NIKE': '9ca17ae2e6ffcda170e2e6eeb8ca45f3eb8b82fb4089a88fb7c15b939f8b87d47a8fa8ae92d56db4b68989d32af0fea7c3b92ab4e78a8fb34da6e8fb87f45e87a88ddadc4d9386fdaff63e9be7a88acd44fc9d8d84ec4dbbb2878ab74896ac86cce973818ff988d44ba6bcbcb9c649f8e78fd8ae21a2f09db0e761f6abae8af24fa7e88a8dc46b87f183b0fc7b8c929d9abc6fb7908688ee658ab69cd6ce4a86f183a7b26e838aa493c452afb6a1dad45a9787ada6ea37e2a3',
    'os': 'pc',
    'JSESSIONID-WYYY': '08y6d5SVPnTq%5CaVosBEDGE%2FUC048fa62F%2B1jt1nGhpXm1u5DZE%5CQFZGBNA%5C7kc%5CzHGrEkF2Bw7Pd%2Be0K18XZtmYilyNYixlm4QlFgweDSSclnNGuO5WPE3%2BcIR%2Fm96AoVSIBfqtgqV4hasxkCVrslwjPBEFx%5CPhSnc1fqVt%2FKYqfR1s%2B%3A1712151786748',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'referer': 'https://music.163.com/',
    'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'iframe',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
}

params = {
    'id': playlist_id[0],
    'userid': user_id[0],
}

response = requests.get('https://music.163.com/playlist', params=params, cookies=cookies, headers=headers)

html = response.text

# 创建HTML解析对象
parser = etree.HTMLParser()
tree = etree.HTML(html)

# 使用XPath提取歌曲链接和歌曲名称
tree = etree.HTML(html)
song_links = tree.xpath('//ul[@class="f-hide"]/li/a/@href')

# 组合链接和名称
output = []
for song_link in song_links:
    full_link = "https://music.163.com" + song_link
    output.append(full_link)

# 打开文件准备写入数据
with open("links.txt", "w") as file:
    for link in output:
        file.write(link + "\n")

# 打印完成提示qaq
print("结果已写入到links.txt文件中，准备下载音乐中")

import os

# 创建保存音乐的文件夹
save_folder = ("网易云音乐")
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 音质选择菜单
print("\n请选择下载音质（回车确认）:")
print("1. 标准音质 (standard)")
print("2. 极高音质 (exhigh)")
print("3. 无损音质 (lossless)")
print("4. 高解析度无损 (hires)")
print("5. 高清环绕音 (jyeffect)")
print("6. 沉浸环绕硬音 (sky)")
print("7. 超声母带 (jymaster)")

# 音质选项映射4
quality_options = {
    "1": "standard",
    "2": "exhigh",
    "3": "lossless",
    "4": "hires",
    "5": "jyeffect",
    "6": "sky",
    "7": "jymaster"
}

# 获取输入并验证
while True:
    choice = input("\n请输入数字(1-7)选择音质: ")
    if choice in quality_options:
        m_yz = quality_options[choice]
        print(f"\n已选择: {m_yz} 音质")
        break
    else:
        print("无效输入，请输入1-7之间的数字")

from tqdm import tqdm

# 首先获取总任务数
total_songs = sum(1 for _ in open('links.txt', 'r'))

# 打开文本文件并逐行读取链接
with open('links.txt', 'r') as file:
    # 创建总体进度条，设置动态刷新参数
    progress_bar = tqdm(total=total_songs, desc="总体进度",
                        position=0, leave=True, dynamic_ncols=True)

    for i, line in enumerate(file, 1):
        try:
            lburl = line.strip()

            headers_token = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'origin': 'https://api.toubiec.cn',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://api.toubiec.cn/wyapi.html',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.265", "Chromium";v="131.0.6778.265", "Not_A Brand";v="24.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"19.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }

            response_token = requests.post('https://api.toubiec.cn/api/get-token.php', headers=headers_token)
            token_data = response_token.json()  # 将响应转换为JSON
            token_token = token_data['token']  # 提提取取token值

            # 对token进行MD5加密（32位小写）
            md5_hash = hashlib.md5(token_token.encode()).hexdigest()

            headers = {
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'authorization': f'Bearer {token_token}',
                'cache-control': 'no-cache',
                'content-type': 'application/json',
                'origin': 'https://api.toubiec.cn',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'referer': 'https://api.toubiec.cn/wyapi.html',
                'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.265", "Chromium";v="131.0.6778.265", "Not_A Brand";v="24.0.0.0"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-model': '""',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-platform-version': '"19.0.0"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            }

            json_data2 = {
                'url': lburl,
                'level': m_yz,
                'type': 'song',
                'token': md5_hash,
            }

            response2 = requests.post('https://api.toubiec.cn/api/music_v1.php', headers=headers, json=json_data2)

            data2 = response2.json()
            url2 = data2['url_info']['url']
            name = data2.get("song_info", {}).get("name")

            # 下载音乐文件
            res = requests.get(url2, stream=True)
            file_name = os.path.join(save_folder, f"{name}.flac")

            # 获取文件大小
            total_size = int(res.headers.get('content-length', 0))

            # 创建文件下载进度条
            with open(file_name, "wb") as f:
                with tqdm(total=total_size,
                          desc=f"正在下载: {name}",
                          unit='B',
                          unit_scale=True,
                          position=1,
                          leave=False,
                          dynamic_ncols=True,
                          bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]') as pbar:

                    for chunk in res.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))

            # 更新总进度
            progress_bar.update(1)
            # 清空当前行并显示完成信息
            print(f"\r✓ {name} 下载完成", flush=True)

        except Exception as e:
            print(f"\r错误: 无法下载 - {e}", flush=True)
            continue

    # 关闭总进度条
    progress_bar.close()

print("\n所有音乐下载完成，请查阅")