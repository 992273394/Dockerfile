from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 知乎热点
def get_zhihu_hot():
    url = "https://www.zhihu.com/hot"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".HotList-item")[:10]
    return [{"title": i.select_one(".HotList-itemTitle").text, "url": "https://www.zhihu.com" + i.a["href"]} for i in items]

# B站热点
def get_bilibili_hot():
    url = "https://api.bilibili.com/x/web-interface/popular/precious?ps=10"
    res = requests.get(url).json()
    return [{"title": i["title"], "url": f"https://www.bilibili.com/video/{i['bvid']}"} for i in res["data"]["list"]]

# 微博热点
def get_weibo_hot():
    url = "https://s.weibo.com/top/summary"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".td-02 a")[:10]
    return [{"title": i.text, "url": "https://s.weibo.com" + i["href"]} for i in items]

@app.route('/')
def index():
    zhihu = get_zhihu_hot()
    bilibili = get_bilibili_hot()
    weibo = get_weibo_hot()
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>全网热点聚合</title>
        <style>
            body { font-family: Arial; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f7fa; }
            h1 { color: #333; text-align: center; }
            .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px; }
            .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }
            .card h2 { color: #2c3e50; margin-top: 0; }
            ul { list-style: none; padding: 0; }
            li { margin: 12px 0; }
            a { color: #3498db; text-decoration: none; }
            a:hover { color: #2980b9; text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>📰 全网热点聚合平台</h1>
        <div class="grid">
            <div class="card">
                <h2>💬 知乎热榜</h2>
                <ul>{% for item in zhihu %}<li><a href="{{item.url}}" target="_blank">{{item.title}}</a></li>{% endfor %}</ul>
            </div>
            <div class="card">
                <h2>📺 B站热门</h2>
                <ul>{% for item in bilibili %}<li><a href="{{item.url}}" target="_blank">{{item.title}}</a></li>{% endfor %}</ul>
            </div>
            <div class="card">
                <h2>📱 微博热搜</h2>
                <ul>{% for item in weibo %}<li><a href="{{item.url}}" target="_blank">{{item.title}}</a></li>{% endfor %}</ul>
            </div>
        </div>
    </body>
    </html>
    ''', zhihu=zhihu, bilibili=bilibili, weibo=weibo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
