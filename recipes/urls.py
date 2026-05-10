from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('register/', views.register, name='register'),
    # ДВА НОВИХ РЯДКИ:
    path('recipe/<int:pk>/like/', views.like_recipe, name='like_recipe'),
    path('recipe/<int:pk>/favorite/', views.favorite_recipe, name='favorite_recipe'),
path('favorites/', views.favorites_list, name='favorites_list'), # НОВИЙ РЯДОК
path('recipe/new/', views.recipe_create, name='recipe_create'),
]