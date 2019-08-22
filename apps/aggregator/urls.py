from django.contrib.auth.views import LogoutView
from django.urls import path
from rest_framework.routers import SimpleRouter
from apps.aggregator import views


router = SimpleRouter()
router.register(r'api/user-token', views.UserTokenView, base_name='api-user-token')


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('docs/<str:code>/', views.SystemDocumentation.as_view(), name='system-docs'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register-client/', views.RegisterClientView.as_view(), name='register-client'),
    path('get-token/', views.GetToken.as_view(), name='get-token'),
]

urlpatterns += router.urls
