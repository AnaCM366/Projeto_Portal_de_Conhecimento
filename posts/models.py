from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Validador de arquivos
def validar_arquivo(value):
    if not value.name.endswith(('.pdf', '.doc', '.docx')):
        raise ValidationError('Apenas arquivos PDF ou Word são permitidos.')

# Modelo de Postagem
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    arquivo = models.FileField(
        upload_to='documentos/',
        validators=[validar_arquivo],
        null=True,
        blank=True,
    )    
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Feedback(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='feedbacks')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.usuario} em {self.post.titulo}"