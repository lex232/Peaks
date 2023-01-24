import pandas as pd
# For heightmap
import plotly.express as px
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordChangeView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
# For reset
from django.urls import reverse_lazy
from django.views import View

# from django.http import HttpResponse
# For users
from .forms import RegisterForm, LoginForm
from .forms import UpdateUserForm, UpdateProfileForm
from .models import AboutSummit


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_message = "Пароль успешно изменен"
    success_url = reverse_lazy('home')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "На почту отправили инструкции по сбросу пароля, " \
                      "Если существует учетная запись с введенным вами адресом электронной почты. Вы должны получить ее в ближайшее время." \
                      "Если вы не получали сообщение, " \
                      "Пожалуйста, убедитесь, что вы ввели адрес, с которым вы зарегистрировались, и проверьте папку со спамом."
    success_url = reverse_lazy('summit:home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен')
            # На этом этапе ошибка - исправлено
            return redirect(to='summit:users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html', {'user_form': user_form, 'profile_form': profile_form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')
        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}.')
            return redirect(to='/')
        return render(request, self.template_name, {'form': form})


def home(request):
    title = 'Главная страница'
    highest_summit = AboutSummit.objects.filter(high__lte=9000).order_by('-high')[:8]
    context = {'title': title,
               'highest_summit': highest_summit}
    return render(request, 'home.html', context)


def main(request):
    title = 'Список вершин'
    select_command = request.GET.get('select', None)
    select_pages = request.GET.get('pages_count', 10)
    high_from = request.GET.get('from', 100)
    high_till = request.GET.get('till', 9000)
    if select_command == 'up':
        all_summits = AboutSummit.objects.filter(high__gte=high_from, high__lte=high_till).order_by('-high')
    elif select_command == 'down':
        all_summits = AboutSummit.objects.filter(high__gte=high_from, high__lte=high_till).order_by('high')
    elif select_command == 'name_up':
        all_summits = AboutSummit.objects.filter(high__gte=high_from, high__lte=high_till).order_by('-title')
    elif select_command == 'name_down':
        all_summits = AboutSummit.objects.filter(high__gte=high_from, high__lte=high_till).order_by('title')
    elif select_command == 'country_up':
        all_summits = AboutSummit.objects.filter(high__gte=high_from, high__lte=high_till).order_by('-country')
    elif select_command == 'country_down':
        all_summits = AboutSummit.objects.filter(high__gte=high_from, high__lte=high_till).order_by('country')
    else:
        all_summits = AboutSummit.objects.all()
    paginator = Paginator(all_summits, select_pages)  # Show posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'title': title,
               'high_till': high_till,
               'high_from': high_from,
               'select_command': select_command,
               'select_pages': select_pages,
               'all_summits': all_summits,
               'page_obj': page_obj}
    return render(request, 'summit/main.html', context)


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


def details(request, slug):
    title = 'Информация о ' + slug + ' Высота, расположение, фото'
    all_summits = AboutSummit.objects.get(slug=slug)
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
            if item[0] > int(high_select) and item[0] < int(high_select) + 1000:
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
        width=1200,
        height=500,
        size='Высота'
    )
    fig.update_layout(
        font_size=14,
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
    context = {"plot": fig, "high_select": high_select, "title": title, }
    template = 'heightmap.html'
    return render(request, template, context)
