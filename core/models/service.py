from django.db import models

from core.models.auth import UserDoctor


class Service(models.Model):
    name = models.CharField(max_length=123)
    info = models.TextField()
    icon = models.ImageField(upload_to='service')

    class Meta:
        verbose_name_plural = '2. Servislar'
        verbose_name = "Servis"

    def __str__(self):
        return self.name

class Price(models.Model):
    doc = models.ForeignKey(UserDoctor, on_delete=models.CASCADE,related_name='service_prices',limit_choices_to={"user_type":3})
    service = models.ForeignKey(Service,on_delete=models.CASCADE)
    price = models.CharField(max_length=123,default='50 000 UZS')
    pr = models.IntegerField(editable=False,null=True,blank=True)

    def __str__(self):
        return f"{self.doc.name} {self.service.name} {self.price}"

    def save(self,*args,**kwargs):
        pr = self.price.replace(" ","")
        for i in ['uzs','usd','$','rub']:
            pr = pr.lower().replace(i, "")
        self.pr = int(pr)
        return super(Price,self).save(*args,**kwargs)

    class Meta:
        verbose_name_plural = '3. Narxlar '
        verbose_name = "Narx"

