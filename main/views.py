from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.crypto import get_random_string
from .forms import BookingForm
from .models import Booking, Payment

@login_required
def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def _price_for_service(name: str) -> int:
    mapping = {
        "Birth Chart Analysis": 2500,
        "Marriage Compatibility": 3500,
        "Career Guidance": 2800,
        "Gemstone Recommendation": 2200,
        "Vastu Shastra": 4000,
        "Numerology Report": 1800,
        "Quick Consultation": 2100,
        "Single Question": 1100,
        "Extended Consultation": 4500,
    }
    return mapping.get(name, 2000)

@login_required
def book(request):
    if request.method != "POST":
        return redirect("home")
    form = BookingForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please correct the errors in the form")
        return redirect("home")
    data = form.cleaned_data
    amount = _price_for_service(data["service"])
    booking = Booking.objects.create(
        user=request.user,
        service=data["service"],
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        dob=data["dob"],
        time=data.get("time"),
        place=data.get("place", ""),
        questions=data.get("questions", ""),
        amount=amount,
        status="pending_payment",
    )
    reference = get_random_string(16)
    payment = Payment.objects.create(
        booking=booking,
        amount=amount,
        status="pending",
        reference=reference,
    )
    return redirect("payment_checkout", reference=payment.reference)

@login_required
def payment_checkout(request, reference):
    payment = get_object_or_404(Payment, reference=reference)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "simulate_success":
            payment.status = "succeeded"
            payment.save()
            booking = payment.booking
            booking.status = "confirmed"
            booking.save()
            messages.success(request, "Payment successful and booking confirmed")
            return redirect("home")
        if action == "simulate_fail":
            payment.status = "failed"
            payment.save()
            messages.error(request, "Payment failed")
            return redirect("payment_checkout", reference=reference)
    return render(request, "payment_checkout.html", {"payment": payment})
