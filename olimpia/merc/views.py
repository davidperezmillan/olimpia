import logging


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Series, TorrentServers, Plugins
from .forms import SeriesForm, TorrentServersForm, SeriesFindForm
from merc.at.airtrapLauncher import AirTrapLauncher

# Get an instance of a logger
logger = logging.getLogger(__name__)


def portada(request):
    context = {}
    return render(request, 'merc/portada.html', context)




# ## Control, formulario Series
@login_required(login_url='/accounts/login/')
def list(request):
    latest_series_update = Series.objects.filter(author=request.user).order_by('-ultima')
    context = {'latest_series_update': latest_series_update}
    return render(request, 'merc/series/list.html', context)

@login_required(login_url='/accounts/login/')
def control(request):
    
    form = SeriesForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            serie = form.save(commit=False)
            serie.author = request.user
            serie.save()
            __sendTelegram("Se ha anadido una nueva serie {0} [{1}]".format(serie.nombre, serie.quality))
            return redirect('list')
    else:
        form = SeriesForm()
    return render(request, 'merc/series/detail.html',{'form': form})

    
@login_required(login_url='/accounts/login/')
def control_edit(request, serie_id):
    serie = get_object_or_404(Series, pk=serie_id)
    if request.method == "POST":
        form = SeriesForm(request.POST, instance=serie)
        if form.is_valid():
            serie = form.save(commit=False)
            # serie.author = request.user
            serie.save()
            return redirect('list')
    else:
        form = SeriesForm(instance=serie)
    return render(request, 'merc/series/detail.html',{'form': form, 'serie': serie})


@login_required(login_url='/accounts/login/')
def control_delete(request, serie_id):
    serie = get_object_or_404(Series, pk=serie_id)
    p = Series.objects.get(pk=serie_id)
    p.delete()
    return redirect('list')





# ## Control, formulario TorrentServers
@login_required(login_url='/accounts/login/')
def listtorrentservers(request):
    latest_torrentservers_update = TorrentServers.objects.filter(author=request.user)
    context = {'latest_torrentservers_update': latest_torrentservers_update}
    return render(request, 'merc/servers/list.html', context)


@login_required(login_url='/accounts/login/')
def control_torrentservers(request):
    
    form = TorrentServersForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            torrentserver = form.save(commit=False)
            torrentserver.author = request.user
            torrentserver.save()
            __sendTelegram("Se ha anadido una nueva Servidor Torrent {0}:{1}".format(torrentserver.host, torrentserver.port))
            return redirect('listtorrentservers')
    else:
        form = TorrentServersForm()
    return render(request, 'merc/servers/detail.html',{'form': form})

    
@login_required(login_url='/accounts/login/')
def control_edittorrent(request, torrentserver_id):
    torrentserver = get_object_or_404(TorrentServers, pk=torrentserver_id)
    if request.method == "POST":
        form = TorrentServersForm(request.POST, instance=torrentserver)
        if form.is_valid():
            torrentserver = form.save(commit=False)
            # serie.author = request.user
            torrentserver.save()
            return redirect('listtorrentservers')
    else:
        form = TorrentServersForm(instance=torrentserver)
    return render(request, 'merc/servers/detail.html',{'form': form, 'torrentserver': torrentserver})


@login_required(login_url='/accounts/login/')
def control_deletetorrent(request, torrentserver_id):
    torrentserver = get_object_or_404(TorrentServers, pk=torrentserver_id)
    p = TorrentServers.objects.get(pk=torrentserver_id)
    p.delete()
    return redirect('listtorrentservers')





@login_required(login_url='/accounts/login/')
def launch_unique(request, serie_id):
    serie = get_object_or_404(Series, pk=serie_id)
    torrentservers = TorrentServers.objects.filter(author=request.user)

    try:
        torrent_found = {}
        launcher = AirTrapLauncher(torrentservers)
        torrent_found, torrent_added, errors = launcher.execute([serie])
        logger.debug("Torrent_found : {}".format(torrent_found))
        logger.debug("torrent_added : {}".format(torrent_added))
        context = {'torrent_found': torrent_found, 'torrent_added': torrent_added, 'serie':serie, 'errors_messages':errors}
        __sendTelegramListAdded(torrent_added)
    except Exception, e:
        return render(request, 'merc/torrent/list.html', {'serie':serie,'errors_messages':e})
        
    return render(request, 'merc/torrent/list.html', context)
    
    # form = SeriesForm(instance=serie)
    # return render(request, 'merc/detail.html',{'form': form, 'serie': serie})



@login_required(login_url='/accounts/login/')
def launch_all(request):
    
    series_update = Series.objects.filter(author=request.user).filter(skipped=False)
    logger.debug('series_update: {}'.format(series_update))
    torrentservers = TorrentServers.objects.filter(author=request.user)

    try:
        torrent_found = {}
        launcher = AirTrapLauncher(torrentservers)
        torrent_found, torrent_added, errors = launcher.execute(series_update)
        logger.debug("Torrent_found : {}".format(torrent_found))
        logger.debug("torrent_added : {}".format(torrent_added))
        context = {'torrent_found': torrent_found, 'torrent_added': torrent_added, 'errors_messages':errors}
        __sendTelegramListAdded(torrent_added)
    except Exception, e:
        return render(request, 'merc/torrent/list.html', {'errors_messages':e})
        
    return render(request, 'merc/torrent/list.html', context)
    


@login_required(login_url='/accounts/login/')
def launch_extreme(request):
    
    form = SeriesFindForm(request.POST)
    
    if request.method == "POST":
        if form.is_valid():
            serie_extreme = form.save(commit=False)
            torrentservers = TorrentServers.objects.filter(author=request.user)
            try:
                to_saved = form['to_saved'].value()
                logger.info("Ordenamos {} grabar la serie {}:{}".format(to_saved,serie_extreme.nombre, serie_extreme.quality))
                torrent_found = {}
                launcher = AirTrapLauncher(torrentservers)
                torrent_found, torrent_added, errors = launcher.execute([serie_extreme])
                logger.debug("Torrent_found : {}".format(torrent_found))
                logger.debug("torrent_added : {}".format(torrent_added))
                context = {'torrent_found': torrent_found, 'torrent_added': torrent_added, "to_saved":to_saved,'errors_messages':errors, }
                if to_saved:
                    logger.info("Intentamos {} grabar la serie {}:{}".format(to_saved,serie_extreme.nombre, serie_extreme.quality))
                    serie_extreme.author = request.user
                    serie_extreme.save()
                    context.update({"to_saved":to_saved,'serie':serie_extreme})
                __sendTelegramListAdded(torrent_added)
            except Exception, e:
                logger.error(e)
                return render(request, 'merc/torrent/list.html', {'errors_messages':e})
            return render(request, 'merc/torrent/list.html', context)

    else:
        form = SeriesFindForm()
    return render(request, 'merc/series/detail_extreme.html',{'form': form})
    
    




def __sendTelegramListAdded(lrequest):
    
        if lrequest:
            sRequest = "'La trampa del Aire - El Mercenario' ha puesto en cola {0} torrent para su descargas :   \n\r".format(len(lrequest))
            sFinal = "\n\rEspero que lo disfruteis, Gracias por utilizar 'La Trampa del Aire - El Mercenario'"
            sitems = ""
            for item in lrequest:
                sitems = "{0} -- {1} [{2}].  \n\r".format(sitems,item.title, item.episode) 
            sRequest = "{0}{1}{2}".format(sRequest,sitems, sFinal)
        else:
            sRequest = 'Que pena no tenemos nada que enviar .....'
        
        __sendTelegram(lrequest)

    
    



def __sendTelegram(mensaje='Interaccion'):
    '''
    Y si anadimos un envio de Telegram cuando se anade una serie
    '''
    
    gth = GenThread(args=(mensaje), kwargs={})
    gth.start()
    



import threading
class GenThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return
    
    
    
    def run(self):
        import sys, os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        RUTA = os.path.join(BASE_DIR, '../airtrap')
        sys.path.insert(0,RUTA)
        from handler.services.telegramHandler import TelegramNotifier, ConfigTelegramBean
        
        clazz = TelegramNotifier()
        config = ConfigTelegramBean(token = '135486382:AAFb4fhTGDfy42FzO77HAoxPD6F0PLBGx2Y', fullnames = [("David","Perez Millan")])
        clazz.notify(self.args, config)
        return


# @login_required(login_url='/accounts/login/')
# def detail(request, serie_id):
#     serie = get_object_or_404(Series, pk=serie_id)
#     return render(request, 'detail.html', {'serie': serie})