from datetime import datetime
from django.db import models


# Create your models here.
class Author(models.Model):
    """
    Author model
    """

    name = models.CharField(max_length=200)


class Book(models.Model):
    """
    Book model
    """

    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()


class Member(models.Model):
    """
    Member model
    """

    name = models.CharField(max_length=200)


class Reservation(models.Model):
    """
    Reservation model
    """

    members = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    is_active = models.BooleanField(default=True)
    queue_position = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.queue_position:
            last_position = (
                Reservation.objects.filter(book=self.book, is_active=True)
                .order_by("-queue_position")
                .filter()
            )
            self.queue_position = (
                (last_position.queue_position + 1) if last_position else 1
            )
        self.book.available_copies -= 1
        self.book.save()
        super().save(*args, **kwargs)


class Checkout(models.Model):
    """
    Checkout model
    """

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    checkout_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def is_overdue(self):
        if self.return_date is None and datetime.now().date() > self.due_date:
            return True
        return False

    def calculate_fine(self):
        if self.is_overdue():
            days_overdue = (datetime.now().date() - self.due_date).days
            return days_overdue * 50
        return 0
