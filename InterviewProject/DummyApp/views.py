import requests
from rest_framework import viewsets, generics

from DummyApp.models import Author, Checkout, Book, Member, Reservation
from DummyApp.serializers import (
    AuthorSerializer,
    BookSerializer,
    MemberSerializer,
    ReservationSerializer,
    CheckoutSerializer,
)
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Count, Avg, F, fields

from datetime import datetime, timedelta

from rest_framework.decorators import api_view
from django.db import models


# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    """
    API View for Author model
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API View for Book model
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class MemberViewSet(viewsets.ModelViewSet):
    """
    API View for Member model
    """

    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API View for Reservation model
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data["book"]
        members = serializer.validated_data["members"]

        if book.available_copies > 0:
            reservation = Reservation.objects.create(
                book=book,
                members=members,
                reservation_date=serializer.validated_data["reservation_date"],
                queue_position=1,
            )
            reservation.save()
            return Response(
                ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED
            )
        else:
            last_position = (
                Reservation.objects.filter(book=book)
                .latest("queue_position")
                .queue_position
            )
            position = last_position + 1 if position else 1
            reservation = Reservation.objects.create(
                book=book,
                members=members,
                reservation_date=serializer.validated_data["reservation_date"],
                queue_position=position,
            )
            reservation.save()
            return Response(
                {
                    "message": f"Book not available, Added to the reservation queue, position: {position}"
                },
                status=status.HTTP_200_OK,
            )


class CheckoutViewSet(viewsets.ModelViewSet):
    """
    API view for Checkout model
    """

    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

    def perform_create(self, serializer):
        serializer.save()
        checkout = serializer.instance
        checkout.book.available_copies -= 1
        checkout.book.save()

    def perform_update(self, serializer):
        serializer.save()
        checkout = serializer.instance
        if checkout.return_date is not None:
            checkout.book.available_copies += 1
            checkout.book.save()


class MemberOverdueBooksViewSet(generics.ListAPIView):
    """
    API View for getting list of overdue members along with their fines
    """

    serializer_class = CheckoutSerializer

    def get_queryset(self):
        member_id = self.kwargs["member_id"]
        member = Member.objects.get(pk=member_id)
        overdue_checkouts = Checkout.objects.filter(
            member=member, return_date__isnull=True, due_date__lt=datetime.now().date()
        )
        for checkout in overdue_checkouts:
            checkout.fine_amount = checkout.calculate_fine()
            checkout.save()

        return overdue_checkouts

    def list(self, request, *args, **kwargs):
        member_id = self.kwargs["member_id"]
        member = Member.objects.get(pk=member_id)
        total_fine_amount = sum(
            checkout.calculate_fine() for checkout in self.get_queryset()
        )
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(
            {"overdue_books": serializer.data, "total_fine_amount": total_fine_amount}
        )


class MostPopularBooksViewSet(generics.ListAPIView):
    """
    API View for fetching the most popular book
    """

    serializer_class = BookSerializer

    def get_queryset(self):
        popular_book = Book.objects.annotate(num_checkout=Count("checkout")).order_by(
            "-num_checkout"
        )[:1]
        return popular_book

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class AverageCheckoutDurationViewSet(generics.ListAPIView):
    """
    API View for fetching average checkout duration
    """

    serializer_class = CheckoutSerializer

    def get_queryset(self):
        return Checkout.objects.filter(return_date__isnull=False)

    def list(self, request, *args, **kwargs):
        average_duration = self.get_queryset().aggregate(
            avg_duration=Avg(
                F("return_date") - F("checkout_date"),
                output_field=fields.DurationField(),
            )
        )
        return Response({"average_checkout_duration": average_duration})


class MostActiveMemberViewSet(generics.ListAPIView):
    """
    API View for fetching most active members
    """

    serializer_class = MemberSerializer

    def get_queryset(self):
        active_members = Member.objects.annotate(
            num_checkout=Count("checkout")
        ).order_by("-num_checkout")[:1]
        return active_members

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


@api_view(["POST"])
def load_bulk_data(request):
    if request.method == "POST":
        for data in request.data:
            if data["type"] == "reservation":
                url = "http://127.0.0.1:8000/api/v1/reservations/"
                body = {
                    "book": data["book_id"],
                    "members": data["member_id"],
                    "reservation_date": str(datetime.now().date()),
                }
                requests.post(url, data=body)
            else:
                url = "http://127.0.0.1:8000/api/v1/checkouts/"
                body = {
                    "checkout_date": str(datetime.now().date()),
                    "due_date": str(datetime.now().date() + timedelta(7)),
                    "book": data["book_id"],
                    "member": data["member_id"],
                }
                requests.post(url, data=body)
        return Response(
            {"Data has been populated. Successfully"}, status=status.HTTP_200_OK
        )
