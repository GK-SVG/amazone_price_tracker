from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Price_Tracker_Model(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amazone_product_url = models.URLField(max_length=400,unique=True)
    amazone_product_price = models.DecimalField(decimal_places=2,max_digits=6)
    amazone_product_title = models.CharField(max_length=400)
    my_price = models.DecimalField(decimal_places=2,max_digits=6)
    product_img = models.URLField(max_length=400)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.amazone_product_title[:75]
    