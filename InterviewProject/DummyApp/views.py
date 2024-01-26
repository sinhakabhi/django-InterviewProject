from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets

from DummyApp.models import *
from DummyApp.serializers import *


# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer


def get_overdue_books(request):
    books = Checkout.objects.all().filter(checkout_date_time__lte=datetime.now() + timedelta(days=1))
    book_list = []
    for book in books:
        get_book = Book.objects.get(name=book.book_id).name
        book_list.append(get_book)
    return HttpResponse(book_list)


def get_overdue_books_by_member(request, member_id):
    books = Checkout.objects.filter(checkout_date_time__lte=datetime.now() + timedelta(days=1), member_id=member_id)
    return HttpResponse('Books')


def get_popular_book(request):
    pass

def get_avg_checkout_time(request):
    pass

def get_active_members(request):
    pass