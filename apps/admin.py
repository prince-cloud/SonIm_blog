from django.contrib import admin

from .models import Event, Gallery, Member, Upcomingevent, Message, Profile, Comment

# Register your models here.
admin.site.register(Event)
admin.site.register(Gallery)
admin.site.register(Member)
admin.site.register(Upcomingevent)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject',)

admin.site.register(Profile)
admin.site.register(Comment)