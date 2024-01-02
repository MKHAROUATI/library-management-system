
from django.urls import path
from django.conf.urls.static import static
from LibraryStore import settings
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('login/', views.login_form,name="login"),
    path('logout/', views.logout_form,name="logout"),
    # =================================================BOOK================
    path('book/create_book', views.create_book,name="create_book"),
    path('books/', views.book_table,name="books"),
    path('book/<int:pk>', views.book,name="book"),
    path('book/search', views.search_book,name="search_book"),
    path('book/delete/<int:pk>', views.delete_book,name="delete_book"),
    path('book/edit/<int:pk>', views.edit_book,name="edit_book"),
    #========================================================RESERVATION======
    path('reservations/', views.reservation,name="reservation"),
    path('deleted/reservations/', views.deleted_reservation,name="deleted_reservation"),
    path('backup/reservations/delete/<int:pk>', views.delete_deletedReservation,name="delete_backup"),
    path('add/reservation/', views.add_reservation,name="add_reservation"),
    path('edit/reservation/<int:pk>', views.edit_reservation,name="edit_reservation"),
    path('delete/reservation/<int:pk>', views.delete_reservation,name="delete_reservation"),
    #=====================================================PDF====================================
    path('pdf/reservation/<int:pk>', views.pdf_reservation,name="print_reservation"),
    path('pdf/deleted/reservation/<int:pk>', views.pdf_deleted_reservation,name="print_deleted_reservation"),

    #========================================================Category======
    path('categories/', views.category,name="category"),
    path('add/category/', views.add_category,name="add_category"),
    path('edit/category/<int:pk>', views.edit_category,name="edit_category"),
    path('delete/category/<int:pk>', views.delete_category,name="delete_category"),

    #========================================================CUSTOMER======
    path('customer/', views.customer,name="customer"),
    path('add/customer/', views.add_customer,name="add_customer"),
    path('edit/customer/<int:pk>', views.edit_customer,name="edit_customer"),
    path('delete/customer/<int:pk>', views.delete_customer,name="delete_customer"),

    #========================================================CART======
    path('Cart/', views.view_cart,name="view_cart"),
    path('add/cart/<int:book_id>', views.add_to_cart,name="add_to_cart"),
    path('delete/cart/<int:book_id>', views.delete_from_cart,name="delete_from_cart"),




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)