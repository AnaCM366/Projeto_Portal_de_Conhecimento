from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validar_arquivo(value):
    if not value.name.endswith(('.pdf', '.doc', '.docx')):
        raise ValidationError('Apenas arquivos PDF ou Word são permitidos.')

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