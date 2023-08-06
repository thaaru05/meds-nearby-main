from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
class PersonalDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    age=models.IntegerField(default=18,)
    B_GROUPS= [
    ("O+ve", "O+ve"),
    ("A+ve", "A+ve"),
    ("B+ve", "B+ve"),
    ("AB+ve", "AB+ve"),
    ("O-ve", "O-ve"),
    ("A-ve", "A-ve"),
    ("B-ve", "B-ve"),
    ("AB-ve", "AB-ve"),
    ]
    blood_group=models.CharField(max_length=6
                                 ,choices=B_GROUPS)
    address=models.TextField(null=True)
    phone_no=models.CharField(max_length=10,null=True)
    def __str__(self):
        return f'{ self.user.username } profile'

    '''def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img=Image.open(self.profile_image.path)
        if img.height>200 or img.width > 200:
            output_size=(200,200)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)'''

