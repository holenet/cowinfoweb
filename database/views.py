# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mimetypes
import os
import urllib
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.middleware import csrf
from django.shortcuts import render, get_object_or_404

from database.forms import DBFileForm
from database.models import DBFile


@login_required
def db_list(request):
    db_files = DBFile.objects.filter(author=request.user).order_by('-uploaded_at')
    queries = []

    for db_file in db_files:
        queries.append(str(db_file.uploaded_at))

    return JsonResponse(queries, safe=False)


@login_required
def db_upload(request):
    if request.method == 'POST':
        form = DBFileForm(request.POST, request.FILES)
        if form.is_valid():
            db_file = form.save(commit=False)
            db_file.author = request.user
            db_file.save()
            return HttpResponse()
    else:
        response = HttpResponse()
        response.set_cookie('csrftoken', csrf.get_token(request))
        return response
    return HttpResponseBadRequest()


@login_required
def db_download(request, file_id):
    db_file = get_object_or_404(DBFile, pk=file_id, author=request.user)
    file_name = os.path.basename(db_file.db_file.name)
    file_path = os.path.join(settings.MEDIA_ROOT, db_file.db_file.name)
    file_wrapper = FileWrapper(file(file_path, 'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % urllib.quote(file_name.encode('utf-8'))
    return response
