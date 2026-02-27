from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'class': 'search-box', # Aplicação do estilo de borda roxa/fundo escuro
                'placeholder': 'Escreva seu feedback aqui...',
                'rows': 2,
                'style': 'width: 100%; border-radius: 12px; resize: none;' # Ajustes extras de layout
            }),
        }