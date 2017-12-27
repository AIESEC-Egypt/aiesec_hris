from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from ..models import LC, Position


class LCQuerysetBase(LoginRequiredMixin):
    def get_queryset(self):
        # MC user, allowed access to all LCs
        if self.request.user.profile.position.type == 1:
            return LC.objects.all()
        # LC user, allowed access to their LC only
        return LC.objects.filter(pk=self.request.user.profile.lc.pk)


class LCList(LCQuerysetBase, ListView):
    """
    List view for LC
    Author: Nader Alexan
    """
    model = LC
    template_name = 'lc/lc_list.html'
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(LCList, self).get_context_data(**kwargs)
        context['fields'] = self.fields
        return context


class LCDetail(LCQuerysetBase, DetailView):
    """
    Detail view of LC
    Author: Nader Alexan
    """
    model = LC
    template_name = 'lc/lc_detail.html'

    def get_context_data(self, **kwargs):
        def build_lc_tree(root, tree):
            children = root.children.all()
            if children:
                tree += [children]
                for child in children:
                    build_lc_tree(child, tree)
            return tree
        context = super(LCDetail, self).get_context_data(**kwargs)
        root = Position.objects.filter(
            lc=self.get_object(), parent=None).first()
        lc_tree = build_lc_tree(root, [[root]])
        context['lc_tree'] = lc_tree
        return context
