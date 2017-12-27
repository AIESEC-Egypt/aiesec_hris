from django.contrib.contenttypes.fields import (
    GenericForeignKey)
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models

from aiesec_hris.form_builder.models import User


class Comment(models.Model):
    """ Represents an instance of Comment """

    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    comment = models.CharField(max_length=512)
    likes_count = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')


class Like(models.Model):
    """
    Represents an instance of a Like
    belonging to a Comment
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
