from django.urls import path

from . import views
from .views import (
    LoginView,
    admin_settings_view,
    city_create_view,
    city_detail_view,
    city_list_view,
    coupon_create_view,
    coupon_detail_view,
    coupon_list_view,
    dashboard_view,
    index_view,
    logout_view,
    message_list_view,
    order_detail_driver_view,
    orders_list_admin_view,
    orders_view,
    user_detail_view,
    users_list_view,
    telegram_auth_token_login,
    coupon_list_driver_view,
    apply_coupon_view,
)


from referral import views as referral_views

app_name = "cabinet"


urlpatterns = [
    # Driver
    path("", index_view, name="index"),
    path("orders/", orders_view, name="orders"),
    path("orders/<int:pk>/", order_detail_driver_view, name="order"),
    path("coupons/", coupon_list_driver_view, name="coupon_list_driver"),
    path("coupons/apply_coupon/<int:pk>", apply_coupon_view, name="apply_coupon"),
    path("admin/orders/", orders_list_admin_view, name="order_list_admin"),
    path("admin/users/", users_list_view, name="users"),
    path("admin/users/<int:pk>/", user_detail_view, name="user"),
    path("admin/coupons/", coupon_list_view, name="coupon_list_admin"),
    path("admin/coupons/<int:pk>/", coupon_detail_view, name="coupon_detail"),
    path("admin/coupons/create/", coupon_create_view, name="coupon_create"),
    path("admin/cities/", city_list_view, name="city_list"),
    path("admin/cities/<int:pk>/", city_detail_view, name="city_detail"),
    path("admin/cities/create/", city_create_view, name="city_create"),
    path("admin/messages/", message_list_view, name="message_list"),
    path("admin/messages/create/", views.message_create_view, name="message_create"),
    path("admin/messages/<int:pk>/", views.message_detail_view, name="message_detail"),
    path("admin/mailings/", views.mailing_list_view, name="mailing_list"),
    path("admin/mailings/create/", views.mailing_create_view, name="mailing_create"),
    path("admin/mailings/<int:pk>/", views.mailing_detail_view, name="mailing_detail"),
    path("admin/raffles/", views.raffle_list_view, name="raffle_list"),
    path("admin/raffles/create/", views.raffle_create_view, name="raffle_create"),
    path("admin/raffles/<int:pk>/", views.raffle_detail_view, name="raffle_detail"),
    path("admin/presents/", referral_views.present_list_view, name="present_list_view"),
    path(
        "admin/presents/create/",
        referral_views.present_create_view,
        name="present_create_view",
    ),
    path(
        "admin/presents/<int:pk>/",
        referral_views.present_detail_view,
        name="present_detail_view",
    ),
    # Admin
    path("admin/dashboard/", dashboard_view, name="dashboard"),
    path("admin/settings/", admin_settings_view, name="settings_admin"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "telegram_auth_token_login/<str:token>/",
        telegram_auth_token_login,
        name="telegram_auth_token_login",
    ),
    path("logout/", logout_view, name="logout"),
]
