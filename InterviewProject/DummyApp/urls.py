from django.urls import include, path
from DummyApp.views import (
    AuthorViewSet,
    AverageCheckoutDurationViewSet,
    BookViewSet,
    CheckoutViewSet,
    MemberOverdueBooksViewSet,
    MemberViewSet,
    MostActiveMemberViewSet,
    MostPopularBooksViewSet,
    ReservationViewSet,
    load_bulk_data,
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"books", BookViewSet, basename="books")
router.register(r"members", MemberViewSet, basename="members")
router.register(r"reservations", ReservationViewSet, basename="reservations")
router.register(r"checkouts", CheckoutViewSet, basename="checkouts")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "analytics/most-active-members/",
        MostActiveMemberViewSet.as_view(),
        name="most_active_members",
    ),
    path(
        "analytics/average-checkout-durations/",
        AverageCheckoutDurationViewSet.as_view(),
        name="average_checkout_durations",
    ),
    path(
        "analytics/most-popular-books/",
        MostPopularBooksViewSet.as_view(),
        name="most_popular_books",
    ),
    path(
        "members/<int:member_id>/overdue/",
        MemberOverdueBooksViewSet.as_view(),
        name="member_overdue_book",
    ),
    path('load-bulk-data/', load_bulk_data, name='load_bulk_data')
]
