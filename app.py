import os

import json

from flask import Flask, render_template, send_from_directory, request
from npoapi import Pages
from npoapi.data.api import PagesForm, PagesSearchType, TextMatcherListType, TextMatcherType

app = Flask(__name__)

client = Pages(interactive=False,
               debug=os.getenv("debug", default=False)
               ).configured_login(config_dir=os.getenv("configdir"), default_config_dirs=True)
client.env("prod")
profile=os.getenv("profile")

@app.route('/')
def index():
    prof = request.args.get('profile') or profile
    form = PagesForm()
    form.searches = PagesSearchType()
    form.searches.types = TextMatcherListType()
    matcher = TextMatcherType()
    matcher.value = "HOME"
    form.searches.types.matcher = [matcher]
    result = client.search(profile = prof, form=form)
    j = json.JSONDecoder().decode(result)
    pages = list(map(lambda i: i['result'], j["items"]))
    return render_template('index.html',  pages=pages)


@app.route('/page/<path:url>')
def page(url:str):
    result = client.get(url)
    j = json.JSONDecoder().decode(result)
    item = j['items'][0]
    if "result" in item:
        page = item['result']
    else:
        page = None

    return render_template('page.html',  page=page)


@app.route('/css/<path:path>')
def send_js(path):
    return send_from_directory('css', path)


