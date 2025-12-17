from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("service", models.CharField(max_length=120)),
                ("name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                ("dob", models.DateField()),
                ("time", models.TimeField(blank=True, null=True)),
                ("place", models.CharField(blank=True, max_length=200)),
                ("questions", models.TextField(blank=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("status", models.CharField(choices=[("pending_payment", "pending_payment"), ("confirmed", "confirmed"), ("cancelled", "cancelled")], default="pending_payment", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("currency", models.CharField(default="INR", max_length=10)),
                ("status", models.CharField(choices=[("pending", "pending"), ("succeeded", "succeeded"), ("failed", "failed"), ("cancelled", "cancelled")], default="pending", max_length=20)),
                ("provider", models.CharField(default="test", max_length=50)),
                ("provider_order_id", models.CharField(blank=True, max_length=120)),
                ("reference", models.CharField(max_length=64, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("booking", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="payment", to="main.booking")),
            ],
        ),
    ]
