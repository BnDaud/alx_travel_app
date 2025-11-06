import os
import django
from faker import Faker
from random import randint, choice, uniform
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

# ✅ Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')
django.setup()

# Now import your models
from listings.models import User, Listing, Booking, Review

fake = Faker()

# --- 0️⃣ Create superuser 'mac' ---
if not User.objects.filter(username='mac').exists():
    User.objects.create_superuser(
        username='mac',
        email='mac@example.com',
        password='macbook01',
        role='admin',  # or 'superuser', depending on your model
        phone_number='000-000-0000'
    )
    print("✅ Superuser 'mac' created")
else:
    print("Superuser 'mac' already exists")

# --- 1️⃣ Create 10 fake users ---
roles = ["host", "admin", "guest"]
users = []
for _ in range(10):
    user = User.objects.create_user(
        username=fake.user_name(),
        password="password123",
        email=fake.email(),
        role=choice(roles),
        phone_number=fake.phone_number()
    )
    users.append(user)
print("✅ 10 users created")

# --- 2️⃣ Create listings (only if hosts exist) ---
hosts = [u for u in users if u.role == "host"]
if not hosts:
    print("⚠️ No hosts found. Skipping listings...")
else:
    listings = []
    for _ in range(randint(50, 100)):
        host = choice(hosts)
        listing = Listing.objects.create(
            host_id=host,
            name=fake.catch_phrase(),
            description=fake.paragraph(nb_sentences=5),
            location=fake.city(),
            pricepernight=Decimal(uniform(25, 150)).quantize(Decimal("0.01")),
        )
        listings.append(listing)
    print(f"✅ {len(listings)} listings created")

    # --- 3️⃣ Create bookings ---
    bookings = []
    for _ in range(randint(60, 120)):
        user = choice(users)
        listing = choice(listings)
        start = timezone.now().date() + timedelta(days=randint(1, 20))
        end = start + timedelta(days=randint(1, 5))
        total = listing.pricepernight * (end - start).days
        booking = Booking.objects.create(
            property_id=listing,
            user_id=user,
            start_date=start,
            end_date=end,
            total_price=total,
            status=choice(["Pending", "Confirmed", "Canceled"]),
        )
        bookings.append(booking)
    print(f"✅ {len(bookings)} bookings created")

    # --- 4️⃣ Create reviews ---
    for _ in range(randint(80, 150)):
        listing = choice(listings)
        Review.objects.create(
            property_id=listing,
            rating=randint(1, 5),
            comment=fake.sentence(nb_words=15)
        )
    print("✅ Reviews created successfully")
