from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, modelformset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView, DetailView, FormView, UpdateView)

from aiesec_hris.core.views.mixins import MCRequiredMixin, PostFormAndFormsetInvalidMixin
from .forms import ParagraphForm, PostForm
from .models import Post, Category, Paragraph


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'newsfeed/post_list.html'
    paginate_by = 10

    def get_queryset(self):
        """
        Return the list of items for this view.
        The return value must be an iterable and may be an instance of
        `QuerySet` in which case `QuerySet` specific behavior will be enabled.
        """
        queryset = self.model.objects.all()
        filter_kwargs = {
            'post': 'title__icontains',
            'category': 'category__id'
        }
        queryset = filter_queryset(queryset, self.request.GET, filter_kwargs)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class PostDetail(LoginRequiredMixin, DetailView):
    """
    Post detail view
    Author: Nader Alexan
    """
    model = Post
    template_name = 'newsfeed/post_detail.html'


class PostCreate(MCRequiredMixin, PostFormAndFormsetInvalidMixin, FormView):
    """
    Create post view
    Author: Nader Alexan
    """
    template_name = 'newsfeed/post_form.html'
    paragraph_prefix = 'paragraph'
    ParagraphFormSet = formset_factory(ParagraphForm)

    def get_context_data(self, **kwargs):
        context = {
            'post_form': PostForm(),
            'paragraph_formset': self.ParagraphFormSet(
                prefix=self.paragraph_prefix)
        }
        return context

    def post(self, request, *args, **kwargs):
        paragraph_formset = self.ParagraphFormSet(
            request.POST, request.FILES, prefix=self.paragraph_prefix)
        post_form = PostForm(request.POST)
        if post_form.is_valid() and paragraph_formset.is_valid():
            return self.form_valid(post_form, paragraph_formset)
        else:
            return self.form_invalid(post_form, paragraph_formset)

    def form_valid(self, form, formset):
        post = form.save(commit=False)
        post.editor = self.request.user
        post.save()
        for i, form in enumerate(formset):
            # avoid creating empty paragraphs
            if (
                form.cleaned_data.get('text') or
                form.cleaned_data.get('youtube_url') or
                form.cleaned_data.get('document')
            ):
                paragraph = form.save(commit=False)
                paragraph.post = post
                paragraph.order = i
                paragraph.save()
        return JsonResponse(
            {'details': 'Post created successfully'}, status=201)


class PostUpdate(MCRequiredMixin, PostFormAndFormsetInvalidMixin, UpdateView):
    """
    Update post view
    Author: Nader Alexan
    """
    model = Post
    template_name = 'newsfeed/post_form.html'
    paragraph_prefix = 'paragraph'
    ParagraphFormSet = modelformset_factory(
        Paragraph, form=ParagraphForm, extra=0)

    def get_context_data(self, **kwargs):
        post = self.get_object()
        context = {
            'post_form': PostForm(instance=post),
            'paragraph_formset': self.ParagraphFormSet(
                prefix=self.paragraph_prefix, queryset=post.paragraph.all())
        }
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        paragraph_formset = self.ParagraphFormSet(
            request.POST,
            request.FILES,
            prefix=self.paragraph_prefix,
            queryset=post.paragraph.all())
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid() and paragraph_formset.is_valid():
            return self.form_valid(post_form, paragraph_formset)
        else:
            return self.form_invalid(post_form, paragraph_formset)

    def form_valid(self, form, formset):
        post = form.save()
        for form in formset:
            # avoid creating empty paragraphs
            if (
                form.cleaned_data.get('text') or
                form.cleaned_data.get('youtube_url') or
                form.cleaned_data.get('document')
            ):
                paragraph = form.save(commit=False)
                paragraph.post = post
                paragraph.save()
        return JsonResponse(
            {'details': 'Post created successfully'}, status=200)


def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    title = post.title
    if request.user.profile.position.type == 1:
        post.delete()
        success_message = 'Post %s deleted successfully' % title
        messages.success(
            request, success_message)
        return JsonResponse(
            {'details': success_message})
    return JsonResponse(
        {'details': 'You do not have permission to delete this post'},
        status=401)


def filter_queryset(queryset, params, filter_kwargs):
    """
    Filters queryset given paramaters and available filters

    Paramaters:
    1. queryset: queryset to perform filtering on and return.
    2. params: Dictionary of paramters to filter on and their values
    3. filter_kwargs: Dictionary of Available filters and corresponding lookups
    Author: Rana El-Garem
    """
    kwargs = {}  # Filter dictionary
    for field, value in params.items():
        if field in filter_kwargs:
            kwargs.update({filter_kwargs[field]: value})
    queryset = queryset.filter(**kwargs)
    return queryset
