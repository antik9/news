import json
import os

from json.decoder import JSONDecodeError
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

file_path = os.path.join('news', 'news_data.json')


def add(request):
    with open(file_path, 'r') as file_object:
        try:
            news_data = json.load(file_object)
        except JSONDecodeError:
            news_data = []

    fresh_news = {
        'title': request.POST.get('title'),
        'text': request.POST.get('text'),
        'datetime': datetime.now().strftime('%d.%m.%y %H:%M:%S'),
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

    news_item = news_data[news_id]

    template = loader.get_template('news/detail.html')
    context = {
       'item': news_item
    }
    return HttpResponse(template.render(context, request))


def index(request):
    with open(file_path, 'r') as file_object:
        try:
            news_data = json.load(file_object)
        except JSONDecodeError:
            news_data = []

    template = loader.get_template('news/index.html')

    news_data = [(id, news) for id, news in enumerate(news_data)]
    context = {
        'news': news_data,
    }
    return HttpResponse(template.render(context, request))
