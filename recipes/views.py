from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Recipe, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import CommentForm
from .tasks import moderate_comment_task
from django.conf import settings
from .forms import CommentForm , RecipeForm


def recipe_list(request):
    query = request.GET.get('q')  # Отримуємо текст з рядка пошуку

    if query:
        # Шукаємо збіги в назві АБО в інгредієнтах (icontains - пошук без врахування регістру)
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | Q(ingredients__icontains=query)
        ).order_by('-created_at')
    else:
        # Якщо пошуку немає - показуємо всі
        recipes = Recipe.objects.all().order_by('-created_at')

    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'query': query})


import requests
import json


def recipe_detail(request, pk):
    # Отримуємо рецепт або 404, якщо його не існує
    recipe = get_object_or_404(Recipe, pk=pk)

    # Виводимо тільки ті коментарі, які пройшли перевірку (is_approved=True)
    comments = recipe.comments.filter(status='approved').order_by('-created_at')
    if request.method == 'POST':
        # Перевіряємо, чи залогінений користувач
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            # Створюємо об'єкт коментаря, але не зберігаємо в базу відразу
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user

            # ВАЖЛИВО: Ставимо False, щоб коментар не з'явився на сайті до перевірки ШІ
            comment.is_approved = False

            # Зберігаємо в базу (тепер ти БАЧИШ його в адмінці відразу)
            comment.save()

            # ВІДПРАВЛЯЄМО ЗАДАЧУ В CELERY
            # Передаємо ID коментаря, щоб фоновий процес знайшов його і перевірив через Gemini
            moderate_comment_task.delay(comment.id)

            # Перенаправляємо користувача назад на сторінку рецепта
            return redirect('recipes:recipe_detail', pk=pk)
    else:
        # Якщо це GET запит - просто створюємо порожню форму
        form = CommentForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'form': form
    })
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Одразу авторизуємо після реєстрації
            return redirect('recipes:recipe_list')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})
@login_required # Цей декоратор не пустить сюди неавторизованих
def like_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    # Якщо користувач вже ставив лайк - забираємо його, якщо ні - додаємо
    if request.user in recipe.likes.all():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return redirect('recipes:recipe_detail', pk=pk)

@login_required
def favorite_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user in recipe.favorites.all():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)
    return redirect('recipes:recipe_detail', pk=pk)

@login_required
def favorites_list(request):
    # Вибираємо рецепти, у яких в полі favorites є наш користувач
    favorite_recipes = Recipe.objects.filter(favorites=request.user).order_by('-created_at')
    return render(request, 'recipes/favorites.html', {'recipes': favorite_recipes})

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES) # request.FILES обов'язково для фото!
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user # Автоматично ставимо автора
            recipe.save()
            return redirect('recipes:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})