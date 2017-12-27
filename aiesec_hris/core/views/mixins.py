from django.http import JsonResponse
from django.contrib.auth.mixins import AccessMixin


class JsonFormInvalidMixin(object):
    """
    Mixin for views based on FormView
    to override the `form_invalid` function and return
    an error list
    Author: Nader Alexan
    """
    def form_invalid(self, form):
        details = ["%s<br>%s" % (
            field.label, field.errors
        ) for field in form if field.errors]
        return JsonResponse({'details': details}, status=400)


class MCRequiredMixin(AccessMixin):
    """
    CBV mixin which verifies that the current user is an MC.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.position.type == 1:
                return super(MCRequiredMixin, self).dispatch(
                    request, *args, **kwargs)
        return self.handle_no_permission()


class PostFormAndFormsetInvalidMixin:
    def form_invalid(self, form, formset):
        def get_errors(form):
            errors = []
            for field in form:
                if field.errors:
                    errors.append("%s<br>%s" % (field.label, field.errors))
            return errors

        errors = get_errors(form)
        for f in formset:
            errors += get_errors(f)
        return JsonResponse({'details': errors}, status=400)
