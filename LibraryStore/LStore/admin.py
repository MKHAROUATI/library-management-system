from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(DeletedReservation)




@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer', 'user', 'display_books', 'created_at', 'updated_at']
    exclude = ('user',)  # Exclude 'user' field from the admin form

    def display_books(self, obj):
        return ", ".join([book.title for book in obj.book.all()])
    display_books.short_description = 'Books'

    def save_model(self, request, obj, form, change):
        # Set the user field to the currently logged-in user
        if hasattr(request, 'user') and request.user.is_authenticated:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def delete_queryset(self, request, queryset):
        # Call the custom delete method on each instance in the queryset
        for obj in queryset:
            obj.delete()

