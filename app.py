from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import requests
import re
import hashlib
from urllib.parse import urlparse, parse_qs
from lxml import etree
import os
import io
import base64
from datetime import datetime
import tempfile

app = Flask(__name__)
CORS(app)

# 默认cookies - 可以通过API更新
default_cookies = {
    'NMTID': '00OrvYCx9CQB9BU6E--r2tR79uKfEQAAAGSI99qmQ',
    '_iuqxldmzr_': '32',
    '_ntes_nnid': '90289846b119116647b96be3b96a12b0,1752904656724',
    '_ntes_nuid': '90289846b119116647b96be3b96a12b0',
    'WEVNSM': '1.0.0',
    'WNMCID': 'dwbedg.1727178810731.01.0',
    'WM_TID': 'ois5gmZE6hpBARVQRQKGGRkbvAdK4ML5',
    'ntes_utid': 'tid._.JU1qvqv8XXxEBkFFFVPTfp%252F86AP%252BcfUR._.0',
    'WM_NI': 'xGWMWrFGF9K3teaTEOYZvoG%2B%2F8CDQpIV8yOe63ybJEG1Lv0SaSXh7OurT6R0Pwh5xg%2BFTgwOmWo4BVhjacB2%2BNO4brwZ2jo%2BYpKlaN9%2BuE3PONyp%2Fzpb0B1UGZLeXq4%2BZFM%3D',
    'WM_NIKE': '9ca17ae2e6ffcda170e2e6eed5ef689496be85fc3489b88fa7c54a879f8f83d26892ef8eccbb80909ef985c42af0fea7c3b92abc9999aed67a86998adaca39b8bbafb5c8459b86ba90c621ede88da5d47c8b8af89ace6ff6edb783c94f85ef8497b359a38d9889b645b7ae9cd7d13c94a9a8d6fb6de99a9c88f645af89a1d5c15eacb6af84c13ae99281d5e17ab586fe8bee219bb0858de446fbf5bba6b25c8d92b791ae72b4be00a3b45f85868486db7bf8f596a7d037e2a3',
    'os': 'pc',  # 这个必须是pc
    'JSESSIONID-WYYY': 'EcG1QP8ruszpe1yNpJXX%2BF48jjJk%2BQONcRoK%5C7KhKpKI6%2B8lceetZEXqf9uMJHT0fMvlzaOr101ovbZvjUlF0cW%2B8zycY1rsxyCCyV98Ot1Il3aE%2BUlmTnkze%2FRRk4%2FartE0r3xoo8ypZ7vyipagTQC9wuzUV3bDP9KGKpPWZnkdWEd9%3A1752906456669',
    '__csrf': 'caff6ceba6c81c0bd735c73cd000d1d2',
    'MUSIC_U': '001550A51A58EA2617BC0161B79B153C87A071215E5C4C9ECC7D80352E240959F0509A8E1BF8D289A4107F727A644EC8950C69A5A81D228C59B64F8C775D1F82D9B4010394ECCA2DDD646A7333CEF3B604815AB5CC2EA166C0C36EF3038738EDA77FF529CCB9F62B30EBE97BD6EC518DB963032A7A780BB94EBFBB60C03BBD87745F8FC6A5906985D6B0211092A5FE5570D621A0F4ACA7BCEAD73DDFE5DE7E33EB671B5A3321DD7E33090563FBEAB42FC112668D2810868FF43FF3B49A7F2FB525A56FB31A0D6D93CDC218E2CDF10CD063E29E82174980C2D82AF037B4945226AA5C341F6EE8D03DCD668D8B7F908EE4A8DC49ED6512E1DD08D2DCAC98BAB0EB556046F5D852F965DAE361D3A247FBAF956E85C2C94E2F55DA2AC7B746986EA016F1A152F32EC7ED1BC275F6DF76DD07573D7D92DF7CF9F3B1E6D061BEB70D472C',
}

# 当前使用的cookies（可以被更新）
cookies = default_cookies.copy()

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

@app.route('/favicon.ico')
@app.route('/favicon.svg')
def favicon():
    return send_from_directory('.', 'favicon.svg', mimetype='image/svg+xml')

@app.route('/api/parse-playlist', methods=['POST'])
def parse_playlist():
    """解析歌单，获取所有歌曲链接"""
    try:
        data = request.json
        playlist_url = data.get('url')
        
        parsed_url = urlparse(playlist_url)
        query_params = parse_qs(parsed_url.query)
        
        playlist_id = query_params.get('id')
        user_id = query_params.get('creatorId', [''])
        
        if not playlist_id:
            return jsonify({'error': '无效的歌单链接'}), 400
        
        params = {
            'id': playlist_id[0],
            'userid': user_id[0] if user_id else '',
        }
        
        response = requests.get('https://music.163.com/playlist', 
                              params=params, 
                              cookies=cookies, 
                              headers=headers)
        
        if response.status_code != 200:
            return jsonify({'error': '获取歌单失败'}), 500
        
        html = response.text
        tree = etree.HTML(html)
        
        # 提取歌单名称
        playlist_name = tree.xpath('//h2[@class="f-ff2 f-brk"]/text()')
        playlist_name = playlist_name[0] if playlist_name else '未知歌单'
        
        # 提取歌曲链接
        song_links = tree.xpath('//ul[@class="f-hide"]/li/a/@href')
        song_names = tree.xpath('//ul[@class="f-hide"]/li/a/text()')
        
        songs = []
        for i, (link, name) in enumerate(zip(song_links, song_names)):
            song_id = link.split('=')[-1]
            songs.append({
                'id': song_id,
                'name': name,
                'url': f"https://music.163.com{link}",
                'index': i + 1
            })
        
        return jsonify({
            'playlist_name': playlist_name,
            'songs': songs,
            'total': len(songs)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/parse-song', methods=['POST'])
def parse_song():
    """解析单曲链接，获取歌曲信息"""
    try:
        data = request.json
        song_url = data.get('url')
        
        # 从URL中提取歌曲ID
        song_id_match = re.search(r'[?&]id=(\d+)', song_url)
        if not song_id_match:
            return jsonify({'error': '无效的歌曲链接'}), 400
        
        song_id = song_id_match.group(1)
        
        # 这里简化处理，实际应该从页面获取歌曲信息
        # 但为了避免复杂的页面解析，我们直接返回基本信息
        return jsonify({
            'id': song_id,
            'name': f'歌曲ID: {song_id}',
            'url': song_url
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-song', methods=['POST'])
def download_song():
    """下载单个歌曲"""
    try:
        data = request.json
        song_url = data.get('url')
        quality = data.get('quality', 'lossless')
        song_name = data.get('name', 'unknown')
        
        # 获取token
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
        token_data = response_token.json()
        token_token = token_data['token']
        
        # 对token进行MD5加密
        md5_hash = hashlib.md5(token_token.encode()).hexdigest()
        
        # 获取下载链接
        headers_download = {
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
        
        json_data = {
            'url': song_url,
            'level': quality,
            'type': 'song',
            'token': md5_hash,
        }
        
        response = requests.post('https://api.toubiec.cn/api/music_v1.php', 
                               headers=headers_download, 
                               json=json_data)
        
        if response.status_code != 200:
            return jsonify({'error': '获取下载链接失败'}), 500
        
        data = response.json()
        
        if 'url_info' not in data or 'url' not in data['url_info']:
            return jsonify({'error': '无法获取下载链接'}), 500
        
        download_url = data['url_info']['url']
        actual_song_name = data.get("song_info", {}).get("name", song_name)
        
        # 下载音乐文件
        music_response = requests.get(download_url, stream=True)
        
        if music_response.status_code != 200:
            return jsonify({'error': '下载音乐文件失败'}), 500
        
        # 将音乐文件转换为base64
        music_content = music_response.content
        music_base64 = base64.b64encode(music_content).decode('utf-8')
        
        return jsonify({
            'success': True,
            'name': actual_song_name,
            'data': music_base64,
            'filename': f"{actual_song_name}.flac",
            'size': len(music_content)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-download', methods=['POST'])
def batch_download():
    """批量处理链接"""
    try:
        data = request.json
        urls = data.get('urls', [])
        quality = data.get('quality', 'lossless')
        
        results = []
        
        for url in urls:
            url = url.strip()
            if not url:
                continue
            
            if 'playlist' in url:
                # 处理歌单
                playlist_response = parse_playlist_internal(url)
                if 'error' not in playlist_response:
                    for song in playlist_response['songs']:
                        results.append({
                            'type': 'song',
                            'url': song['url'],
                            'name': song['name'],
                            'id': song['id']
                        })
            else:
                # 处理单曲
                song_id_match = re.search(r'[?&]id=(\d+)', url)
                if song_id_match:
                    results.append({
                        'type': 'song',
                        'url': url,
                        'name': f'歌曲',
                        'id': song_id_match.group(1)
                    })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_playlist_internal(playlist_url):
    """内部使用的解析歌单函数"""
    try:
        parsed_url = urlparse(playlist_url)
        query_params = parse_qs(parsed_url.query)
        
        playlist_id = query_params.get('id')
        user_id = query_params.get('creatorId', [''])
        
        if not playlist_id:
            return {'error': '无效的歌单链接'}
        
        params = {
            'id': playlist_id[0],
            'userid': user_id[0] if user_id else '',
        }
        
        response = requests.get('https://music.163.com/playlist', 
                              params=params, 
                              cookies=cookies, 
                              headers=headers)
        
        if response.status_code != 200:
            return {'error': '获取歌单失败'}
        
        html = response.text
        tree = etree.HTML(html)
        
        song_links = tree.xpath('//ul[@class="f-hide"]/li/a/@href')
        song_names = tree.xpath('//ul[@class="f-hide"]/li/a/text()')
        
        songs = []
        for link, name in zip(song_links, song_names):
            song_id = link.split('=')[-1]
            songs.append({
                'id': song_id,
                'name': name,
                'url': f"https://music.163.com{link}"
            })
        
        return {'songs': songs}
        
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/get-cookies', methods=['GET'])
def get_cookies():
    """获取当前的cookies配置"""
    # 返回可编辑的cookies字段
    editable_cookies = {k: v for k, v in cookies.items() if k != 'os'}  # os必须是pc
    return jsonify({
        'cookies': editable_cookies,
        'fixed_fields': {'os': 'pc'}
    })

@app.route('/api/update-cookies', methods=['POST'])
def update_cookies():
    """更新cookies配置"""
    try:
        data = request.json
        cookie_string = data.get('cookieString', '')
        
        if cookie_string:
            # 解析cookie字符串
            parsed_cookies = parse_cookie_string(cookie_string)
            
            # 更新cookies，但保持os=pc不变
            for key, value in parsed_cookies.items():
                if key != 'os' and value:  # 忽略os字段和空值
                    cookies[key] = value
            
            # 确保os始终是pc
            cookies['os'] = 'pc'
            
            return jsonify({
                'success': True,
                'message': 'Cookies已更新',
                'cookies': {k: v for k, v in cookies.items() if k != 'os'},
                'parsed_count': len(parsed_cookies)
            })
        else:
            return jsonify({'error': '请输入Cookie字符串'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def parse_cookie_string(cookie_string):
    """解析cookie字符串为字典"""
    parsed = {}
    # 分割cookie字符串，支持分号或换行符分隔
    pairs = re.split('[;\\n]', cookie_string)
    
    for pair in pairs:
        pair = pair.strip()
        if '=' in pair:
            key, value = pair.split('=', 1)
            key = key.strip()
            value = value.strip()
            # 只提取我们需要的cookie字段
            if key in default_cookies:
                parsed[key] = value
    
    return parsed

@app.route('/api/reset-cookies', methods=['POST'])
def reset_cookies():
    """重置cookies为默认值"""
    global cookies
    cookies = default_cookies.copy()
    return jsonify({
        'success': True,
        'message': 'Cookies已重置为默认值',
        'cookies': {k: v for k, v in cookies.items() if k != 'os'}
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)