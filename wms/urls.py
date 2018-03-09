"""wms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from rest_framework import routers
from program import views
from django.contrib import admin

from .views import home_page,term_page , logout_page
from accounts.views import validate_email, login_action, register_action
from program.views import (
program_page, order_transaction,add_address_page, save_address, change_user_address, reciever_product, staff_view,
 show_product_from_order,update_order, product_view, manage_user,update_user_company, product_add ,product_add_item_page,
 request_inactive, product_inactive, launch_truck_page,launch_truck,complete_launch)
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'path', views.CarPathViewSet)

urlpatterns = [
    url(r'^$',home_page, name="home" ),
    url(r'^term/',term_page , name="term" ),
    url(r'^molamola/',program_page , name="program_page" ),
    url(r'^login_action/',login_action , name="login_action" ),
    url(r'^save_address/',save_address , name="save_address" ),
    url(r'^ordered/',order_transaction , name="order_transaction" ),
    url(r'^address/',add_address_page , name="add_address_page" ),
    url(r'^reciever/',reciever_product , name="reciever_product" ),
    url(r'^product/',product_view , name="product_view" ),
    url(r'^update_user_company/',update_user_company , name="update_user_company" ),
    url(r'^lauch/',launch_truck_page , name="launch_truck_page" ),
    url(r'^launch_truck/',launch_truck , name="launch_truck" ),
    url(r'^complete_launch/',complete_launch , name="complete_launch" ),
    url(r'^staff/',staff_view , name="staff_view" ),
    url(r'^request_inactive/',request_inactive , name="request_inactive" ),
    url(r'^product_inactive/',product_inactive , name="product_inactive" ),
    url(r'^manage_user/',manage_user , name="manage_user" ),
    url(r'^product_add/',product_add , name="product_add" ),
    url(r'^product_add_item_page/',product_add_item_page , name="product_add_item_page" ),
    url(r'^update_order/',update_order , name="update_order" ),
    url(r'^show_product_from_order/',show_product_from_order , name="show_product_from_order" ),
    url(r'^change_user_address/',change_user_address , name="change_user_address" ),
    url(r'^register_action/',register_action , name="register_action"  ),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/$', logout_page, name='logout'),
    url(r'^validate_email/$', validate_email, name='validate_email'),

    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
