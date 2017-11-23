
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required

from .models import Series
from .forms import SeriesForm

# def login(request):
#     context = {}
#     return render(request, 'mercurio/login.html', context)

@login_required(login_url='/mercurio/accounts/login/')
def portada(request):
    latest_series_update = Series.objects.order_by('-ultima')
    context = {'latest_series_update': latest_series_update}
    return render(request, 'mercurio/portada.html', context)

@login_required(login_url='/mercurio/accounts/login/')
def control(request):
    
    form = SeriesForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            serie = form.save(commit=False)
            serie.save()
            __sendTelegram(serie)
            return redirect('portada')
    else:
        form = SeriesForm()
    return render(request, 'mercurio/detail.html',{'form': form})

    
@login_required(login_url='/mercurio/accounts/login/')
def control_edit(request, serie_id):
    serie = get_object_or_404(Series, pk=serie_id)
    if request.method == "POST":
        form = SeriesForm(request.POST, instance=serie)
        if form.is_valid():
            serie = form.save(commit=False)
            serie.save()
            return redirect('portada')
    else:
        form = SeriesForm(instance=serie)
    return render(request, 'mercurio/detail.html',{'form': form, 'serie': serie})


@login_required(login_url='/mercurio/accounts/login/')
def control_delete(request, serie_id):
    serie = get_object_or_404(Series, pk=serie_id)
    p = Series.objects.get(pk=serie_id)
    p.delete()
    return redirect('portada')



def __sendTelegram(serie):
    '''
    Y si anadimos un envio de Telegram cuando se anade una serie
    '''
    
    gth = GenThread(args=(serie), kwargs={})
    gth.start()
    



import threading
class GenThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        return
    def run(self):
        
        nombre=self.args.nombre #Existe siempre
        quality=self.args.quality #Existe siempre
        
        import sys, os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        RUTA = os.path.join(BASE_DIR, '../airtrap')
        sys.path.insert(0,RUTA)
        from handler.services.telegramHandler import TelegramNotifier, ConfigTelegramBean
        
        clazz = TelegramNotifier()
        config = ConfigTelegramBean(token = '135486382:AAFb4fhTGDfy42FzO77HAoxPD6F0PLBGx2Y', fullnames = [("David","Perez Millan")])
        clazz.notify("Mercury Advises", "se ha anadido una nueva serie {0} [{1}]".format(nombre, quality), config)
        return


# @login_required(login_url='/mercurio/accounts/login/')
# def detail(request, serie_id):
#     serie = get_object_or_404(Series, pk=serie_id)
#     return render(request, 'mercurio/detail.html', {'serie': serie})