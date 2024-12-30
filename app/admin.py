from django.contrib import admin
from .models import *

class NotesUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'email', 'contact_no')
    ordering = ('name',)

class NotesAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at')
    ordering = ('user', 'created_at')

# Register your models here.

admin.site.register(NotesUser, NotesUserAdmin)
admin.site.register(Notes, NotesAdmin)
