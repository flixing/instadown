from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

header = {"User-Agent":"instadown", "e-mail":"contato@contato.com"}
_regex = r'("https:(.*?).2")'


def get_pic(url):
    r = requests.get(url, headers=header)
    if r.status_code == 200:
        sopa = BeautifulSoup(r.content)
        for meta in sopa.findAll("meta"):
            if meta.get("property") == "og:image" and meta.get("content") != None:
                return meta.get("content")


@app.route('/', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        _url = request.form['url']
        _url_pic = get_pic(_url)
        return render_template('home.html', url_dow=_url_pic)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
