
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Photo,Photoa
from .forms import PhotoForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.core.exceptions import PermissionDenied


import urllib.request
import os
import sys
from django.core.files.base import ContentFile
from django.core.files.base import File
from django.core.files.storage import default_storage #FileSystemStorage
import urllib.request
import re

from TwitterAPI import TwitterAPI,TwitterPager
from TwitterAPI import TwitterRequestError
from TwitterAPI import TwitterConnectionError

def post_list(request):
    
    return render(request, 'blog/post_list.html',)


def photogallary(request):
    if request.method == "POST":
        form = PhotoForm(request.POST)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.published_date = timezone.now()
            post = Photoa.objects.all().filter(name = photo.tag )
            if not post:
                api = TwitterAPI('X2XG271rJPmdxtVVMz1ejtxMZ', 'jvGO68wXnnlC5gw3kWdpqZ7NkQwze2eDOxRFnIjZLQDY2iZ1vO', '998624117602435073-8obGWt14pP19zD5ZtRjdbGuVZ7JTgCg', 'nZVJjHP1w1FZqr245PRcvdrYCpZeH2rKWxmaYsmcXUdLX')
                r = TwitterPager(api, 'search/tweets', {'q':photo.tag, 'count':10})
                list = []
                for item in r.get_iterator(wait=20):
                    try:
                          if 'text' in item:

                              images = item['extended_entities']['media']

                              for image in images:

                                  if image['type'] == 'video':
                                         #imagelink = image['media_url']
                                    for video in image["video_info"]["variants"]:
                                         imagelink = video["url"]
                                         url = imagelink
                                         p = url.split('/')[-1]
                                         l= p.split('?')[0]
                                         q = l.split('.')[-1]
                                         if q == 'mp4':
                                             list.extend(imagelink)
                                             req = urllib.request.Request(url)
                                             resp = urllib.request.urlopen(req)
                                             respData = resp.read()
                                             from django.core.files.base import ContentFile
                                             f2 = ContentFile(respData)
                                             fs = default_storage
                                             filename = fs.save(url.split('/')[-1].split('?')[0],f2)
                                             pob = Photoa()
                                             pob.name = photo.tag
                                             pob.img.save(filename, f2,save=False)
                                             pob.url_img = url
                                             pob.save(True)
                                             photo.save()
                                         

                          elif 'message' in item and item['code'] == 88:
                                 print ('SUSPEND, RATE LIMIT EXCEEDED: %s\n' % item['message'])    
                                 break

                    except KeyError:
                        pass   
                post = Photoa.objects.all().filter(name = photo.tag )        
                return render(request,'blog/display.html',{'list':post})

            list1 = []
            for p in post:
                list1.extend(p.url_img)

            return render(request,'blog/display.html',{'list':post})


    else:
        form = PhotoForm()
    return render(request, 'blog/photosearch.html', {'form': form})   

from django.http import HttpResponse
from .resources import PhotoaResource

def export(request):
    image_resource = PhotoaResource()
    dataset = image_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="image.csv"'
    return response                                    


def comment_remove(request, pk):
    comment = get_object_or_404(Photoa, pk=pk)
    
    name = comment.name
    print("hi")
    comment.delete()
    return redirect('photogallary_after_remove',name = name)

def photogallary_after_remove(request, name):
    post = Photoa.objects.all().filter(name = name )

    return render(request,'blog/display.html',{'list':post})