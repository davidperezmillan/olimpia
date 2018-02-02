import logging


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Create your views here.
from merc.models import Series
from .models import Fichas, Capitulos, Vistos

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required(login_url='/accounts/login/')
def index(request):
    slope_series = Vistos.objects.filter(author=request.user).filter(visto=False)    
    return render(request, 'hod/pendientes/list.html',{'slope_series': slope_series, })




@login_required(login_url='/accounts/login/')
def export(request):
    
    series = Series.objects.all()
    for serie in series:
        
        ## Actualizamos las fichas que tengamos
        ficha, ficha_create = export_ficha(serie)
        
        
        ## Actualizamos los capitulos 
        if serie.ep_start:
            session = int(float(serie.ep_start[3:5])) or 0
            episode = int(float(serie.ep_start[-2:])) or 0
            
            for s in range(session,0,-1):
                temporada, created = Capitulos.objects.get_or_create(ficha=ficha, temporada=s, capitulos=episode)
        else:
            continue
            
    slope_series = Vistos.objects.filter(author=request.user)    
        
    return render(request, 'hod/pendientes/list.html',{'slope_series': slope_series, })




def export_ficha(serie):
    ## Actualizamos las fichas que tengamos
    ficha, created = Fichas.objects.get_or_create(nombre=serie.nombre, estado=1) 
    return ficha, created