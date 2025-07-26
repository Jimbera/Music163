# 网易云音乐下载器 Web版

一个基于Web的网易云音乐下载工具，支持歌单和单曲下载，具有现代化的用户界面。

## 功能特点

- 🎵 支持歌单批量下载
- 🎶 支持单曲下载
- 🎨 支持混合输入（歌单和单曲链接混合）
- 🌓 深色/浅色主题切换
- 📱 响应式设计
- 📊 下载历史记录
- 🎚️ 多种音质选择（标准、极高、无损、Hi-Res等）
- ⚡ 实时下载进度显示
- 🔧 Cookie设置管理（支持自定义网易云Cookie）

## 安装步骤

1. 克隆或下载项目到本地

2. 安装Python依赖：
```bash
pip install -r requirements.txt
```

## 运行方法

1. 启动后端服务器：
```bash
python app.py
```
服务器将在 http://localhost:5000 启动

2. 在浏览器中打开 `index.html` 文件，或使用任何静态文件服务器托管

## 使用说明

1. **输入链接**：
   - 在输入框中粘贴网易云音乐的歌单或单曲分享链接
   - 支持多行输入，每行一个链接
   - 支持歌单和单曲链接混合输入

2. **选择音质**：
   - 从下拉菜单中选择所需的音质
   - 可选：标准、极高、无损、高解析度无损等

3. **开始处理**：
   - 点击"开始处理"按钮
   - 系统会自动识别链接类型并处理

4. **下载音乐**：
   - 处理完成后，点击每首歌曲旁的"保存"按钮下载
   - 下载的歌曲会自动添加到历史记录

5. **历史记录**：
   - 查看所有下载历史
   - 可以删除单个记录或清空所有历史

6. **Cookie设置**：
   - 点击右上角的设置按钮
   - 可以自定义网易云音乐的Cookie信息
   - 支持重置为默认Cookie
   - os字段固定为"pc"，不可修改

## 技术栈

- **前端**：HTML5, CSS3, JavaScript (原生)
- **后端**：Python Flask
- **API**：网易云音乐Web API

## 注意事项

- 请确保网络连接正常
- 某些歌曲可能因版权限制无法下载
- 建议合理使用，避免频繁请求

## 项目结构

```
Music163/
├── index.html          # 前端页面
├── app.py             # Flask后端服务
├── main.py            # 原始命令行版本
├── requirements.txt   # Python依赖
└── README.md         # 项目说明
```

## 开发说明

- 前端使用原生JavaScript，无需构建工具
- 支持现代浏览器（Chrome, Firefox, Safari, Edge）
- 后端API使用RESTful风格设计
- 支持CORS跨域请求

## License

仅供学习交流使用，请勿用于商业用途。

# 📊 GitHub Stats

![Alt](https://repobeats.axiom.co/api/embed/dac734b79288e09bc9a85b5f27be742548700127.svg "Repobeats analytics image")

## Star History

<a href="https://www.star-history.com/#Jimbera/Music163&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Jimbera/Music163&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Jimbera/Music163&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Jimbera/Music163&type=Date" />
 </picture>
</a>
