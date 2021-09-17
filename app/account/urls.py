from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    # url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', LoginView.as_view(), name='logout'),
    url(r'^$', views.schemas, name='schemas'),
    path('scheme/<int:scheme_id>', views.scheme, name='scheme'),
    path('delete/scheme/<int:scheme_id>', views.delete_scheme, name='delete'),
    path('scheme/<int:scheme_id>', views.scheme, name='scheme'),
    # path('create/scheme/', views.SchemeAndRow.as_view(), name='add_scheme_and_row'),
    # path('create/scheme/row/<str:name>', views.create_scheme_row, name='create_row'),
    url(r'^add/$', views.SchemeAndRow.as_view(), name='add_scheme_and_row'),
    path('data/sets/', views.get_sets, name='sets'),
    path('generete/sets/', views.generate_sets, name='generate_sets'),
]
