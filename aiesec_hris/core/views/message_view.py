from django.views.generic import TemplateView


class MessageView(TemplateView):
    """
    Generic message view.
    Use case: add a message to
    django.contrib.messages and redirect to this view
    Author: Nader Alexan
    """
    template_name = 'message.html'
