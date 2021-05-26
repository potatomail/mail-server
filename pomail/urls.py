from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from .settings import STATIC_URL, STATIC_ROOT

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("accounts/login", views.login_view, name="login"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('send/', views.send, name="send"),
    path('send_mail_plain', views.SendPlainEmail, name='plain_email'),
    path('send_mail_plain_with_stored_file', views.send_mail_plain_with_stored_file, name='plain_email'),
    path('send_mail_plain_with_file', views.send_mail_plain_with_file, name='plain_email'),
    path('receive_list/', views.receive_list, name="receive_list"),
    path('send_list/', views.send_list, name="send_list"),
    path('read_mail/', views.read_mail, name="read_mail"),
    path('receive_list/<int:cur_page>', views.receive_list, name="receive_list"),
    path('send_list/<int:cur_page>', views.send_list, name="send_list"),
    path('read_mail/<int:mail_id>', views.read_mail, name="read_mail"),
]
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

