Library Management System Readme
Overview
The Library Management System is a Django-based web application designed to manage a library's book inventory, customer information, and reservations. The system provides a user-friendly interface for library administrators to efficiently handle book transactions, track inventory, and manage customer data.

Features
Book Management:

Add, edit, and delete books in the library inventory.
Assign books to different categories.
Track the quantity of each book and its availability status.
Category Management:

Create and manage book categories with names and optional descriptions.
Customer Management:

Maintain a database of customers with their full name, phone number, grade, and email.
Ensure unique email addresses for each customer.
Reservation System:

Allow customers to reserve books.
Track reservations with details such as the customer, reserved books, and reservation dates.
Automatically update the book quantity and availability status when reservations are made or canceled.
Deleted Reservation History:

Keep a record of deleted reservations in a separate history table.
Include details like the customer, user, reserved books, and deletion date.
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your_username/library-management-system.git
cd library-management-system
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Apply Migrations:

bash
Copy code
python manage.py migrate
Create a Superuser:

bash
Copy code
python manage.py createsuperuser
Run the Development Server:

bash
Copy code
python manage.py runserver
Access the Application:
Open your web browser and go to http://localhost:8000/admin/ to log in with the superuser credentials and manage the application.

Usage
Admin Dashboard:

Log in to the admin dashboard using the superuser credentials.
Manage books, categories, customers, reservations, and deleted reservations.
Book Management:

Add new books with details like name, author, description, quantity, image, language, and category.
Edit or delete existing books.
Category Management:

Create, edit, or delete book categories.
Customer Management:

Add new customers with details like full name, phone number, grade, and email.
Ensure each customer has a unique email address.
Reservation System:

Create reservations for customers, specifying the reserved books.
View and manage existing reservations.
Deleting a reservation updates the book quantity and availability status.
Deleted Reservation History:

View a history of deleted reservations, including details about the customer, user, reserved books, and deletion date.
Contributing
If you would like to contribute to the development of this project, please follow the standard Git workflow:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes and push the branch to your fork.
Submit a pull request with a clear description of your changes.
License
This Library Management System is licensed under the MIT License.

Feel free to reach out for any questions or issues related to the project. Happy coding!