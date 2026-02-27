from django.contrib import admin
from .models import Profile
from posts.models import Feedback

admin.site.register(Profile)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # Escolhemos quais colunas aparecerão na lista do admin
    list_display = ('usuario', 'post', 'data_envio', 'comentario_curto')
    
    # Adicionamos filtros na lateral para facilitar a busca
    list_filter = ('data_envio', 'usuario', 'post')
    
    # Campo de busca para encontrar feedbacks específicos
    search_fields = ('comentario', 'usuario__username', 'post__titulo')

    # Função extra para mostrar apenas o começo do comentário na lista
    def comentario_curto(self, obj):
        return obj.comentario[:50] + "..." if len(obj.comentario) > 50 else obj.comentario
    comentario_curto.short_description = 'Comentário'