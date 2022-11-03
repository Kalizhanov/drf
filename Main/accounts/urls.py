from .views import BasketAPI, ItemAPI, LoginAPI, RegisterAPI, Purchase, BestSelling, Popular, SingleItem
from django.urls import path
from knox import views as knox_views
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/basket/', BasketAPI.as_view(), name='basket'),
    path('api/items/', ItemAPI.as_view(), name='item'),
    path("", SingleItem.as_view()),
    path('api/items/bestselling', BestSelling.as_view()),
    path('api/items/popular', Popular.as_view()),
    path('api/basket/purchase/', Purchase.as_view())
]


urlpatterns += doc_urls