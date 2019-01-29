from django.conf.urls import url
from .views import (
        contato_create,
        contato_list,
        contato_list_respondidos,
        contato_list_pre_exclusao,
        contato_delete,
        contato_resposta,
        contato_pre_exclusao,
)

urlpatterns = [
    url(r'^contatocreate/$', contato_create),
    url(r'^contatolist/$', contato_list, name='contatolist'),
    url(r'^contatolistrespondidos/$', contato_list_respondidos, name='contatolistrespondidos'),
    url(r'^contatolistpreexcluidos/$', contato_list_pre_exclusao, name='contatolistpreexcluidos'),
    url(r'^(?P<id>\d+)/contatodelete/$', contato_delete, name='contatodelete'),
    url(r'^(?P<id>\d+)/contatopreexclusao/$', contato_pre_exclusao, name='contatopreexclusao'),
    url(r'^(?P<id>\d+)/contatoresposta/$', contato_resposta, name='contatoresposta'),
]
