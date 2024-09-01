from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.sessions.models import Session
import datetime

# Create your models here.
class blog(models.Model):

    content= models.TextField()
    title= models.CharField(max_length=122, null=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='images/')

    def __str__(self):
        return self.title

class BookingForm(models.Model):
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    
    PACKAGES = (
        ('Couple Pack','Couple Pack'),
        ('Family Pack','Family Pack'),
        ('Custom Pack','Custom Pack'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    age = models.IntegerField(default=5)
    phone_number = models.CharField(max_length=12)
    country = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER)
    packs = models.CharField(max_length=11,choices=PACKAGES, default='')
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return str((self.user)) + ' - ' + str((self.phone_number))

class Category(models.Model):
    categoryName = models.CharField(max_length=20)

    def __str__(self):
        return self.categoryName

class Product(models.Model):
    productTitle = models.CharField(max_length=120)
    productDisp = models.ImageField(default='')
    productDesc = models.TextField()
    productPrice = models.IntegerField(default=200)
    productOffer = models.IntegerField(null=True, blank=True)
    productCategory = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name='cat')

    def __str__(self):
        return self.productTitle

    @staticmethod
    def getProductByID(ids):
        return Product.objects.filter(id__in = ids)

class FeaturedProduct(models.Model):
    featuredProduct = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')

    def __str__(self):
        return self.featuredProduct.productTitle

class order(models.Model):
    Customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='producted')
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    completed = models.BooleanField(default=False)
    readAndReturn = models.BooleanField(default=False, name="readAndReturn")
    returnDate = models.DateField(blank=True, null=True, name="returnDate")

    def placeOrder(self):
        return self.save()

    def __str__(self):
        c=self.Customer
        p=self.product
        return (('%s' % c)  + ' : ' + ('%s' % p))

    def getCustomerId(Customer_id):
        return order.objects.filter(Customer=Customer_id)

class NewsCategory(models.Model):
    category_news = (
        # ('News','News'),
        ('New Releases','New Releases'),
        ('Authors Corner','Authors Corner'),
        ('Events','Events'),
        ('Interview','Interview')
    )
    categoryTitle = models.CharField(max_length=20, choices=category_news)

    def __str__(self):
        return self.categoryTitle

class News(models.Model):
    newsTitle = models.CharField(max_length=120)
    newsContent = models.TextField(default='')
    created = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='images/')
    Category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, blank=True, null=True, related_name='category')

    def __str__(self):
        return self.newsTitle

class Partners(models.Model):
    Partnername = models.CharField(max_length=30)
    Partnerimage = models.FileField(upload_to='images/')
    Partnerlink = models.URLField(default='')

    def __str__(self):
        return self.Partnername
    
class Donate(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=254)
    address = models.TextField(default='')
    comment = models.TextField(default='')
    amount = models.PositiveIntegerField(default=50)

    def __str__(self):
        return self.fname

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    subject = models.TextField(max_length=54)
    message = models.TextField(max_length=254)
    
    def __str__(self):
        return self.name

class Statistic(models.Model):
    name = models.CharField(max_length=20)
    count = models.IntegerField(default=1)

    def __str__(self):
        return (str(self.name) + ' - ' + str(self.count))