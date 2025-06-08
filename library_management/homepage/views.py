from django.contrib import messages
from django.shortcuts import render,redirect
from datetime import datetime
from .models import Book, Member   

# Homepage View
def index(request):
    return render(request, 'homepage/index.html', {'now': datetime.now()})

# Member Registration View
def add_members(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        joined_date = request.POST.get('joined_date')

        Member.objects.create(
            name=name,
            email=email,
            joined_date=joined_date
        )

        return render(request, 'homepage/members.html', {
            'message': 'You are now a member of this library.',
            'members': Member.objects.all()
        })

    return render(request, 'homepage/form.html')  # Form to add a member

# View Members
def view_members(request):
    members = Member.objects.all()
    return render(request, 'homepage/members.html', {'members': members})

# View Books
def view_books(request):
    books = Book.objects.all()
    return render(request, 'homepage/viewbooks.html', {'books': books})

# Borrow Book
def borrow(request):
    books = Book.objects.all()
    members = Member.objects.all()

    if request.method == 'POST':
        # You can add logic to store the borrow action if you have a Borrow model
        selected_book = request.POST.get('book')
        selected_member = request.POST.get('member')
        message = f"Member ID {selected_member} borrowed Book ID {selected_book}."
        return render(request, 'homepage/borrow.html', {
            'books': books,
            'members': members,
            'message': message
        })

    return render(request, 'homepage/borrow.html', {'books': books, 'members': members})
def addbooks(request):
    if request.method == 'POST':
        book_name = request.POST.get('title')
        author_name = request.POST.get('author')
        ISBN = request.POST.get('isbn')
        date_of_publish=request.POST.get('date_of_publish')
        available = request.POST.get('available') == 'on'  # Checkbox handling

        Book.objects.create(
            book_name=book_name,
            author_name=author_name,
            ISBN=ISBN,
            date_of_publish=date_of_publish,
            available=available
        )
        messages.success(request,'Book added successfully!')
        return redirect("view_book")
    return render(request, 'homepage/addbooks.html')