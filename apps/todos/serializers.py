from rest_framework import serializers, exceptions

from django.conf import settings

from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'index',
            'title',
            'content',
            'is_done',
            'updated_at',
            'created_at',
        )
        model = Todo

    def create(self, validated_data):
        if Todo.objects.count() >= settings.LIMITED_TODO_COUNT:
            raise exceptions.NotAcceptable(
                    detail="The maximum number of todo has been exceeded. Please remove the other todos")
        todo = Todo.objects.create(**validated_data)
        return todo
