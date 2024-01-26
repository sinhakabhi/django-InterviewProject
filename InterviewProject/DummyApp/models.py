from django.db import models
from django.urls import reverse


# Create your models here.
class Author(models.Model):
    """
    Author model
    """

    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Author"

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model
    """

    book_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Book"

    def __str__(self):
        return self.name


class Member(models.Model):
    """
    Member model
    """

    member_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    fine_charged = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Member"

    def __str__(self):
        return self.name


class Reservation(models.Model):
    """
    Reservation model
    """

    reservation_id = models.AutoField(primary_key=True)
    members_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date_time = models.DateTimeField()

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"


    def get_absolute_url(self):
        return reverse("Reservation_detail", kwargs={"pk": self.pk})


class Checkout(models.Model):
    """
    Checkout model"""

    checkout_id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    checkout_date_time = models.DateTimeField()
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Checkout"
        verbose_name_plural = "Checkouts"


    def get_absolute_url(self):
        return reverse("Checkout_detail", kwargs={"pk": self.pk})
