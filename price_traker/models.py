from django.db import models

# Create your models here.
class Price_Tracker_Model(models.Model):
    amazone_product_url = models.URLField(max_length=400,unique=True)
    amazone_product_price = models.IntegerField()
    amazone_product_title = models.CharField(max_length=400)
    my_price = models.IntegerField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.amazone_product_title[:75]
    