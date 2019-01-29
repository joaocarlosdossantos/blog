from django import forms
from .models import Contato
from pagedown.widgets import PagedownWidget


class ContatoForm(forms.ModelForm):
    nome = forms.CharField(required=True, label="Nome")
    email = forms.EmailField(required=True, label="Email")
    content = forms.CharField(widget=PagedownWidget(show_preview=False), label="Texto")

    class Meta:
        model = Contato
        fields = [
            'nome',
            'email',
            'content',
        ]


class ContatoRespostaForm(forms.ModelForm):
    contatoresposta = forms.CharField(widget=PagedownWidget(show_preview=False), label="Resposta")

    class Meta:
        model = Contato
        fields = [
            'contatoresposta',
        ]


class ContatoPreExclusaoForm(forms.ModelForm):
    motivocancelamento = forms.CharField(widget=PagedownWidget(show_preview=False), label="Motivo")

    class Meta:
        model = Contato
        fields = [
            'motivocancelamento',
        ]
