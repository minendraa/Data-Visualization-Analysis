from django.contrib import messages
from django.shortcuts import render,redirect
from datetime import datetime
from .models import Book, Member,Returnbook   
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'homepage/index.html', {'now': datetime.now()})

@login_required
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

@login_required
def view_members(request):
    members = Member.objects.all()
    return render(request, 'homepage/members.html', {'members': members})

@login_required
def view_books(request):
    books = Book.objects.all()
    return render(request, 'homepage/viewbooks.html', {'books': books})

@login_required
def borrow(request):
    books = Book.objects.all()
    members = Member.objects.all()
    if request.method == 'POST':
        # You can add logic to store the borrow action if you have a Borrow model
        selected_book = request.POST.get('book')
        selected_member = request.POST.get('member')
        for book in books:
            if book.book_name == selected_book:
                book.stock
                if book.stock > 0:
                    book.stock = book.stock-1 
                    book.save()
                    messages.success(request, f"Member {selected_member} borrowed Book ID {selected_book}.")

                else:
                    messages.error(request,f'{selected_book} is out of stock!!') 
                    break
        return render(request, 'homepage/borrow.html', {
            'books': books,
            'members': members,
        })

    return render(request, 'homepage/borrow.html', {'books': books, 'members': members})

@login_required
def returnbook(request):
    members = Member.objects.all()
    
    # Get only books that are currently borrowed (stock < total_copies or some other indicator)
    # This assumes you have a way to track borrowed books. If not, you'll need to modify this.
    borrowed_books = Book.objects.filter(stock__lt=F('total_copies')) if hasattr(Book, 'total_copies') else Book.objects.all()
    
    if request.method == 'POST':
        book_id = request.POST.get('book')
        member_id = request.POST.get('member')
        
        try:
            book = Book.objects.get(id=book_id)
            member = Member.objects.get(id=member_id)
            
            # Increase book stock
            book.stock += 1
            book.save()
            
            # Create return record
            Returnbook.objects.create(
                book=book,
                Member=member,
                return_date=timezone.now().date()
            )
            
            messages.success(request, f"Book '{book.book_name}' returned successfully by {member.name}.")
            return redirect('returnbook')
            
        except Book.DoesNotExist:
            messages.error(request, "Selected book not found!")
        except Member.DoesNotExist:
            messages.error(request, "Selected member not found!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, 'homepage/returnbook.html', {
        'members': members,
        'borrowed_books': borrowed_books
    })

@login_required

def addbooks(request):
    if request.method == 'POST':
        book_name = request.POST.get('title')
        author_name = request.POST.get('author')
        ISBN = request.POST.get('isbn')
        date_of_publish=request.POST.get('date_of_publish')
        available = request.POST.get('available') == 'on'  # Checkbox handling
        stock=request.POST.get('stock')
        
        Book.objects.create(
            book_name=book_name,
            author_name=author_name,
            ISBN=ISBN,
            date_of_publish=date_of_publish,
            available=available,
            stock=stock
        )
        messages.success(request,'Book added successfully!')
        return redirect("view_book")
    return render(request, 'homepage/addbooks.html')

@login_required

def updatebook(request):
    if request.method == 'POST':
        isbn = request.POST.get('ISBN')  # Changed to match form field name
        stock = request.POST.get('stock')

        try:
            # Try to get the book using the ISBN provided
            book = Book.objects.get(ISBN=isbn)

            # Add the new stock to the current stock
            book.stock += int(stock)
            book.save()

            messages.success(request, f'Book "{book.book_name}" updated successfully! New stock: {book.stock}')
            return redirect('update_book')  # Redirect back to the same page to show success message
        except Book.DoesNotExist:
            messages.error(request, f'Book with ISBN {isbn} not found!')
        except ValueError:
            messages.error(request, 'Please enter a valid number for stock')

    return render(request, 'homepage/updatebook.html')

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('index')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'homepage/accounts/login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, 'homepage/accounts/signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'homepage/accounts/signup.html')
        if User.objects.filter(email=email).exists() and email != '':
            messages.error(request, "Email already in use.")
            return render(request, 'homepage/accounts/signup.html')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    return render(request, 'homepage/accounts/signup.html')

def logout(request):
    auth_logout(request)
    return redirect('index')
