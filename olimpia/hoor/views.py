#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
from .subviews.views_descargas import *
from .subviews.views_ficha import *
from .subviews.views_utiles import *



@login_required(login_url='/accounts/login/')
def index(request):
    logger.debug("Estamos en index")
    logger.debug("user {}, groups {}".format(request.user, request.user.groups.all()))
    return render(request, 'hoor/pendientes/list.html',
        {'slope_series': get_series_slope(request.user, 1), 
        'slope_series_session': get_session_slope(request.user, 2),})



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


