from django.contrib import admin
<<<<<<< HEAD

from .models import User
=======
from django.contrib.auth import get_user_model


User = get_user_model()

>>>>>>> 5ca4f1f0c443ec0e28d06357e363acc8cdfc9e90

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role')
    list_display_links = ('id', 'username',)
    search_fields = ('username', 'email')

<<<<<<< HEAD
admin.site.register(User, UserAdmin)
=======

admin.site.register(User, UserAdmin)
>>>>>>> 5ca4f1f0c443ec0e28d06357e363acc8cdfc9e90
