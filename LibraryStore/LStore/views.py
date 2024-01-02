from io import BytesIO
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from LStore.forms import BookForm, CategoryForm, CustomerForm, ReservationForm
from LibraryStore import settings
from .models import *
from django.core.mail import send_mail
from django.template.loader import get_template
from xhtml2pdf import pisa


#============================================================HOME===================================

@login_required(login_url='login')
def home(request):
    books = Book.objects.all()
    return render(request,'home.html', {"books": books})

#==================================================BOOK==================================================

@login_required(login_url='login')
def book(request,pk):
    book = Book.objects.get(id=pk)
    return render(request,'book/book.html', {"book": book})

def book_table(request):
    books = Book.objects.all()
    return render(request,'book/book_table.html', {"books": books})

@login_required(login_url='login')
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('book', pk=book.pk)
    else:
        form = BookForm()
    return render(request,'book/create_book.html',{"form":form})

@login_required(login_url='login')
def delete_book(request,pk):
    book = Book.objects.get(id=pk)
    book.delete()
    return redirect('home')

@login_required(login_url='login')
def search_book(request):
    if request.method == 'POST':
        search_term = str(request.POST.get('search', ''))
        search_by = int(request.POST.get('search_by', ''))  # Convert to integer
        if search_term != "" and search_by != 0:
            if search_by == 1:
                books = Book.objects.filter(name__icontains=search_term)
                return render(request, 'home.html',
                              {'books': books, 'search_term': search_term, 'search_by': search_by})

            elif search_by == 2:
                books = Book.objects.filter(author__icontains=search_term)
                return render(request, 'home.html',
                              {'books': books, 'search_term': search_term, 'search_by': search_by})

            else:
                books = Book.objects.filter(book_category__name__icontains=search_term)
                return render(request, 'home.html',
                              {'books': books, 'search_term': search_term, 'search_by': search_by})
        else:
            messages.error(request, ' ): Empty Search by or Empty Search Input')
            return redirect('home')
    else:
        return redirect('home')

@login_required(login_url='login')
def edit_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book', pk=pk)  
    else:
        form = BookForm(instance=book)
    return render(request, 'book/edit_book.html', {'form': form, 'book': book})



#============================================================CUSTOMER======================================        

@login_required(login_url='login')
def customer(request):
    customers = Customer.objects.all()
    return render(request,'customer/customer.html', {"customers": customers})

@login_required(login_url='login')
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer')
    else:
        form = CustomerForm()
    return render(request,'customer/create_customer.html',{"form":form})

@login_required(login_url='login')
def edit_customer(request,pk):
    customer = get_object_or_404(Customer, id=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer')
    else:
        form = CustomerForm(instance=customer)
    return render(request,'customer/edit_customer.html',{"form":form,"customer": customer})

@login_required(login_url='login')
def delete_customer(request,pk):
    customer = Customer.objects.get(id=pk)
    customer.delete()
    return redirect('customer')

#================================================RESERVATIONS=================================================


@login_required(login_url='login')
def reservation(request):
    reservations = Reservation.objects.all()
    return render(request,'reservation/reservation.html', {"reservations": reservations})

@login_required(login_url='login')
def add_reservation(request):
    cart = request.session.get('cart', [])
    if cart:

        if request.method == 'POST':
            form = ReservationForm(request.POST,books_in_cart=cart)
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.user = request.user 
                request.session['cart'] = []
                reservation.save()  # Save the reservation first
                
                for available_book in form.cleaned_data['book']:
                    if available_book.quantity > 0:
                        reservation.book.add(available_book)  # Add the book to the reservation
                        available_book.quantity -= 1
                        available_book.save()
                    else:
                        messages.error(request, 'Choose a book')
                        return redirect('reservation')

                messages.success(request, 'Reservation added successfully!')
                return redirect('reservation')
        else:
            form = ReservationForm(books_in_cart=cart)

        return render(request, 'reservation/add_reservation.html', {"form": form,"books":cart})
    else:
        if request.method == 'POST':
            form = ReservationForm(request.POST)
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.user = request.user 
                reservation.save()  # Save the reservation first
                
                for available_book in form.cleaned_data['book']:
                    if available_book.quantity > 0:
                        reservation.book.add(available_book)  # Add the book to the reservation
                        available_book.quantity -= 1
                        available_book.save()
                    else:
                        messages.error(request, 'Choose a book')
                        return redirect('reservation')

                messages.success(request, 'Reservation added successfully!')
                return redirect('reservation')
        else:
            form = ReservationForm()

        return render(request, 'reservation/add_reservation.html', {"form": form})



@login_required(login_url='login')
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            selected_books = cleaned_data.get('book')
            existing_books = reservation.book.all()

            # Check book quantities before making changes
            for book in selected_books:
                if book.quantity <= 0 and book not in existing_books:
                    messages.error(request, f"Quantity for '{book.name}' is insufficient.")
                    return redirect('edit_reservation', pk=pk)

            # Increment quantity for books in the instance but not in the form
            for existing_book in existing_books:
                if existing_book not in selected_books:
                    existing_book.quantity += 1
                    existing_book.save()

                else:
                    messages.success(request,'you are selecting the same book')
                    redirect('reservation')

            # Decrement quantity for books in the form but not in the instance
            for book in selected_books:
                if not reservation.id or (reservation.id and book not in reservation.book.all()):
                    if book.quantity > 0:
                        book.quantity -= 1
                        book.save()

            # Save the reservation and update ManyToManyField
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            form.save()

            return redirect('reservation')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservation/edit_reservation.html', {"form": form, "reservation": reservation})


@login_required(login_url='login')
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    reservation.delete()

    return redirect('reservation')

#======================================================================DELETED RESERVATIONS==========================

@login_required(login_url='login')
def deleted_reservation(request):
    deleted_reservations = DeletedReservation.objects.all()
    return render(request,'reservation/deleted_reservation.html', {"deleted_reservations": deleted_reservations})   


@login_required(login_url='login')
def delete_deletedReservation(request, pk):
    deleted_reservation = get_object_or_404(DeletedReservation, id=pk)
    deleted_reservation.delete()

    return redirect('deleted_reservation')
#=========================================================CATEGORY==================================================


@login_required(login_url='login')
def category(request):
    categories = Category.objects.all()
    return render(request,'category/category.html', {"categories": categories})

@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save() # Save the reservation first
            messages.success(request, 'category added successfully!')
            return redirect('category')
    else:
        form = CategoryForm()

    return render(request, 'category/add_category.html', {"form": form})


@login_required(login_url='login')
def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,'category Updated successfully!')
            return redirect('category')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'category/edit_category.html', {"form": form, "category": category})


@login_required(login_url='login')
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    category.delete()
    messages.success(request,f'{category.name} category Deleted successfully!')
    return redirect('category')



#=========================================================ADD TO CART===============================================


def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    if book:
        cart = request.session.get('cart', [])
        if book_id not in cart:
            cart.append(book_id)
        else:
            messages.error(request,'This Book is already on the Cart')
        request.session['cart'] = cart
        return redirect('home')
    else:
        messages.error(request,'this not a valid book')
        return redirect('home')

def delete_from_cart(request, book_id):
    cart = request.session.get('cart', [])
    if book_id in cart:
        cart.remove(book_id)
        request.session['cart'] = cart
    return redirect('view_cart')  

def view_cart(request):
    cart = request.session.get('cart', [])
    books = Book.objects.filter(id__in=cart)
    return render(request, 'cart/add_to_cart.html', {'books': books})

#=========================================================AUTH SYSTEM===============================================


def logout_form(request):
    logout(request) 
    return redirect('login')  


def login_form(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Sending email
            subject = f'Hello, {username}'
            message = 'Discover the Latest Books'
            from_email = settings.EMAIL_HOST_USER  # Use the default email specified in settings
            recipient_list = [user.email]

            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception as e:
                # Handle email sending errors
                print(f"Error sending email: {e}")

            messages.success(request, 'You logged in successfully.')
            return redirect('home')  # Replace 'home' with the name of your home URL pattern
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')

    return render(request, 'login.html')



#=========================================================Print pdf==================================================

def pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    # Set encoding to 'utf-8' and use a font that supports French characters
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='utf-8')
    if not pdf.err:
        return result.getvalue()
    return None

#==============================================================================

def pdf_reservation(request, pk, *args, **kwargs):
    if isinstance(pk, dict):
        reservation_id = pk.get('id')
    else:
        reservation_id = pk

    # Ensure reservation_id is defined
    if reservation_id is None:
        raise Http404("Reservation ID not provided or invalid.")

    # Retrieve the Reservation object by ID
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation_dict = {
               "name" : reservation.name,
               "customer" : reservation.customer,
               "user" : reservation.user,
               "books" : reservation.book,
               "created_at" : reservation.created_at
    }
    
    pdf_content = pdf('reservation/pdf.html', reservation_dict)
    
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        filename = "Reservation_%s.pdf" %("12341231")
        response['Content-Disposition'] = f'inline; filename="{filename}"'

        return response
    else:
        return HttpResponse("Error generating PDF", status=500)
    



def pdf_deleted_reservation(request, pk, *args, **kwargs):
    if isinstance(pk, dict):
        reservation_id = pk.get('id')
    else:
        reservation_id = pk

    # Ensure reservation_id is defined
    if reservation_id is None:
        raise Http404("Reservation ID not provided or invalid.")

    # Retrieve the Reservation object by ID
    reservation = get_object_or_404(DeletedReservation, id=reservation_id)
    reservation_dict = {
               "name" : reservation.name,
               "customer" : reservation.customer,
               "user" : reservation.user,
               "books" : reservation.book,
               "created_at" : reservation.created_at
    }
    
    pdf_content = pdf('reservation/pdf.html', reservation_dict)
    
    if pdf_content:
        response = HttpResponse(pdf_content, content_type='application/pdf')
        filename = "Reservation_%s.pdf" %("12341231")
        response['Content-Disposition'] = f'inline; filename="{filename}"'

        return response
    else:
        return HttpResponse("Error generating PDF", status=500)