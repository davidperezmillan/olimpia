import logging


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import Ficha, Capitulo, Document, Descarga

from .forms import UploadFileForm, FichaModelForm,DescargaModelForm
from django.core.files.storage import FileSystemStorage

import hoor.scrape.handler_scrap

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


@login_required(login_url='/accounts/login/')
def index(request):
    logger.debug("Estamos en index")
    logger.debug("user {}, groups {}".format(request.user, request.user.groups.all()))
    return render(request, 'hoor/pendientes/list.html',
        {'slope_series': get_series_slope(request.user, 1), 
        'slope_series_session': get_session_slope(request.user, 2),})


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
    return render(request, 'hoor/down/down.html',{'form': form,})
    
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
    return render(request, 'hoor/down/down.html',{'form': form,})

@login_required(login_url='/accounts/login/')
def add_down(request):
    logger.debug("Estamos en add_down")
    ficha = get_object_or_404(Ficha, pk=ficha_id)
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
def visto(request, capitulo_id):
    visto = get_object_or_404(Capitulo, pk=capitulo_id)
    visto.visto=True
    visto.save()
    return redirect('ver_ficha',visto.ficha.id)
    

@login_required(login_url='/accounts/login/')
def visto_all(request, ficha_id):
    # en este metodo vamos a poner todos los capitulos como vistos
    logger.debug("Ficha_id {}".format(ficha_id))
    Capitulo.objects.filter(ficha=ficha_id).update(visto=True)
    return redirect('ver_ficha',ficha_id)

@login_required(login_url='/accounts/login/')
def visto_all_session(request,ficha_id,session_id):
    # en este metodo vamos a poner todos los capitulos como vistos
    logger.debug("Ficha_id {}, Session_id : {}".format(ficha_id,session_id))
    Capitulo.objects.filter(ficha=ficha_id).filter(temporada=session_id).update(visto=True)
    return redirect('ver_ficha',ficha_id)
    
    
# DESCARGADO 
@login_required(login_url='/accounts/login/')
def descargado(request, capitulo_id):
    descargado = get_object_or_404(Capitulo, pk=capitulo_id)
    descargado.descargado=True
    descargado.save()
    return redirect('ver_ficha',descargado.ficha.id)
    

@login_required(login_url='/accounts/login/')
def descargado_all(request, ficha_id):
    # en este metodo vamos a poner todos los capitulos como descargados
    logger.debug("Ficha_id {}".format(ficha_id))
    Capitulo.objects.filter(ficha=ficha_id).update(descargado=True)
    return redirect('ver_ficha',ficha_id)

@login_required(login_url='/accounts/login/')
def descargado_all_session(request,ficha_id,session_id):
    # en este metodo vamos a poner todos los capitulos como descargados
    logger.debug("Ficha_id {}, Session_id : {}".format(ficha_id,session_id))
    Capitulo.objects.filter(ficha=ficha_id).filter(temporada=session_id).update(descargado=True)
    return redirect('ver_ficha',ficha_id)


@login_required(login_url='/accounts/login/')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
        	doc = form.save(commit=True)
        	doc.save()
        	return render(request, 'hoor/upload_file/upload_file.html', {'form': form,'uploaded_file_url': doc})
        return render(request, 'hoor/upload_file/upload_file.html', {'form': UploadFileForm(),'uploaded_file_url': doc})
    else:
        form = UploadFileForm()
    #tambien se puede utilizar render_to_response
    #return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))
    return render(request, 'hoor/upload_file/upload_file.html', {'form': form})

@login_required(login_url='/accounts/login/')
def info_ficha(request, ficha_id):
    logger.debug("Estamos en info_ficha")
    ficha = get_object_or_404(Ficha, pk=ficha_id)
    hoor.scrape.handler_scrap.getInfoOlimpia([ficha], None) # No se envia session todos las sessiones
    return redirect('ver_ficha',ficha.id)



    
   
# privado
def get_series_slope(user, estado):
    slope_series = []
     ## Recuperamos todas las series del usuario
    fichas = Ficha.objects.filter(author=user).filter(estado=estado)
    
    for ficha in fichas:
        logger.debug("ficha : {}".format(ficha))
        obj = Capitulo.objects.filter(ficha=ficha).filter(visto=False).filter(descargado=True).order_by('capitulo')[:1]
        if obj:
            logger.debug("captitulos pendientes : {}".format(obj[0].ficha.nombre))
            slope_series.append(obj)
    # slope_series = Vistos.objects.filter(temporada__ficha__author=request.user).filter(visto=False)  # No es broma, se puede seguir la tabla para arriba  """temporada__ficha__author"""
    logger.debug("slope_series : {}".format(slope_series))
    return slope_series;

# privado
def get_session_slope(user, estado):
    slope_series = []
     ## Recuperamos todas las series del usuario
    fichas = Ficha.objects.filter(author=user).filter(estado=estado)
    
    for ficha in fichas:
        logger.debug("ficha : {}".format(ficha))
        obj = Capitulo.objects.filter(ficha=ficha).filter(visto=False).order_by('capitulo')[:1]
        if obj:
            logger.debug("captitulos pendientes : {}".format(obj[0].ficha.nombre))
            slope_series.append(obj)
    # slope_series = Vistos.objects.filter(temporada__ficha__author=request.user).filter(visto=False)  # No es broma, se puede seguir la tabla para arriba  """temporada__ficha__author"""
    logger.debug("slope_series : {}".format(slope_series))
    return slope_series;

    
# def get_series_ficha_old(ficha):
#     slope_series_ficha= Capitulo.objects.filter(ficha=ficha).filter(visto=False).order_by('capitulo')
#     logger.debug("captitulos pendientes : {}".format(slope_series_ficha))
#     return slope_series_ficha;

# privado
def get_series_ficha(ficha):
    slope_series_ficha = []
    temporadas =  Capitulo.objects.values('temporada').distinct().filter(ficha=ficha).order_by('temporada')
    for temporada in temporadas:
        my_dict = {'temporada':temporada, 'capitulos' : Capitulo.objects.filter(ficha=ficha).filter(temporada=temporada['temporada']).order_by('capitulo')}
        slope_series_ficha.extend([my_dict])
        
    logger.debug("Temporadas pendientes : {}".format((slope_series_ficha)))
    # slope_series_ficha= Capitulos.objects.filter(ficha=ficha).filter(visto=False).order_by('temporada','capitulo')
    # logger.debug("captitulos pendientes : {}".format(slope_series_ficha))
    return slope_series_ficha;

# privado
def get_series_down_ficha(ficha):
    logger.debug("Estamos en get_series_down_ficha")
    down_series_ficha=Descarga.objects.filter(ficha=ficha)
    logger.debug("get_series_down_ficha: {}".format(down_series_ficha))
    return down_series_ficha[0] if down_series_ficha else None




def resultado(request, sResponse):
    var = 'Muchas gracias'
    return render(request, 'calendarioTest/resultado.html', {'var':var})    