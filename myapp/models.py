from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.
class Code(models.Model):
    code = models.CharField(max_length=5,blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.code
    

    def save(self, *args,**kwargs):
        num_list = [num for num in range(10)]
        code_item = ""
        for i in range(5):
            num = random.choice(num_list)
            code_item+=str(num)
        self.code = code_item
        super().save(*args,**kwargs)


class MailValid(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    mail_valid = models.BooleanField(default=False)

class Links(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Link")
    title = models.CharField(max_length=300)
    url = models.URLField(max_length=500)
    tags = models.CharField(max_length=200)
    public = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:50]
        
