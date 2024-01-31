from rest_framework import serializers
from DummyApp.models import Author, Book, Checkout, Member, Reservation


# Create your serializers here.
class AuthorSerializer(serializers.ModelSerializer):
    """
    Author serializer class
    """

    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    """
    Book serializer class
    """

    class Meta:
        model = Book
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    """
    Member serializer class
    """

    class Meta:
        model = Member
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    """
    Reservation serializer class
    """

    queue_position = serializers.IntegerField(required=False)

    class Meta:
        model = Reservation
        fields = "__all__"


class CheckoutSerializer(serializers.ModelSerializer):
    """
    Checkout serializer class
    """

    return_date = serializers.DateField(required=False)
    fine_amount = serializers.SerializerMethodField()

    class Meta:
        model = Checkout
        fields = "__all__"

    def get_fine_amount(self, obj):
        return obj.calculate_fine()
