from rest_framework import serializers

from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'


class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'text', 'position')
        read_only_fields = ['id', 'position']


class TodoCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'completed',)
        read_only_fields = ['id']


class TodoReorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'position',)
        read_only_fields = ['id']
