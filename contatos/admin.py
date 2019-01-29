from django.contrib import admin
from .models import Contato


class ContatoModelAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "updated",  "timestamp"]
    list_display_links = ["nome"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["nome", "content", "email"]

    class Meta:
        model = Contato


admin.site.register(Contato, ContatoModelAdmin)

