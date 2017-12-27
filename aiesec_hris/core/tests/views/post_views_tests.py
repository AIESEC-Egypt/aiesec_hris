from django.test import TestCase
from django.urls import reverse

from ...factories import (
    UserFactory,
    PostFactory,
    CategoryFactory,
    ParagraphFactory,
    ProfileFactory,
    PositionFactory)
from ...models import Post, Category
from ..helpers import compare_lists


class PostViewsTests(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.password = 'password'
        self.user.set_password(self.password)
        self.user.save()
        position = PositionFactory(type=1)
        ProfileFactory(user=self.user, position=position)
        self.client.login(username=self.user.username, password=self.password)

        CategoryFactory.create_batch(5)
        PostFactory.create_batch(25)

    def test_post_list_render(self):
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            compare_lists(
                response.context.get('object_list'),
                Post.objects.all()[:10],
                'id'))
        self.assertTrue(
            compare_lists(
                response.context.get('category_list'),
                Category.objects.all(),
                'id'))

    def test_post_detail(self):
        post = PostFactory()
        response = self.client.get(
            reverse('post-detail', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        title = 'hello world'
        data = {
            'category': Category.objects.first().id,
            'title': title,
            'paragraph-0-text': 'lorem impsum',
            'paragraph-1-text': 'lorem impsum 2',
            'paragraph-MIN_NUM_FORMS': '0',
            'paragraph-INITIAL_FORMS': '0',
            'paragraph-TOTAL_FORMS': '2',
            'paragraph-MAX_NUM_FORMS': '1000',

        }
        response = self.client.post(reverse('post-create'), data=data)
        self.assertEqual(response.status_code, 201)
        post = Post.objects.get(title=title)
        self.assertEqual(post.paragraph.count(), 2)

    def test_post_create_unsuccessful(self):
        title = 'hello world'
        data = {
            'title': title,
            'paragraph-0-text': 'lorem impsum',
            'paragraph-1-text': 'lorem impsum 2',
            'paragraph-MIN_NUM_FORMS': '0',
            'paragraph-INITIAL_FORMS': '0',
            'paragraph-TOTAL_FORMS': '2',
            'paragraph-MAX_NUM_FORMS': '1000',

        }
        response = self.client.post(reverse('post-create'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_update_render(self):
        post = Post.objects.first()
        response = self.client.get(
            reverse('post-update', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context.get('post_form'))
        self.assertTrue(response.context.get('paragraph_formset'))

    def test_post_update(self):
        paragraph = ParagraphFactory()
        post = paragraph.post
        data = {
            'category': post.category.all().values_list('pk', flat=True),
            'id': post.id,
            'title': 'new title',
            'paragraph-0-text': 'new text',
            'paragraph-0-youtube_url': paragraph.youtube_url,
            'paragraph-0-document': paragraph.document,
            'paragraph-0-photo': paragraph.photo,
            'paragraph-0-id': paragraph.id,
            'paragraph-MIN_NUM_FORMS': '0',
            'paragraph-INITIAL_FORMS': '0',
            'paragraph-TOTAL_FORMS': '1',
            'paragraph-MAX_NUM_FORMS': '1000',

        }
        response = self.client.post(
            reverse('post-update', kwargs={'pk': post.pk}), data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_update_unsuccessful(self):
        title = 'hello world'
        data = {
            'title': title,
            'paragraph-0-text': 'lorem impsum',
            'paragraph-1-text': 'lorem impsum 2',
            'paragraph-MIN_NUM_FORMS': '0',
            'paragraph-INITIAL_FORMS': '0',
            'paragraph-TOTAL_FORMS': '2',
            'paragraph-MAX_NUM_FORMS': '1000',

        }
        response = self.client.post(reverse('post-create'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_delete(self):
        post = PostFactory()
        pk = post.pk
        response = self.client.get(reverse('post-delete', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(pk=pk))
