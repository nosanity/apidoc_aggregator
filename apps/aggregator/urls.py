from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('docs/<str:code>/', views.SystemDocumentation.as_view(), name='system-docs'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
