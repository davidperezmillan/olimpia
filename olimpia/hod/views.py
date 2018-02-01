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
def export(request):
    series = Series.objects.all()
    for serie in series:
        
        ## Actualizamos las fichas que tengamos
        ficha, created = Fichas.objects.get_or_create(nombre=serie.nombre)
        
        ## Actualizamos los capitulos 
        descargado = serie.ep_start

        ## aqui la liamos int(float(a))
        if descargado:
            quality = descargado[:2] or None
            session = int(float(descargado[3:5])) or 0
            episode = int(float(descargado[-2:])) or 0
        
        print("descargado {} -- session {} -- episode {}".format(descargado,session, episode))
        
        if episode > 0:
            episode = episode-1
            
            for i in range(episode,0,-1):
                 ## error
                print("serie {} -- session {} -- episode {}".format(serie.nombre, session, i))
                capitulo, created = Capitulos.objects.get_or_create(ficha=ficha, temporada=session, capitulo=i)
                
                print("visto {} -- capitulo_id {}".format(serie.nombre, capitulo.id))
                visto, created = Vistos.objects.get_or_create(author=serie.author, capitulo=capitulo, descargado=True)
                      
            
        else:
            # No grabamos nada
            continue
        
        
        
    return
