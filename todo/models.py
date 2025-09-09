from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import F


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.IntegerField()
    text = models.TextField()
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # increment position of new task
        if not self.pk:
            self.position = Todo.objects.filter(user=self.user).count() + 1

        super().save()

    def reorder(self, new_position: int) -> None:
        with transaction.atomic():
            todos_to_reorder = Todo.objects.filter(position__gte=new_position)
            todos_to_reorder.update(position=F('position') + 1)

            self.position = new_position
            self.save(update_fields='position')

    def complete(self) -> None:
        pass