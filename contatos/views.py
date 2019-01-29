import datetime
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string


from .forms import ContatoForm, ContatoRespostaForm, ContatoPreExclusaoForm
from .models import Contato


def contato_create(request):
    form = ContatoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Inclusão bem sucedida!", extra_tags="some-tags")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "contact.html", context)


@login_required
def contato_list(request):
    queryset_list = Contato.objects.excluidos()
    excluidos = queryset_list.count()

    queryset_list = Contato.objects.send()
    respondidos = queryset_list.count()

    queryset_list = Contato.objects.active()
    emabertos = queryset_list.count()

    today = datetime.datetime.now()

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Contato.objects.all().filter(status=False).filter(statusexcluido=False)

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(nome__icontains=query) |
            Q(email__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 25)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    context = {
        "object_list": queryset,
        "title": "Pendêntes",
        "today": today,
        "respondidos": respondidos,
        "emabertos": emabertos,
        "excluidos": excluidos,
    }
    return render(request, "contato_list.html", context)


@login_required
def contato_list_respondidos(request):
    queryset_list = Contato.objects.excluidos()
    excluidos = queryset_list.count()

    queryset_list = Contato.objects.send()
    respondidos = queryset_list.count()

    queryset_list = Contato.objects.active()
    emabertos = queryset_list.filter(status=False).count()

    today = datetime.datetime.now()

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Contato.objects.all().filter(status=True).filter(statusexcluido=False)

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(nome__icontains=query) |
            Q(email__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 25)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    context = {
        "object_list": queryset,
        "title": "Respondidos",
        "today": today,
        "respondidos": respondidos,
        "emabertos": emabertos,
        "excluidos": excluidos,
    }
    return render(request, "contato_list.html", context)

@login_required
def contato_list_pre_exclusao(request):
    queryset_list = Contato.objects.excluidos()
    excluidos = queryset_list.count()

    queryset_list = Contato.objects.send()
    respondidos = queryset_list.count()

    queryset_list = Contato.objects.active()
    emabertos = queryset_list.filter(status=False).count()

    today = datetime.datetime.now()

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Contato.objects.all().filter(statusexcluido=True)

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(nome__icontains=query) |
            Q(email__icontains=query) |
            Q(content__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 25)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)

    context = {
        "object_list": queryset,
        "title": "Excluídos",
        "today": today,
        "respondidos": respondidos,
        "emabertos": emabertos,
        "excluidos": excluidos,
    }
    return render(request, "contato_list.html", context)


@login_required  # (login_url="/login/")
def contato_pre_exclusao(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    obj = Contato.objects.get(id=id)
    form = ContatoPreExclusaoForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.statusexcluido = True
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "instance": obj,
        "title": obj.nome,
        "form": form,
    }
    return render(request, "contact_resposta.html", context)


@login_required  # (login_url="/login/")
def contato_delete(request, id):
    try:
        obj = Contato.objects.get(id=id)
    except:
        raise Http404

    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Infomação foi excluida!")
        return HttpResponseRedirect(obj.get_absolute_url())

    context = {
        "object": obj,
    }
    return render(request, "confirm_delete.html", context)


@login_required  # (login_url="/login/")
def contato_resposta(request, id):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    obj = Contato.objects.get(id=id)
    form = ContatoRespostaForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.status = True
        instance.save()

        to_email = obj.email
        message = obj.contatoresposta
        subject = "Feepaerj respondeu a seu contato"

        ctx = {
            'TITLE': subject,
            'message': message,
            'SITE_NAME': 'www.compnetinformatica.com.br',
            'SITE_DOMAIN': '.',
            'nome': obj.nome,
        }

        c = Context(ctx).flatten()
        text_content = render_to_string('email/base.txt', c)
        html_content = render_to_string('email/base.html', c)

        email = EmailMultiAlternatives(subject, text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [to_email]
        email.send()

        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "instance": obj,
        "title": obj.nome,
        "form": form,
    }
    return render(request, "contact_resposta.html", context)
