from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_hot():
    try:
        url = "https://github.com/trending"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("article.Box-row")[:10]

        return [{
            "title": i.h2.text.strip().replace("\n", "").replace(" ", ""),
            "url": "https://github.com" + i.h2.a["href"]
        } for i in items]

    except Exception as e:
        return [{"title": f"获取失败: {e}", "url": "#"}]

@app.route('/')
def index():
    data = get_hot()
    return render_template_string('''
    <h1>🔥 GitHub 热榜</h1>
    <ul>
    {% for item in data %}
        <li><a href="{{item.url}}">{{item.title}}</a></li>
    {% endfor %}
    </ul>
    ''', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
