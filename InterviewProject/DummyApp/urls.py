from django.urls import include, path
from DummyApp import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"authors", views.AuthorViewSet)
router.register(r"books", views.BookViewSet)
router.register(r"members", views.MemberViewSet)
router.register(r"reservations", views.ReservationViewSet)
router.register(r"checkouts", views.CheckoutViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("get-overdue-books/", views.get_overdue_books),
    path("get-overdue-books/member/<int:member_id>", views.get_overdue_books_by_member),
    path("get-popular-books/", views.get_popular_book),
    path("get-avg-checkout-time/", views.get_avg_checkout_time),
    path("get-active-members/", views.get_active_members),
]
