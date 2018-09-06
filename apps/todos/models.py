from django.db import models

import positions

class Todo(models.Model):
    title = models.CharField(max_length=80, null=False)
    content = models.TextField(null=True)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    index = positions.PositionField(default=-1)
    objects = positions.PositionManager('index')

    def __str__(self):
        """A string representation of the model."""
        return self.title

    def __repr__(self):
            return str(self.to_dict())

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, models.fields.related.ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))

            elif isinstance(f, models.DateTimeField):
                if f.value_from_object(self) is not None:
                    data[f.name] = str(f.value_from_object(self))
                else:
                    data[f.name] = None
            else:
                data[f.name] = f.value_from_object(self)
        return data
