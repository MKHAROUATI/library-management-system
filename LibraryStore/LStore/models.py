from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.forms import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
class Book(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    author = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False, editable=False)
    book_category = models.ManyToManyField(Category, related_name='categories')
    quantity = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='uploads/', null=False, blank=False)
    language = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.status = self.quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} --- {self.quantity}"
    

class Customer(models.Model):
    full_name = models.CharField(max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=50, null=False, blank=False)
    grade = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name




    


class DeletedReservation(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (deleted)"




class Reservation(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, *args, **kwargs):
        # Create a DeletedReservation record before deleting
        deleted_reservation = DeletedReservation(
            name=self.name,
            customer=self.customer,
            user=self.user,
            created_at=self.created_at,
        )
        deleted_reservation.save()

        # Add associated books to the DeletedReservation using set()
        deleted_reservation.book.set(self.book.all())

    

        # Increment the quantity for each book when the reservation is deleted
        for b in self.book.all():
            b.quantity += 1
            b.save()

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"



