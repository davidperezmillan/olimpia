#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Case, Value, When
from django.http import JsonResponse

from hoor.models import Ficha, Capitulo
from hoor.forms import FichaModelForm
import hoor.business.scrape.handler_scrap

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
from hoor.subviews.views_utiles import *


@login_required(login_url='/accounts/login/')
def list(request):
    logger.debug("Estamos en list")
    if request.user.is_superuser:
        latest_series_update = Ficha.objects.all()
    else:
        latest_series_update = Ficha.objects.filter(author=request.user).all()
    
    for ficha in latest_series_update:    
        slope_series_ficha = get_series_ficha(ficha)
        logger.debug("Ficha {}, Capitulos {}".format(ficha, slope_series_ficha))
        down_series_ficha = get_series_down_ficha(ficha)
        ficha.slope = slope_series_ficha
        ficha.down = down_series_ficha
    
    context = {'latest_series_update': latest_series_update}
    return render(request, 'hoor/series/list.html', context)


@login_required(login_url='/accounts/login/')
def ver_ficha(request, ficha_id):
    logger.debug("Estamos en ver_ficha")
    ficha = get_object_or_404(Ficha, pk=ficha_id)
    logger.debug("Ficha {}".format(ficha.nombre))
    if request.method == "POST":
        form = FichaModelForm(request.POST, instance=ficha)
        if form.is_valid():
            ficha = form.save(commit=False)
            # serie.author = request.user
            ficha.save()
    else:
        form = FichaModelForm(instance=ficha)

    slope_series_ficha = get_series_ficha(ficha)
    logger.debug("Ficha {}, Capitulos {}".format(ficha, slope_series_ficha))
    down_series_ficha = get_series_down_ficha(ficha)
    logger.debug("Ficha {}, Capitulos {}, Descargado: {}".format(ficha, slope_series_ficha, down_series_ficha))
    return render(request, 'hoor/pendientes/ficha.html',{'form': form,'ficha': ficha, 'slope_series_ficha':slope_series_ficha, 'down_series_ficha':down_series_ficha})
    
@login_required(login_url='/accounts/login/')
def add_ficha(request):
    logger.debug("Estamos en add_ficha")
    if request.method == 'POST':
        form = FichaModelForm(request.POST)
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.author=request.user
            ficha.save()
            info_ficha(request,ficha.id)
            return redirect('ver_ficha',ficha.id)
        return render(request, 'hoor/pendientes/ficha.html',{'form': form,})
    else:
        form = FichaModelForm()
        return render(request, 'hoor/pendientes/ficha.html',{'form': form,})    

@login_required(login_url='/accounts/login/')
def visto(request, capitulo_id):
    visto = get_object_or_404(Capitulo, pk=capitulo_id)
    visto.visto= False if visto.visto else True
    visto.save()
    return redirect('ver_ficha',visto.ficha.id)
    

@login_required(login_url='/accounts/login/')
def visto_all(request, ficha_id):
    # en este metodo vamos a poner todos los capitulos como vistos
    logger.debug("Ficha_id {}".format(ficha_id))
    # Capitulo.objects.filter(ficha=ficha_id).update(visto=Case(When(visto=True, then=Value(False)),default=Value(True)))
    Capitulo.objects.filter(ficha=ficha_id).update(visto=True)
    return redirect('ver_ficha',ficha_id)

@login_required(login_url='/accounts/login/')
def visto_all_session(request,ficha_id,session_id):
    # en este metodo vamos a poner todos los capitulos como vistos
    logger.debug("Ficha_id {}, Session_id : {}".format(ficha_id,session_id))
    # Capitulo.objects.filter(ficha=ficha_id).filter(temporada=session_id).update(visto=Case(When(visto=True, then=Value(False)),default=Value(True)))
    Capitulo.objects.filter(ficha=ficha_id).filter(temporada=session_id).update(visto=True)
    return redirect('ver_ficha',ficha_id)
    
    


@login_required(login_url='/accounts/login/')
def toggle_capitulo(request, capitulo_id):
    logger.debug("Estamos en toggleVisto_capitulo")
    
    capitulo = get_object_or_404(Capitulo, pk=capitulo_id)
    
    if capitulo.descargado:
        if capitulo.visto:
            capitulo.descargado = False
            capitulo.visto = False
        else:
            capitulo.visto = True
    else:
        capitulo.descargado = True
        capitulo.visto = False
    data = {
        'visto': capitulo.visto,
        'descargado': capitulo.descargado
    }
    capitulo.save()
    logger.debug("Devolvemos {}".format(data))
    return JsonResponse(data)    
    
# @login_required(login_url='/accounts/login/')
# def toggle_session(request, ficha_id,session_id):
#     descargado = request.GET.get('descargado', None)
#     visto = request.GET.get('visto', None)
    
#     logger.debug("Estamos en toggleVisto_session ficha: {} session: {} descargado: {} visto: {}".format(ficha_id,session_id, descargado, visto))
#     if descargado:
#         Capitulo.objects.filter(ficha=ficha_id).filter(temporada=session_id).update(descargado=descargado)
#     if visto:
#         Capitulo.objects.filter(ficha=ficha_id).filter(temporada=session_id).update(visto=visto)
#     data = {
#         'session': session_id,
#         'descargado': descargado,
#         'visto': visto,
#     }
#     logger.debug("Devolvemos {}".format(data))
#     return JsonResponse(data)        

    
@login_required(login_url='/accounts/login/')
def info_ficha(request, ficha_id):
    logger.debug("Estamos en info_ficha")
    ficha = get_object_or_404(Ficha, pk=ficha_id)
    hoor.business.scrape.handler_scrap.getInfoOlimpia([ficha], None) # No se envia session todos las sessiones
    return redirect('ver_ficha',ficha.id)


