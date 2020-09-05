from django.contrib import admin

from .models import Event, Member, Upcomingevent, Message, Profile, Comment, Picture

# Register your models here.
admin.site.register(Event)

@admin.register(Member)
class MeberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email',)

admin.site.register(Upcomingevent)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject',)

admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Picture)