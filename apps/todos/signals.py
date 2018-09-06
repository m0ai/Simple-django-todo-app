import json

from django.core import serializers
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from .models import Todo

@receiver(post_delete, sender=Todo)
def announce_todo_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    data = instance.to_dict()
    data['type'] = 'notify_delete'
    async_to_sync(channel_layer.group_send)(
        'todos_app', data
    )

@receiver(post_save, sender=Todo)
def announce_todo_update_or_create(sender, instance, created, **kwargs):
    updated = not created
    if created or updated:
        channel_layer = get_channel_layer()
        data = instance.to_dict()
        data['type'] = 'update_or_create'
        async_to_sync(channel_layer.group_send)(
            'todos_app', data
        )



