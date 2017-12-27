from django.contrib import admin

from aiesec_hris.education.models import *
from aiesec_hris.form_builder.models import *
from .models import (
    Event,
    LC,
    Position,
    Profile,
    Task,
    ExperiencePoints)


class ParagraphInline(admin.TabularInline):
    model = Paragraph


class PostAdmin(admin.ModelAdmin):
    inlines = [ParagraphInline]


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('lc',)


admin.site.register(Category)
admin.site.register(Event)
admin.site.register(ExperiencePoints)
admin.site.register(LC)
admin.site.register(Position)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)

admin.site.register(Form)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(SubmitForm)
admin.site.register(Task)
