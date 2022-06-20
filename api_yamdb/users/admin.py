from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role')
    list_display_links = ('id', 'username',)
    search_fields = ('username', 'email')

admin.site.register(User, UserAdmin)