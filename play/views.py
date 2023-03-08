import os
import random
import time

import cv2
import numpy as np
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from play.models import video_info
# Create your views here.
from django.shortcuts import render
import ffmpeg

from djangoProject1 import settings


def read_frame_by_time(in_file, time):
  out, err = (
    ffmpeg.input(in_file, ss=time)
    .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
    .run(capture_stdout=True)

  )
  return out

def video_upload(request):
  messages=" "
  Filename=time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
  if request.method == 'POST':
    # stream = ffmpeg.input("C:/Users/zhaoy/Desktop/coolPlay-master/test.mp4")
    #
    # ffmpeg.run(stream)
    File = request.FILES.get('hunter',None)

    Title=request.POST.get('title',None)
    Intro = request.POST.get('intro', None)
    if File is None:
      return render(request,'upload.html',{'msg':'没有文件上传'})
    dir = os.path.join(settings.MEDIA_ROOT, Filename+'.mp4')
    destination = open(dir,'wb+')
    for chunk in File.chunks():
      destination.write(chunk)
    stream = ffmpeg.input(dir)
    stream = ffmpeg.output(stream,'C:/Users/zhaoy/Desktop/nginx-1.23.3/hls/video1/'+ Filename + '.m3u8', format='hls', hls_time=10, hls_list_size=0)
    ffmpeg.run(stream)
    destination.close()


    probe = ffmpeg.probe(dir)
    print('source_video_path: {}'.format(dir))
    format = probe['format']
    bit_rate = int(format['bit_rate']) / 1000
    duration = format['duration']
    size = int(format['size']) / 1024 / 1024
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    num_frames = int(video_stream['nb_frames'])
    fps = int(video_stream['r_frame_rate'].split('/')[0]) / int(video_stream['r_frame_rate'].split('/')[1])
    duration = float(video_stream['duration'])
    random_time = random.uniform(0, float(duration))
    out = read_frame_by_time(dir, random_time)
    image_array = np.asarray(bytearray(out), dtype="uint8")
    img_frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    cv2.imwrite('static/img/'+Filename+".png", img_frame)
    img_url=Filename+'.png'
    video_capture = cv2.VideoCapture(dir)
    width = int(video_capture.get(3))
    height = int(video_capture.get(4))

    info=video_info()
    info.name=Filename
    info.num_frames=num_frames
    info.bit_rate=bit_rate
    info.fps=fps
    info.size=size
    info.duration=duration
    info.img_url=img_url
    info.title=Title
    info.intro=Intro
    info.height=height
    info.width=width
    info.save()
    if(int(fps)!=0):
     messages='Sucessful!'
    else:
     messages='Failed!'

  return render(request,'upload.html',{'msg':messages})







def index(request):
  info=video_info.objects.all()



  return render(request, 'index.html',{'info':info})

def play(request):
  id = request.GET.get('id')
  info=video_info.objects.get(name=id)
  return  render(request,'play.html',{'info':info})

