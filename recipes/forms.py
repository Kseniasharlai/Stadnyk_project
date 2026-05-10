from django import forms
from .models import Comment, Recipe

# Твоя стара форма для коментарів
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Напишіть коментар...'}),
        }

# НОВА форма для додавання рецепта (перевір, чи вона тут є!)
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        # Змінили 'instructions' на 'description'
        fields = ['title', 'category', 'cooking_time', 'ingredients', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва страви'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Хвилин'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Перерахуйте інгредієнти...'}),
            # Тут також змінили назву ключа на 'description'
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Кроки приготування...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }