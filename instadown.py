import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

header = {"User-Agent":"instadown", "e-mail":"contato@contato.com"}


def get_data(url):
    r = requests.get(url, headers=header)
    _url_video = ''
    if r.status_code == 200:
        sopa = BeautifulSoup(r.content)
        for meta in sopa.findAll("meta"):
            if meta.get("property") == "og:title" and meta.get("content") != None:
                _content_title = meta.get("content")
            if meta.get("property") == "og:video" and meta.get("content") != None:
                _url_video = meta.get("content")
            elif meta.get("property") == "og:image" and meta.get("content") != None:
                _url_image = meta.get("content")
        if _url_video == '':
            return dict(title=_content_title, image=_url_image)
        else:
            return dict(title=_content_title, video=_url_video)
    
    return None


@app.route('/', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        _url = request.form['url']
        data = get_data(_url)
        print data
        return render_template('home.html', content_dow=data)
    return render_template('home.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
