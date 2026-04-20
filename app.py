from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "🎉 热点聚合项目部署成功！VPS 上运行正常！"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
