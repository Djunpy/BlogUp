from django.urls import path,include
from .views import (IndexPage, ByCategory, SinglePage, ByTag,
                    Search, Login, Signup, Logout)


urlpatterns = [
    path('', IndexPage.as_view(), name='index_url'),
    path('post/<str:slug>/<int:pk>/', SinglePage.as_view(), name='single_url'),
    path('category/<str:slug>/', ByCategory.as_view(), name='category_url'),
    path('tag/<str:slug>/', ByTag.as_view(), name='tag_url'),
    path('search/', Search.as_view(), name='search_url'),
    path('account/login/', Login.as_view(), name='login_url'),
    path('account/signup/', Signup.as_view(), name='register_url'),
    path('account/logout/', Logout.as_view(), name='logout_url'),

]