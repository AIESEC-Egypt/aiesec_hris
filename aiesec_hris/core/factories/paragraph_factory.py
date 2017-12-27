import factory
import factory.fuzzy

from ..models import Paragraph, Post


class ParagraphFactory(factory.DjangoModelFactory):
    class Meta:
        model = Paragraph

    post = factory.Iterator(Post.objects.all())
    youtube_url = 'https://www.youtube.com/embed/p9Urng_hGF8'
    document = factory.django.ImageField(color='blue')
    photo = factory.django.ImageField(color='blue')
    text = factory.Faker('text')
