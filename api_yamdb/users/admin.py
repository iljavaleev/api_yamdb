from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import CustomUserChangeForm

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    list_display = ('id',
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'bio',
                    'role'
                    )
    list_display_links = ('id', 'username',)
    search_fields = ('username', 'email')


admin.site.register(User, UserAdmin)
