from django.db import models

# Create your models here.
class Book(models.Model):
    book_name=models.CharField(max_length=30)
    ISBN=models.IntegerField(default=0)
    author_name=models.CharField(max_length=30)
    date_of_publish=models.DateField()
    available=models.BooleanField(default=True)
    stock=models.IntegerField(default=1,null=True)

    def __str__(self):
        return f"{self.book_name}"
    
class Member(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(unique=True)
    joined_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
class Borrow(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    Member=models.ForeignKey(Member,on_delete=models.CASCADE)
    borrow_date=models.DateField(auto_now_add=True)
    return_date=models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.book}"

