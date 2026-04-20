cat > app.py << 'EOF'
from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 带错误处理的知乎热榜
def get_zhihu_hot():
    try:
        url = "https://www.zhihu.com/hot"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".HotList-item")[:10]
        return [{"title": i.select_one(".HotList-itemTitle").text, "url": "https://www.zhihu.com" + i.a["href"]} for i in items]
    except Exception as e:
        print(f"获取知乎热榜失败: {e}")
        return [{"title": "当前网络环境受限，暂时无法获取热榜", "url": "#"}]

@app.route('/')
def index():
    zhihu = get_zhihu_hot()
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>全网热点聚合平台</title>
        <style>
            body { font-family: Arial; max-width: 1000px; margin: 0 auto; padding: 20px; background: #f5f7fa; }
            h1 { color: #333; text-align: center; }
            .card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin-top:20px; }
            .card h2 { color: #2c3e50; }
            ul { padding: 0; list-style: none; }
            li { margin: 10px 0; font-size: 16px; }
            a { color: #2d7ff9; text-decoration: none; }
        </style>
    </head>
    <body>
        <h1>📰 全网热点聚合平台</h1>
        <div class="card">
            <h2>💬 知乎热榜</h2>
            <ul>
                {% for item in zhihu %}
                <li><a href="{{item.url}}" target="_blank">{{item.title}}</a></li>
                {% endfor %}
            </ul>
        </div>
    </body>
    </html>
    ''', zhihu=zhihu)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
