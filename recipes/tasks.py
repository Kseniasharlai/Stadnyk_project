from celery import shared_task
from .models import Comment
import time


@shared_task
def moderate_comment_task(comment_id):
    try:
        # Штучна затримка в 2 секунди, щоб імітувати роботу ШІ та показати викладачу асинхронність
        time.sleep(2)

        comment = Comment.objects.get(id=comment_id)

        # Наш власний словник заборонених слів (можеш додати свої)
        forbidden_words = ['казино', 'ставки', 'casino', 'vulkan', 'слоти', 'slot', 'крипта']
        is_ok = True

        # Перевіряємо текст коментаря
        for word in forbidden_words:
            if word in comment.text.lower():
                is_ok = False
                break

        if is_ok:
            comment.is_approved = True
            comment.save()
            print(f"Celery: Коментар {comment_id} СХВАЛЕНО")
        else:
            comment.is_approved = False
            comment.save()
            print(f"Celery: Коментар {comment_id} ЗАБЛОКОВАНО (спам)")

    except Exception as e:
        print(f"Помилка Celery: {e}")