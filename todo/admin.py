from django.contrib import admin

from todo.models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'position',
        'completed',
        'text'
    )

    readonly_fields = (
        'id',
        'user',
        'position',
    )

