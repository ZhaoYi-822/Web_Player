from django.db import models

# Create your models here.
class video_info(models.Model):
   name=models.CharField(max_length=255)
   title=models.CharField(max_length=25,null=True)
   intro=models.CharField(max_length=255,null=True)
   num_frames=models.DecimalField(max_digits=10,decimal_places=2)
   bit_rate=models.DecimalField(max_digits=10,decimal_places=2)
   fps=models.DecimalField(max_digits=10,decimal_places=2)
   size=models.DecimalField(max_digits=10,decimal_places=2)
   duration=models.DecimalField(max_digits=10,decimal_places=2)
   img_url=models.CharField(max_length=255)
   width=models.DecimalField(max_digits=10,null=True,decimal_places=0)
   height=models.DecimalField(max_digits=10,null=True,decimal_places=0)
