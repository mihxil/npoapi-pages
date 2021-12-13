import os

import json
from datetime import time, datetime

from flask import Flask, render_template, send_from_directory, request
from npoapi import Pages
from npoapi.data.api import PagesForm, PagesSearchType, TextMatcherListType, TextMatcherType, PageSortType, \
    PageSortTypeEnum, OrderTypeEnum

app = Flask(__name__)

client = Pages(interactive=False,
               debug=os.getenv("debug", default=False)
               ).configured_login(config_dir=os.getenv("configdir"), default_config_dirs=True)
client.env("prod")
profile=os.getenv("profile")

@app.route('/')
def index():
    profArg = request.args.get('profile')
    if "" == profArg:
        prof = None
    else:
        prof = profArg  or profile
    form = PagesForm()
    form.sort_fields = [PageSortType()]
    form.sort_fields[0].value = PageSortTypeEnum.SORT_DATE
    form.sort_fields[0].order = OrderTypeEnum.DESC
    form.searches = PagesSearchType()
    form.searches.types = TextMatcherListType()
    matcher = TextMatcherType()
    matcher.value = "HOME"
    form.searches.types.matcher = [matcher]
    pages = []

    for item in client.iterate(profile = prof, form=form, limit=2000):
        pages.append(item)
    result = {'total': len(pages)}

    return render_template('index.html',  pages=pages, result=result, profile=prof)


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


@app.template_filter('formattime')
def formattime(s):
    return  datetime.utcfromtimestamp(s / 1000).strftime('%Y-%m-%d')

@app.after_request
def add_header(response):
    response.cache_control.max_age = 600
    return response

if __name__ == "__main__":
    from waitress import serve
    import logging
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.DEBUG)
    serve(app, host="0.0.0.0", port=8080)