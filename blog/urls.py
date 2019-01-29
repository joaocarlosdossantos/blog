from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from accounts.views import (login_view,
                            register_view,
                            logout_view
                            )

from contatos.views import (contato_create,
                            contato_list,
                            contato_list_respondidos,
                            contato_list_pre_exclusao
                            )

from posts.views import post_create

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include(('comments.urls', 'comments'), namespace='comments')),
    url(r'^contatos/', include(('contatos.urls', 'contatos'), namespace='contatos')),
    url(r'^register/', register_view, name='register'),
    url(r'^login/', login_view, name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^contatocreate/', contato_create, name='contatocreate'),
    url(r'^contatolist/', contato_list, name='contatolist'),
    url(r'^contatolistrespondidos/', contato_list_respondidos, name='contatolistrespondidos'),
    url(r'^contatolistpreexcluidos/$', contato_list_pre_exclusao, name='contatolistpreexcluidos'),
    url(r'^create/', post_create, name='create'),
    url(r'^', include(('posts.urls', 'posts'), namespace='posts')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






