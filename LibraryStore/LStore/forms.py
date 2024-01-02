from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'description', 'book_category', 'quantity', 'image', 'language']
        
        widgets = {
            'book_category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['full_name', 'phone_number', 'grade', 'email']
        
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),  # Assuming grade is a single-line text input
            'email': forms.EmailInput(attrs={'class': 'form-control'}),  # Assuming email is an email field
        }


class ReservationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        books_in_cart = kwargs.pop('books_in_cart', [])
        super(ReservationForm, self).__init__(*args, **kwargs)

        # Get available books from the cart and the database
        available_books_from_cart = Book.objects.filter(id__in=books_in_cart)
        available_books_from_db = Book.objects.exclude(id__in=books_in_cart)

        # Combine the two sets of available books
        available_books = available_books_from_cart | available_books_from_db

        self.fields['book'].queryset = available_books
        self.fields['book'].initial = available_books_from_cart

    class Meta:
        model = Reservation
        fields = ['name', 'customer', 'book']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'book': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
      
        }

    
    

 

