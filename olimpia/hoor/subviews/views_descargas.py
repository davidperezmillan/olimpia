#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Case, Value, When

from hoor.models import Ficha, Capitulo, Descarga

from hoor.forms import DescargaModelForm


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
from hoor.subviews.views_utiles import *

### DOWN
@login_required(login_url='/accounts/login/')
def ver_down(request, down_id):
    logger.debug("Estamos en ver_down")
    down = get_object_or_404(Descarga, pk=down_id)
    if request.method == "POST":
        form = DescargaModelForm(request.POST, instance=down)
        if form.is_valid():
            down = form.save(commit=False)
            down.save()
            return redirect('ver_ficha',down.ficha.id)
    else:
        form = DescargaModelForm(instance=down)
    return render(request, 'hoor/down/down.html',{'form': form,  'down': down})
    
@login_required(login_url='/accounts/login/')
def add_down_for_ficha(request, ficha_id):
    logger.debug("Estamos en add_down_for_ficha")
    ficha = get_object_or_404(Ficha, pk=ficha_id)
    if request.method == 'POST':
        form = DescargaModelForm(request.POST)
        if form.is_valid():
            print
            down = form.save(commit=False)
            down.save()
            return redirect('ver_ficha',down.ficha.id)
    else:
        form = DescargaModelForm()
    form.fields["ficha"].initial = ficha
    logger.debug(form)
    return render(request, 'hoor/down/down.html',{'form': form,'ficha': ficha})

# Deprecated 
# No se utiliza porque no se deberia añadir ninguna descarga sin ficha
@login_required(login_url='/accounts/login/')
def add_down(request):
    logger.debug("Estamos en add_down")
    if request.method == 'POST':
        form = DescargaModelForm(request.POST)
        if form.is_valid():
            down = form.save(commit=False)
            down.save()
            return redirect('ver_ficha',down.ficha.id)
    else:
        form = DescargaModelForm()
    return render(request, 'hoor/down/down.html',{'form': form,})


@login_required(login_url='/accounts/login/')
def down_delete(request, down_id):
    down = get_object_or_404(Descarga, pk=down_id)
    down=Descarga.objects.get(pk=down_id)
    down.delete()
    return redirect('ver_ficha',down.ficha.id)



# DESCARGADO 
@login_required(login_url='/accounts/login/')
def descargado(request, capitulo_id):
    descargado = get_object_or_404(Capitulo, pk=capitulo_id)
    descargado.descargado = False if descargado.descargado else True
    descargado.save()
    return redirect('ver_ficha',descargado.ficha.id)

@login_required(login_url='/accounts/login/')
def descargado_all(request, ficha_id):
    # en este metodo vamos a poner todos los capitulos como descargados
    logger.debug("Ficha_id {}".format(ficha_id))
    Capitulo.objects.filter(ficha=ficha_id).update(descargado=Case(When(descargado=True, then=Value(False)),default=Value(True)))
    return redirect('ver_ficha',ficha_id)

@login_required(login_url='/accounts/login/')
def descargado_all_session(request,ficha_id,session_id):
    # en este metodo vamos a poner todos los capitulos como descargados
    logger.debug("Ficha_id {}, Session_id : {}".format(ficha_id,session_id))
    Capitulo.objects.filter(ficha=ficha_id).filter(temporada=session_id).update(descargado=Case(When(descargado=True, then=Value(False)),default=Value(True)))
    return redirect('ver_ficha',ficha_id)
    
    



