from django.db import models

# Create your models here.
from embed_video.fields import EmbedVideoField
from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager

COURSE_BY_CHOICES = (
    ('AI', 'AIESEC International'),
    ('RO', 'Regional Office'),
    ('MC', 'National Office'),
    ('LC', 'Local Office'),
    ('GFB', 'Global Finance Board'),
    ('GEB', 'Global Expansions Board'),
    ('ICB', 'Internal Control Board')
)


class Course(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    course_by = MultiSelectField(choices=COURSE_BY_CHOICES, max_choices=3)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    next = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=128)
    video = EmbedVideoField(null=True, blank=True)
    subtitle = models.CharField(max_length=300, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True)
    next = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
