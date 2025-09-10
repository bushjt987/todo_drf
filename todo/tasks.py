from django.conf import settings
from django.core.mail import send_mail

from config.celery import app


@app.task()
def send_todo_completed_email(todo_id: int) -> None:
    from todo.models import Todo

    todo = Todo.objects.filter(id=todo_id).select_related('user').first()

    send_mail(
        subject=f'Todo Completed: {todo.text}',
        message=f'The following todo item was marked as complete: "{todo.text}"',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(todo.user.email,),
    )