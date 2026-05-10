from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")

    class Meta:
        verbose_name_plural = "Categories" # Ось це виправить граматику в адмінці

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва рецепта")
    ingredients = models.TextField(verbose_name="Інгредієнти",
                                   help_text="Вкажіть інгредієнти та їхню кількість (кожен з нового рядка)")
    description = models.TextField(verbose_name="Кроки приготування")
    cooking_time = models.PositiveIntegerField(help_text="Час приготування у хвилинах")
    image = models.ImageField(upload_to='recipes/images/', verbose_name="Фото страви")

    # Зв'язки "Один до багатьох"
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')

    # Зв'язки "Багато до багатьох" для лайків і збереженого
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True)
    favorites = models.ManyToManyField(User, related_name='favorite_recipes', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # ОСЬ ЦЬОГО РЯДКА СКОРІШ ЗА ВСЕ НЕ ВИСТАЧАЄ:
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Коментар {self.author} до {self.recipe}"