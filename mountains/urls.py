"""mountains URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from filebrowser.sites import site

from summit import views
from summit.forms import LoginForm
from summit.views import ResetPasswordView, ChangePasswordView, CustomLoginView


handler404 = 'core.views.page_not_found'
handler403 = 'core.views.csrf_failure'

urlpatterns = [
                  path('admin/filebrowser/', site.urls),
                  path('grappelli/', include('grappelli.urls')),
                  path('admin/', admin.site.urls),
                  path('', views.home, name='home'),
                  path('summit/', include('summit.urls')),  # Приложение вершин гор
                  path('heightmap/<int:high_select>', views.heightmap, name='heightmap'),  # Карта высот
                  path('tinymce/', include('tinymce.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Авторизация
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

]
