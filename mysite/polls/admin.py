from django.contrib import admin
from django.contrib.auth.models import User

from polls.models import Poll
from polls.models import Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['user', 'question']}),
        ('Date Information', {'fields':['pub_date'], 'classes': ['collapse']})
        ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_today')
    lists_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'

    def queryset(self, request):
        qs = super(PollAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user" and not request.user.is_superuser:
            kwargs['queryset'] = User.objects.filter(id=request.user.id)
        return super(PollAdmin, self)\
                 .formfield_for_foreignkey(db_field, request, **kwargs)
    
admin.site.register(Poll, PollAdmin)
