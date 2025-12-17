from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home, register, book, payment_checkout

urlpatterns = [
    path("", home, name="home"),
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("book/", book, name="book"),
    path("payment/<str:reference>/", payment_checkout, name="payment_checkout"),
]
