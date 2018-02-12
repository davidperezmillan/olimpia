import logging


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .models import Ficha, Capitulo, Document, Descarga

from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage

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
        slope_series_ficha = get_series_slope_ficha(ficha)
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
    slope_series_ficha = get_series_slope_ficha(ficha)
    logger.debug("Ficha {}, Capitulos {}".format(ficha, slope_series_ficha))
    down_series_ficha = get_series_down_ficha(ficha)
    return render(request, 'hoor/pendientes/ficha.html',{'ficha': ficha, 'slope_series_ficha':slope_series_ficha, 'down_series_ficha':down_series_ficha})
    

@login_required(login_url='/accounts/login/')
def visto(request, visto_id):
    visto = get_object_or_404(Capitulo, pk=visto_id)
    visto.visto=True
    visto.save()
    return redirect('ver_ficha',visto.ficha.id)
    


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



# Lanzamos processos
@login_required(login_url='/accounts/login/')
def launch_unique(request, ficha_id):
    ficha = get_object_or_404(Ficha, pk=ficha_id)
    torrentservers = TorrentServers.objects.filter(author=request.user)

    try:
        torrent_found = {}
        launcher = AirTrapLauncher(torrentservers)
        torrent_found, torrent_added, errors = launcher.execute([serie])
        logger.debug("Torrent_found : {}".format(torrent_found))
        logger.debug("torrent_added : {}".format(torrent_added))
        context = {'torrent_found': torrent_found, 'torrent_added': torrent_added, 'serie':serie, 'errors_messages':errors}
        receivers = merc.management.commands.commands_utils.utilgetreceivers(request.user)
        merc.at.hilos.utiles.sendTelegramListAdded(torrent_added, serie=serie, user=request.user, receivers=receivers)
    except Exception, e:
        return render(request, 'merc/torrent/list.html', {'serie':serie,'errors_messages':e})
        
    return render(request, 'merc/torrent/list.html', context)

    
   
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

    
def get_series_slope_ficha(ficha):
    slope_series_ficha= Capitulo.objects.filter(ficha=ficha).filter(visto=False).order_by('capitulo')
    logger.debug("captitulos pendientes : {}".format(slope_series_ficha))
    return slope_series_ficha;

def get_series_down_ficha(ficha):
    down_series_ficha=Descarga.objects.filter(ficha=ficha)
    return down_series_ficha[0] if down_series_ficha else None



def resultado(request, sResponse):
    var = 'Muchas gracias'
    return render(request, 'calendarioTest/resultado.html', {'var':var})    