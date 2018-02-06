import logging


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Create your views here.
from merc.models import Series
from .models import Fichas, Capitulos

# Get an instance of a logger
logger = logging.getLogger(__name__)



@login_required(login_url='/accounts/login/')
def index(request):
    logger.debug("Estamos en index")
    return render(request, 'hod/pendientes/list.html',
        {'slope_series': get_series_slope(request.user), 
        'slope_series_session': get_series_slope_session(request.user),})


@login_required(login_url='/accounts/login/')
def visto(request, visto_id):
    visto = get_object_or_404(Capitulos, pk=visto_id)
    visto.visto=True
    visto.save()
    return redirect('index')
    


@login_required(login_url='/accounts/login/')
def export(request):
    
    logger.debug("Estamos en export")
    series = Series.objects.all()
    for serie in series:
        
        ## Actualizamos las fichas que tengamos
        ficha, ficha_create = export_ficha_by_author(serie, request.user)
        
        
        ## Actualizamos los capitulos 
        if serie.ep_start:
            session = int(float(serie.ep_start[3:5])) or 0
            episode = int(float(serie.ep_start[-2:])) or 0
            
            for ep in range(episode,0,-1):
                temporada, created = Capitulos.objects.get_or_create(ficha=ficha, temporada=session, capitulo=ep)
        else:
            continue
      
    return redirect('index')




def export_ficha(serie):
    ## Actualizamos las fichas que tengamos
    ficha, created = Fichas.objects.get_or_create(nombre=serie.nombre, author=serie.author, estado=1) 
    return ficha, created
    

def export_ficha_by_author(serie, user):
    
    '''
    choice_ficha_estado = (
    (0 , 'Descartada'),
    (1 , 'Activa'),
    (2 , 'Pendiente de nueva Temporada'),
    (3 , 'Cancelada'),
    (4 , 'Terminada'),
    )
    '''
    
    
    ## Actualizamos las fichas que tengamos
    estado = 1
    if serie.skipped:
        estado = 0
    if 0 == int(float(serie.ep_start[-2:])):
        estado = 2
    
    ficha, created = Fichas.objects.get_or_create(nombre=serie.nombre, author=serie.author, estado=estado) 
    return ficha, created


    
def get_series_slope(user):
    slope_series = []
     ## Recuperamos todas las series del usuario
    fichas = Fichas.objects.filter(author=user).filter(estado=1)
    
    for ficha in fichas:
        logger.debug("ficha : {}".format(ficha))
        obj = Capitulos.objects.filter(ficha=ficha).filter(visto=False).order_by('capitulo')[:1]
        if obj:
            logger.debug("captitulos pendientes : {}".format(obj[0].ficha.nombre))
            slope_series.append(obj)
    # slope_series = Vistos.objects.filter(temporada__ficha__author=request.user).filter(visto=False)  # No es broma, se puede seguir la tabla para arriba  """temporada__ficha__author"""
    logger.debug("slope_series : {}".format(slope_series))
    return slope_series;
    
    
def get_series_slope_session(user):
    slope_series = []
     ## Recuperamos todas las series del usuario
    fichas = Fichas.objects.filter(author=user).filter(estado=2)
    
    for ficha in fichas:
        logger.debug("ficha : {}".format(ficha))
        obj = Capitulos.objects.filter(ficha=ficha).filter(visto=False).order_by('capitulo')[:1]
        if obj:
            logger.debug("captitulos pendientes : {}".format(obj[0].ficha.nombre))
            slope_series.append(obj)
    # slope_series = Vistos.objects.filter(temporada__ficha__author=request.user).filter(visto=False)  # No es broma, se puede seguir la tabla para arriba  """temporada__ficha__author"""
    logger.debug("slope_series : {}".format(slope_series))
    return slope_series;