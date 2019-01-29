from django.db import models
from django.urls import reverse
from django.utils import timezone


class PostManager(models.Manager):
    def active(self, *args, ** kwargs):
        return super(PostManager, self).filter(status=False).filter(updated__lte=timezone.now())

    def send(self, *args, ** kwargs):
        return super(PostManager, self).filter(status=True).filter(statusexcluido=False).filter(updated__lte=timezone.now())

    def excluidos(self, *args, ** kwargs):
        return super(PostManager, self).filter(statusexcluido=True).filter(updated__lte=timezone.now())


class Contato(models.Model):
    nome = models.CharField(max_length=120)
    email = models.EmailField(null=False, blank=False)
    content = models.TextField()
    contatoresposta = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    statusexcluido = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    motivocancelamento = models.CharField(max_length=10, default='Padrão', blank=False, choices=(
        ('Padrão', 'Padrão'),
        ('OUTROS', 'OUTROS'),
    ))

    class Meta:
        ordering = ["-timestamp", "-updated"]

    objects = PostManager()

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("contatos:contatolist")

    def get_preexclusao_url(self):
        return reverse("contatos:contatopreexclusao", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("contatos:contatodelete", kwargs={"id": self.id})

    def get_resposta_url(self):
        return reverse("contatos:contatoresposta", kwargs={"id": self.id})

    def get_respondidos_url(self):
        return reverse("contatos:contatolistrespondidos")

