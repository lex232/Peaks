from django.shortcuts import render, redirect
from django.urls import reverse
from .models import AboutSummit
import plotly.express as px
import numpy as np
import pandas as pd
from django.http import HttpResponse
#next_link = ''


def home(request):
    title = 'Главная страница'
    context = {'title': title}
    return render(request, 'home.html', context)


def main(request):
    title = 'Список вершин'
    all_summits = AboutSummit.objects.all()
    context = {'title': title,
               'all_summits': all_summits}
    return render(request, 'summit/main.html', context)


def user_info(request):
    if request.method == 'GET':
        print('\n\nrequest.GET ==>>',
              request.GET,
              '\n\n')

        if request.session.get('username', False):
            userinfo = {
                'username': request.session['username'],
                'country': request.session['country'],
            }
        else:
            userinfo = False
        context = {'userinfo': userinfo,
                   'title': 'User Info Page'}
        template = 'summit/user_info.html'
        return render(request,
                      template,
                      context)


def user_form(request):
    if request.method == 'GET':
        context = {'title': 'User Form Page'}
        template = 'summit/user_form.html'

        return render(request,
                      template,
                      context)

    elif request.method == 'POST':
        username = request.POST.get('username')
        country = request.POST.get('country')
        request.session['username'] = username
        request.session['country'] = country

        return redirect(reverse('summit:user_info'))


def details(request, id):
    title = 'Details'
    all_summits = AboutSummit.objects.get(id=id)
    context = {'title': title,
               'all_summits': all_summits}
    return render(request, 'summit/details.html', context)

def get_data(high_select):
    title_data = []
    high_data = []
    if high_select == 9000:
        new_test_data = sorted(list(AboutSummit.objects.all().values_list('high', 'title')))
        for item in new_test_data:
            high_data.append(item[0])
        for item in new_test_data:
            title_data.append(item[1])
    elif high_select == 9001:
        new_test_data = sorted(list(AboutSummit.objects.all().values_list('high', 'title')), reverse=True)
        for item in new_test_data:
            high_data.append(item[0])
        for item in new_test_data:
            title_data.append(item[1])
    elif high_select == 8000:
        new_test_data = sorted(list(AboutSummit.objects.all().values_list('high', 'title')))
        print(new_test_data)
        for item in new_test_data:
            if item[0] > 8000:
                high_data.append(item[0])
                title_data.append(item[1])
    else:
        new_test_data = sorted(list(AboutSummit.objects.all().values_list('high', 'title')))
        print(high_select)
        for item in new_test_data:
            if item[0] > int(high_select) and item[0] < int(high_select)+1000:
                high_data.append(item[0])
                title_data.append(item[1])
    df = pd.DataFrame({
    'Название': title_data,
    'Высота': high_data,
    })
    return df

def create_plot(df, high_select):
    fig = px.scatter(
        data_frame=df,
        x='Название',
        y='Высота',
        width = 1200,
        height = 500,
        size='Высота'
    )
    fig.update_layout(
        font_size = 14,
        font_family="PT sans",
        font_color="black",
        title_font_family="PT sans",
        title_font_color="red",
        legend_title_font_color="green"
    )
    fig = fig.to_html()
    return fig

def heightmap(request, high_select):
    title = 'Карта высот'
    df = get_data(high_select)
    fig = create_plot(df, high_select)
    context = {"plot": fig, "high_select": high_select, "title": title,}
    template = 'heightmap.html'
    return render(request, template, context)