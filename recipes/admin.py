from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Recipe, Comment

admin.site.register(Category)
admin.site.register(Recipe)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Відображаємо тільки ті поля, які точно є в моделі
    list_display = ('text', 'author', 'recipe', 'colored_status', 'created_at')

    def colored_status(self, obj):
        # Перевіряємо саме поле status
        if obj.status == 'approved':
            color = 'green'
        elif obj.status == 'rejected':
            color = 'red'
        else:
            color = 'orange'
        return format_html('<b style="color: {};">{}</b>', color, obj.status)

    colored_status.short_description = 'Status'