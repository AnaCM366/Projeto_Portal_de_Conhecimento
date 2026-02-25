from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'criado_em')

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('arquivo',)
        return ()

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.arquivo = None
        super().save_model(request, obj, form, change)

admin.site.register(Post, PostAdmin)