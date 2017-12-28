import logging


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

# Create your views here.
from .models import Series, TorrentServers, Plugins, TelegramChatIds,TransmissionReceivers
from .forms import SeriesForm, TorrentServersForm, SeriesFindForm, TelegramSendForm
from merc.at.airtrapLauncher import AirTrapLauncher

import merc.at.hilos.utiles
import merc.management.commands.commands_utils

# Get an instance of a logger
logger = logging.getLogger(__name__)


def portada(request):
    return redirect('list')



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
            receivers = merc.management.commands.commands_utils.utilgetreceivers(request.user)
            merc.at.hilos.utiles.sendTelegram(mensaje="Se ha anadido una nueva serie {0} [{1}]".format(serie.nombre, serie.quality),user=request.user, receivers=receivers)
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
            torrentserver = form.save(commit=True)
            torrentserver.author = request.user
            torrentserver.save()
            receivers = merc.management.commands.commands_utils.utilgetreceivers(request.user)
            merc.at.hilos.utiles.sendTelegram(mensaje="Se ha anadido una nueva Servidor Torrent {0}:{1}".format(torrentserver.host, torrentserver.port),user=request.user, receivers=receivers)
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
            torrentserver = form.save(commit=True)
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




# Lanzamos processos
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
        receivers = merc.management.commands.commands_utils.utilgetreceivers(request.user)
        merc.at.hilos.utiles.sendTelegramListAdded(torrent_added, series=serie, request.user, receivers=receivers)
    except Exception, e:
        return render(request, 'merc/torrent/list.html', {'serie':serie,'errors_messages':e})
        
    return render(request, 'merc/torrent/list.html', context)
    
@login_required(login_url='/accounts/login/')
def launch_all(request):
    
    series_update = Series.objects.filter(author=request.user).filter(skipped=False)
    logger.debug('series_update: {}'.format(series_update))
    torrentservers = TorrentServers.objects.filter(author=request.user)
    logger.debug('torrentservers: {}'.format(torrentservers))
    
    receivers = merc.management.commands.commands_utils.utilgetreceivers(request.user)
    try:
        merc.at.hilos.utiles.findAndDestroy(series_update, torrentservers, user=request.user, receivers=receivers)
    except Exception, e:
        strError = "Se ha produccido un error en el proceso del mercenario"
        logger.error(e)
        merc.at.hilos.utiles.sendTelegram(mensaje=strError, user=request.user, receivers=receivers )
        
    context = {}
    return render(request, 'merc/portada.html', context)

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
                    try:
                        logger.info("Intentamos {} grabar la serie {}:{}".format(to_saved,serie_extreme.nombre, serie_extreme.quality))
                        serie_extreme.author = request.user
                        serie_extreme.save()
                        context.update({"to_saved":to_saved,'serie':serie_extreme})
                    except IntegrityError, e:
                        serie_no_update = Series.objects.filter(nombre=serie_extreme.nombre).filter(quality=serie_extreme.quality).filter(author=request.user)[0]
                        logger.error(e.message)
                        context.update({"to_saved":to_saved,'serie':serie_no_update})
                        raise Exception("La serie {} : {} para {} puede que ya este en la base de datos".format(serie_no_update.nombre, serie_no_update.quality, serie_no_update.author))
                
                receivers = merc.management.commands.commands_utils.utilgetreceivers(request.user) 
                merc.at.hilos.utiles.sendTelegramListAdded(torrent_added, serie=serie_extreme, user=request.user, receivers=receivers)
            except Exception, e:
                logger.error(e)
                context.update({'errors_messages':e})
            return render(request, 'merc/torrent/list.html', context)

    else:
        form = SeriesFindForm()
    return render(request, 'merc/series/detail_extreme.html',{'form': form})
    
    


@login_required(login_url='/accounts/login/')
def organize(request):
    
    torrentservers = TorrentServers.objects.filter(author=request.user)
    context = {}
    try:
        launcher = AirTrapLauncher(torrentservers)
        errors = launcher.organize()
    except Exception, e:
        logger.error(e)
        context.update({'errors_messages':errors})
    
    # TODO
    return redirect('list')





@login_required(login_url='/accounts/login/')
def telegramSend(request):
    
    form = TelegramSendForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            logger.info("{form}".format(form=form))
            from merc.at.service.telegramHandler import ReceiverTelegram
            msg = form['msg'].value()
            username = form['receiver'].value()
            fullname = merc.management.commands.commands_utils.getAndBuildFullnames(form['receiver'].value())
            group = form['receiver'].value()
            logger.info("{fullnames}{groups}{usernames}".format(fullnames=[fullname], groups=[group], usernames=[username]))
            receivers = ReceiverTelegram(fullnames=[fullname], groups=[group], usernames=[username])
            merc.at.hilos.utiles.sendTelegram(mensaje=msg, user=request.user, receivers=receivers)
    else:
        form = TelegramSendForm()
    return render(request, 'merc/telegram/detail.html',{'form': form})
    




