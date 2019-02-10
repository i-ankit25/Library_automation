from __future__ import print_function
from django.views import generic
from .models import Book, UserProfileInfo
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import pyzbar.pyzbar as pyzbar
import cv2
import winsound
from datetime import date, timedelta
import smtplib
import ssl


def index(request):
    return render(request, 'library/index.html')


class DetailView(generic.DetailView):
    model = UserProfileInfo
    template_name = 'library/details.html'


#search bar not functional yet!!
def search(request):
    if request.method == 'GET':
        q = request.GET.get('query', None)
        try:
            results = Book.objects.filter(Book_name__icontains=q)
        except:
                    return HttpResponse("No Book found !!!")
        else:
                    return render(request, 'library/search.html', {})


@login_required
def issue(request):
    su = 0
    t = date.today()
    td = t.strftime('%d-%m-%Y')
    dur = 15
    k = "abc"
    dd = t+timedelta(days=dur)
    ded = dd.strftime('%d-%m-%Y')
    current_user = request.user.userprofileinfo
    all_books = Book.objects.all()
    try:
        id = barcode()
        book = Book.objects.get(Book_id=id, Status=0)
    except:
        #incase the book is not available for issue
        current_user.save()
        user_logout(request)
        return render(request, 'library/error.html')
    else:
        #incase book is available
        for book in all_books:
            if book.Book_id == id and book.Status == 0:
                #to ensure that the user does issue more than the specified limit of books
                if current_user.B1_id == "0":
                    current_user.B1_id = id
                    book.Issued_by = current_user.Roll_no
                    book.Status = 1
                    book.Issue_date = t
                    book.Due_date = dd#assigning a issue period of 15 days
                    k = book.Book_name
                    book.save()
                    su = 1
                elif current_user.B2_id == "0":
                    current_user.B2_id = id
                    book.Issued_by = current_user.Roll_no
                    book.Issue_date = t
                    book.Due_date = dd
                    book.Status = 1
                    k = book.Book_name
                    book.save()
                    su = 1
                elif current_user.B3_id == "0":
                    current_user.B3_id = id
                    book.Issued_by = current_user.Roll_no
                    book.Status = 1
                    book.Issue_date = t
                    book.Due_date = dd
                    k = book.Book_name
                    book.save()
                    su = 1
        if su == 1:
            #auto-email in case of successful issue
            context = ssl.create_default_context()
            con = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
            con.ehlo()
            con.login('abc@gmail.com', 'password123')#change email id and password here
            con.sendmail('abc@gmail.com', request.user.email,#change email id here
                         "Subject:Book issued successfully\n\nThis is to inform that " + k + " with  id: " + id
                     + " has been successfully issued \nISSUE DATE:" + td + "\nDUE DATE:" + ded)
            winsound.Beep(7000, 600)
            con.quit()
        current_user.save()
        user_logout(request)
        return render(request, 'library/index.html')


@login_required
def withdraw(request):
    su = 0
    current_user = request.user.userprofileinfo
    try:
        id = barcode()
        book = Book.objects.get(Issued_by=current_user.Roll_no, Book_id=id)
    except:
        #incase the referred book was not issued by the user
        current_user.save()
        user_logout(request)
        return render(request, 'library/error.html')
    else:
        #incase the book was issued by the user
        if current_user.B1_id == id and book:
            current_user.B1_id = 0
            book.Status = 0
            book.Issued_by = "abc"
            k = book.Book_name
            book.Due_date = date.today()
            book.save()
            su = 1

        if current_user.B2_id == id and book:
            current_user.B2_id = 0
            book.Status = 0
            book.Issued_by = "abc"
            k = book.Book_name
            book.Due_date = date.today()
            book.save()
            su = 1

        if current_user.B3_id == id and book:
            current_user.B3_id = 0
            book.Status = 0#assigning default status
            book.Issued_by = "abc"#assinging default values
            k = book.Book_name

            su = 1

        if su == 1:
            today = date.today()
            dd = book.Due_date
            #auto-fine calculation
            if today > dd:
                current_user.fine = current_user.fine+int((today-dd)/timedelta(days=1))
            #auto-email after successful return
            context = ssl.create_default_context()

            con = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
            con.ehlo()
            con.login('abc@gmail.com', 'password123')#change email id and password here
            con.sendmail('abc@gmail.com', request.user.email,#change email id here
                         "Subject:Book returned successfully\n\nThis is to inform that " + k + " with  id: " + id
                         + " has been successfully returned \n\n")
            winsound.Beep(7000, 600)
            con.quit()
            book.Issue_date = date.today()
            book.Due_date = date.today()
            book.save()
            current_user.save()
        elif su == 0:
            current_user.save()
        user_logout(request)
        return render(request, 'library/index.html')


def barcode():
    #function to control computer vision operations
    ret = True
    name = "Live Video Feed"
    cv2.namedWindow(name)
    cap = cv2.VideoCapture(0)
    while ret:
        ret, frame = cap.read()
        cv2.imshow(name, frame)
        s = decode(frame)
        if s != None:
            if s[0] == "1":
                ret = False
                id = s[1:]
        else:
            id = 0
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    cap.release()
    return id


def decode(im):
    #barcode detection
        ids = pyzbar.decode(im)
        for obj in ids:
            winsound.Beep(7000, 600)
            k = obj.data
            t = str(k)
            return "1" + t


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


class BookCreate(CreateView):
    model = Book
    fields = ['Book_name', 'Book_id', 'Book_publisher', 'Issue_date', 'Due_date', 'Status', 'Issued_by']


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            context = ssl.create_default_context()
            con = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
            con.ehlo()
            #auto-email after successful registertaion
            con.login('abc@gmail.com', 'password123')#change email id and password here
            con.sendmail('abc@gmail.com', user.email,#chnage email id here
                         "Subject:Registration successful\n\nThis is to inform that registration has been completed "
                         "successfully")
            winsound.Beep(7000, 600)
            con.quit()
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'library/registration_form.html', {'user_form': user_form, 'profile_form': profile_form,
                  'registered': registered})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
           if user.is_active:
                login(request, user)
                return render(request, 'library/details.html')
           else:
                return HttpResponse("Account not active")
        else:
            print("login unsuccessful")
            print("Username:{} snd password:{}".format(username, password))
            return render(request, 'library/invalid_login.html',)
    else:
        return render(request, 'library/login.html', {})


def error(request):
    return render(request, 'library/error.html')


def invalid_login(request):
    return render(request, 'library/invalid_login.html')






