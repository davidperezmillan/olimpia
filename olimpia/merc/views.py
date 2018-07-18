import logging


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.conf import settings

# Create your views here.
from .models import Series, TorrentServers, Plugins, TelegramChatIds,TransmissionReceivers
from .forms import SeriesForm, TorrentServersForm, SeriesFindForm, TelegramSendForm
from merc.at.airtrapLauncher import AirTrapLauncher
import merc.at.properties.msgproperties as msgproperties

import merc.at.hilos.utiles
import merc.management.commands_utils

# Get an instance of a logger
logger = logging.getLogger(__name__)


# ## Control, formulario Series
@login_required(login_url='/accounts/login/')
def portada(request):
    
    '''
    if request.user.is_superuser:
        latest_series_update = Series.objects.order_by('-ultima')
        slopes_series = Series.objects.filter(skipped=True).order_by('-ultima')
        paussed_series = Series.objects.filter(paussed=True).order_by('-ultima')
    else:
        latest_series_update = Series.objects.filter(author=request.user).order_by('-ultima')
        slopes_series = Series.objects.filter(author=request.user).filter(skipped=True).order_by('-ultima')
        paussed_series = Series.objects.filter(author=request.user).filter(paussed=True).order_by('-ultima')
    '''
    
    if request.user.is_superuser:
        latest_series_update = Series.objects.order_by('-ultima')
    else:
        latest_series_update = Series.objects.filter(author=request.user).order_by('-ultima')
    
    	
    follow_series = []
    paussed_series = []
    slopes_series = []
    for serie in latest_series_update:
        
        if not serie.skipped and not serie.paussed:
            follow_series.append(serie)
        if serie.skipped:
            slopes_series.append(serie)
        elif serie.paussed:
            paussed_series.append(serie)

    
    context = {'follow_series':follow_series,'slopes_series': slopes_series, 'paussed_series': paussed_series,'latest_series_update': latest_series_update}
    context2 = {'s_follow':len(follow_series),'s_slopes': len(slopes_series), 's_paussed': len(paussed_series),'s_latest': len(latest_series_update)}
    context.update(context2)
    return render(request, 'merc/series/index.html', context)
    # return redirect('list')
    



# ## Control, formulario Series
@login_required(login_url='/accounts/login/')
def list(request):
    if request.user.is_superuser:
        latest_series_update = Series.objects.order_by('-ultima')
    else:
        latest_series_update = Series.objects.filter(author=request.user).order_by('-ultima')
    context = {'latest_series_update': latest_series_update}
    return render(request, 'merc/series/list.html', context)

@login_required(login_url='/accounts/login/')
def control(request):
    form = SeriesForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            logger.info("Serie para el usuario {}".format(form))
            serie = form.save(commit=False)
            if not serie.author:
                serie.author = request.user
            serie.save()
            receivers = merc.management.commands_utils.utilgetreceivers(serie.author)
            merc.at.hilos.utiles.sendTelegram(mensaje=msgproperties.MSG_TELEGRAM["new"].format(serie.nombre, serie.quality),user=serie.author, receivers=serie.author)
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
            if not serie.author:
                serie.author = request.user
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
            receivers = merc.management.commands_utils.utilgetreceivers(request.user)
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
        receivers = merc.management.commands_utils.utilgetreceivers(request.user)
        merc.at.hilos.utiles.sendTelegramListAdded(torrent_added, serie=serie, user=request.user, receivers=receivers)
    except Exception, e:
        return render(request, 'merc/torrent/list.html', {'serie':serie,'errors_messages':e})
        
    return render(request, 'merc/torrent/list.html', context)
    
@login_required(login_url='/accounts/login/')
def launch_all(request):
    
    series_update = Series.objects.filter(author=request.user).filter(skipped=False)
    logger.debug('series_update: {}'.format(series_update))
    torrentservers = TorrentServers.objects.filter(author=request.user)
    logger.debug('torrentservers: {}'.format(torrentservers))
    
    receivers = merc.management.commands_utils.utilgetreceivers(request.user)
    try:
        merc.at.hilos.utiles.findAndDestroy(series_update, torrentservers, user=request.user, receivers=receivers)
    except Exception, e:
        strError = "Se ha produccido un error en el proceso del mercenario"
        logger.error(e)
        merc.at.hilos.utiles.sendTelegram(mensaje=strError, user=request.user, receivers=receivers )
        
    context = {}
    return redirect('list')

@login_required(login_url='/accounts/login/')
def launch_extreme(request):
    
    form = SeriesFindForm(request.POST)
    
    if request.method == "POST":
        context = {}
        if form.is_valid():
            serie_extreme = form.save(commit=False)
            torrentservers = TorrentServers.objects.filter(author=request.user)
            try:
                to_saved = form['to_saved'].value()
                logger.info("Ordenamos {} grabar la serie {}:{}".format(to_saved,serie_extreme.nombre, serie_extreme.quality))
                torrent_found = {}
                launcher = AirTrapLauncher(torrentservers)
                torrent_found, torrent_added, errors = launcher.execute([serie_extreme], to_saved=to_saved)
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
                
                receivers = merc.management.commands_utils.utilgetreceivers(request.user) 
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
    
    # torrentservers = TorrentServers.objects.filter(author=request.user)
    # receivers = merc.management.commands_utils.utilgetreceivers(request.user)
    # context = {}
    # try:
    #     launcher = AirTrapLauncher(torrentservers)
    #     errors = launcher.organize()
    #     merc.at.hilos.utiles.sendTelegram("Hemos organizado la libreria", user=request.user, receivers=receivers)
    # except Exception, e:
    #     logger.error(e)
    #     context.update({'errors_messages':errors})
    
    author = request.user
    torrentservers = TorrentServers.objects.filter(author=request.user)
    merc.at.hilos.utiles.organizeProccess(author, None, None, torrentservers)
    
    # TODO
    return redirect('list')






@login_required(login_url='/accounts/login/')
def telegramSend(request):
    
    form = TelegramSendForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            usernames=[]
            fullnames=[]
            groups=[]
            from merc.at.service.telegramHandler import ReceiverTelegram
            logger.info("receiver : {form}".format(form=form['receiver'].value()))
            msg = form['msg'].value()
            rec=None
            if bool(form['receiver'].value()):
                
                if form['receiver'].value()=='ALL':
                    recs = TelegramChatIds.objects.all()
                    for rec in recs:
                        if rec.username:
                            usernames.append(rec.username)
                        if rec.firstname:   
                            fullnames.append((rec.firstname,rec.surname))
                        if rec.group:
                            groups.append(rec.group)
                else:
                    rec = TelegramChatIds.objects.filter(id=form['receiver'].value())[0]
                    if rec.username:
                        usernames.append(rec.username)
                    if rec.firstname:   
                        fullnames.append((rec.firstname,rec.surname))
                    if rec.group:
                        groups.append(rec.group)

            else:
                rec = form['receiverUnique'].value()
                usernames.append(rec)
                fullnames.append(merc.management.commands_utils.getAndBuildFullnames(rec))
                groups.append(rec)
                
            logger.info("Destinatario unico {fullnames}{groups}{usernames}".format(fullnames=fullnames, groups=groups, usernames=usernames))
            receivers = ReceiverTelegram(fullnames=fullnames, groups=groups, usernames=usernames)
            merc.at.hilos.utiles.sendTelegram(mensaje=msg, user=request.user, receivers=receivers)

    else:
        form = TelegramSendForm()
    return render(request, 'merc/telegram/detail.html',{'form': form})

@login_required(login_url='/accounts/login/')
def listPTorrent(request):
    latest_excluidos_update = []
    latest_incluidos_update = []
    
    __getFileWrapper(latest_incluidos_update,'*_WTCHD_INCLUIDOS.dat', 'phub')
    __getFileWrapper(latest_incluidos_update,'*_WTCHD_CLUB_INCLUIDOS.dat','ypclub')
    
    __getFileWrapper(latest_excluidos_update,'*_WTCHD_EXCLUIDOS.dat', 'phub')
    __getFileWrapper(latest_excluidos_update,'*_WTCHD_CLUB_EXCLUIDOS.dat','ypclub')
    
    latest_incluidos_update.sort(key=lambda x: x['title'].upper())
    latest_excluidos_update.sort(key=lambda x: x['title'].upper())
    
    context = {'latest_excluidos_update': latest_excluidos_update,'latest_incluidos_update':latest_incluidos_update}
    return render(request, 'merc/torrent/special.html', context)    
    
    
    
import os.path
import glob
    
def __get_latest_file(path, *paths):
    """Returns the name of the latest (most recent) file 
    of the joined path(s)"""
    fullpath = os.path.join(path, *paths)
    list_of_files = glob.glob(fullpath)  # You may use iglob in Python3
    if not list_of_files:                # I prefer using the negation
        return None                      # because it behaves like a shortcut
    latest_file = max(list_of_files, key=os.path.getctime)
    _, filename = os.path.split(latest_file)
    return filename
    
    
    
    
def __getFileWrapper(latest_update,pattern, origen=""):
    path = os.path.join(settings.BASE_DIR,'../data/olimpia/report')
     # Vamos a coger el ultimo archivo de la carpeta en cuestion
    fname = __get_latest_file(path,pattern)
    if fname:
        logger.info("Archivo origen {}".format(fname))
        fullPathName = os.path.join(path,fname)
        with open(fullPathName) as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
        linesRaw = [x.strip() for x in content]
    
        # mappeamos el objeto 
        logger.info("lineas a mapear {}".format(len(linesRaw)))    
        for line in linesRaw:
            if line:
                # line.split('::')[-1] ### Siempre tiene que estar porque es la ultima
                linea = line.split('::')
                titulo = linea[1] if len(linea) >= 2 else ""
                link = linea[2] if len(linea) >= 2 else ""
                trr =  linea[3] if len(linea) >= 3 else ""
                sCat = linea[-1].replace( "[", "").replace( "]", "").replace(", ",",")
                lDict = {"origen":origen,"title":titulo,"link":link,"cat":sCat,"fch":fname, "trr":trr}
                latest_update.append(lDict)