import re

from django.db import models
from django.urls import reverse

from aiesec_hris.users.models import User


class Category(models.Model):
    """
    Model representing a category for models.Post
    Author: Nader Alexan
    """
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-title']


class Post(models.Model):
    """
    Model representing a newsfeed post
    Author: Nader Alexan
    """
    category = models.ManyToManyField(Category)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def has_video(self):
        return self.paragraph.exclude(youtube_url=None).exists()

    @property
    def has_document(self):
        return self.paragraph.exclude(document='').exists()

    @property
    def has_photo(self):
        return self.paragraph.exclude(photo='').exists()

    @property
    def first_photo(self):
        if self.has_photo:
            return self.paragraph.exclude(photo='')[0].photo
        return None

    @property
    def first_video(self):
        if self.has_video:
            return self.paragraph.exclude(youtube_url=None)[0]
        return None

    @property
    def teaser(self):
        paragraphs = self.paragraph.exclude(text=None)
        if paragraphs:
            return paragraphs.first().text
        return '...'

    class Meta:
        ordering = ['-created_at']


class Paragraph(models.Model):
    """
    Model reperesenting a post paragraph
    Author: Nader Alexan
    """
    post = models.ForeignKey(Post, related_name='paragraph', on_delete=models.CASCADE)

    photo = models.ImageField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    document = models.FileField(
        upload_to='post_documents/', null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return '%s: %s' % (self.post.title, self.text)

    @property
    def youtube_id(self):
        pattern = r'((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)'
        return re.search(pattern, self.youtube_url).group(0)

    class Meta:
        ordering = ['order']
