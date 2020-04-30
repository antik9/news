import json
import os
import random

from json.decoder import JSONDecodeError
from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect
from django.template import loader

file_path = os.path.join('news', 'news_data.json')

DT_TEMPLATE = '%Y/%m/%d %H:%M:%S'


def main(request, *args, **kwargs):
    return HttpResponseRedirect('/news')


def add(request):
    with open(file_path, 'r') as file_object:
        try:
            news_data = json.load(file_object)
        except JSONDecodeError:
            news_data = []

    fresh_news = {
        'title': request.POST.get('title'),
        'text': request.POST.get('text'),
        'created_at': datetime.now().strftime(DT_TEMPLATE),
        'link': random.randint(1, 1_000_000),
    }
    news_data.append(fresh_news)

    with open(file_path, 'w') as file_object:
        json.dump(news_data, file_object)

    return redirect('index')


def adding_page(request):
    template = loader.get_template('news/adding_page.html')

    return HttpResponse(template.render({}, request))


def detail(request, news_id):
    with open(file_path, 'r') as file_object:
        news_data = json.load(file_object)

    for news_item in news_data:
        if news_id == int(news_item['link']):
            template = loader.get_template('news/detail.html')
            context = {
               'item': news_item
            }
            return HttpResponse(template.render(context, request))
    raise Http404


def index(request):
    with open(file_path, 'r') as file_object:
        try:
            news_data = json.load(file_object)
        except JSONDecodeError:
            news_data = []

    q = request.GET.get('q', '')
    template = loader.get_template('news/index.html')

    news = {}
    for item in news_data:
        if q not in item['title'].lower():
            continue
        d = datetime.strptime(item['created_at'], DT_TEMPLATE).date().strftime(DT_TEMPLATE[:8])
        if d not in news:
            news[d] = []
        news[d].append(item)
        for value in news.values():
            value.sort(key=lambda k: k['created_at'], reverse=True)

    context = {'news': news}
    return HttpResponse(template.render(context, request))
