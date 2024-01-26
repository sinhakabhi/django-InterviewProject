from rest_framework import serializers
from DummyApp.models import *


# Create your serializers here.
class AuthorSerializer(serializers.ModelSerializer):
    """
    Author serializer class
    """

    author_id = serializers.ReadOnlyField()

    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """
    Book serializer class
    """

    book_id = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    """
    Member serializer class
    """

    member_id = serializers.ReadOnlyField()

    class Meta:
        model = Member
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    """
    Reservation serializer class
    """

    reservation_id = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = "__all__"


class CheckoutSerializer(serializers.ModelSerializer):
    """
    Checkout serializer class
    """

    checkout_id = serializers.ReadOnlyField()

    class Meta:
        model = Checkout
        fields = "__all__"
