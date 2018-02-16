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
    logger.debug("user {}, groups {}".format(request.user, request.user.groups.all()))
    if request.user.is_superuser:
        return render(request, 'hod/pendientes/list.html',
            {'slope_series': get_series_slope(None, 1), 
            'slope_series_session': get_series_slope(None, 2),})
    else:
        return render(request, 'hod/pendientes/list.html',
            {'slope_series': get_series_slope(request.user, 1), 
            'slope_series_session': get_series_slope(request.user, 2),})
   

@login_required(login_url='/accounts/login/')
def ver_ficha(request, ficha_id):
    logger.debug("Estamos en ver_ficha")
    ficha = get_object_or_404(Fichas, pk=ficha_id)
    slope_series_ficha = get_series_slope_ficha(ficha)
    return render(request, 'hod/pendientes/ficha.html',{'ficha': ficha, 'slope_series_ficha':slope_series_ficha})
    

@login_required(login_url='/accounts/login/')
def visto(request, visto_id):
    visto = get_object_or_404(Capitulos, pk=visto_id)
    visto.visto=True
    visto.save()
    return redirect('hod:ver_ficha',visto.ficha.id)





@login_required(login_url='/accounts/login/') 
def visto_ajax(request):
    
    from django.http import JsonResponse
    
    visto_id = request.GET.get('visto_id', None)
    logger.info("capitulo a tratar {}".format(visto_id))
    if visto_id:
        visto = get_object_or_404(Capitulos, pk=visto_id)
        visto.visto=True
        visto.save()
        ficha = get_object_or_404(Fichas, pk=visto.ficha.id)
        slope_series_ficha = get_series_slope_ficha(ficha)
        return render(request, 'hod/pendientes/ficha.html',{'ficha': ficha, 'slope_series_ficha':slope_series_ficha})
    return 



@login_required(login_url='/accounts/login/')
def visto_all(request, ficha_id):
    # en este metodo vamos a poner todos los capitulos como vistos
    logger.debug("Ficha_id {}".format(ficha_id))
    Capitulos.objects.filter(ficha=ficha_id).update(visto=True)
    return redirect('hod:ver_ficha',ficha_id)



@login_required(login_url='/accounts/login/')
def export(request):
    
    logger.debug("Estamos en export")
    if request.user.is_superuser:
        series = Series.objects.filter(author=request.user)
    else:
        series = Series.objects.all()
    for serie in series:
        
        ## Actualizamos las fichas que tengamos
        ficha, ficha_create = export_ficha(serie)
        # ficha, ficha_create = export_ficha_by_author(serie, request.user)
        
        
        ## Actualizamos los capitulos 
        if serie.ep_start:
            session = int(float(serie.ep_start[3:5])) or 0
            episode = int(float(serie.ep_start[-2:])) or 0
            
            for ep in range(episode-1,0,-1):
                temporada, created = Capitulos.objects.get_or_create(ficha=ficha, temporada=session, capitulo=ep, descargado=True)
        else:
            continue
      
    return redirect('hod:index')




def export_ficha(serie):
    
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


    
def get_series_slope(user, estado):
    slope_series = []
     ## Recuperamos todas las series del usuario
    if user:
        fichas = Fichas.objects.filter(author=user).filter(estado=estado)
    else:
        fichas = Fichas.objects.filter(estado=estado)
    
    for ficha in fichas:
        logger.debug("ficha : {}".format(ficha))
        obj = Capitulos.objects.filter(ficha=ficha).filter(visto=False).filter(descargado=True).order_by('capitulo')[:1]
        if obj:
            logger.debug("captitulos pendientes : {}".format(obj[0].ficha.nombre))
            slope_series.append(obj)
    # slope_series = Vistos.objects.filter(temporada__ficha__author=request.user).filter(visto=False)  # No es broma, se puede seguir la tabla para arriba  """temporada__ficha__author"""
    logger.debug("slope_series : {}".format(slope_series))
    return slope_series;
    
    
def get_series_slope_ficha(ficha):
    slope_series_ficha= Capitulos.objects.filter(ficha=ficha).filter(visto=False).order_by('temporada','capitulo')
    logger.debug("captitulos pendientes : {}".format(slope_series_ficha))
    return slope_series_ficha;
    