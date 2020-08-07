from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^screens/$',views.Screens.as_view()),
    url(r'^screens/(?P<screen_name>\w+)/reserve/$',views.Reserve.as_view()),
    url(r'^screens/(?P<screen_name>\w+)/seats$',views.ShowSeats.as_view())
]