from django.db import models
from django.utils import timezone


class WhatsNextUsers(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('organizer', 'Organizer'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.TextField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "whats_next_users"

    def __str__(self):
        return f"{self.name} ({self.role})"


class WhatsNextOrganizers(models.Model):
    user = models.OneToOneField(WhatsNextUsers, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=150, blank=True, null=True)
    website_url = models.URLField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "whats_next_organizers"

    def __str__(self):
        return self.organization_name or self.user.name


class WhatsNextWorkshopCategories(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "whats_next_workshop_categories"

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone

class WhatsNextWorkshops(models.Model):
    organizer = models.ForeignKey('WhatsNextOrganizers', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey('WhatsNextWorkshopCategories', on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200)
    address = models.TextField()
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    capacity = models.PositiveIntegerField(default=50)
    poster = models.ImageField(upload_to='workshop_posters/', null=True, blank=True) 
    instructor_name = models.CharField(max_length=100, default='', blank=True) 
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "whats_next_workshops"

    def __str__(self):
        return f"{self.title} on {self.date}"


class WhatsNextBookings(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(WhatsNextUsers, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WhatsNextWorkshops, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')

    class Meta:
        db_table = "whats_next_bookings"

    def __str__(self):
        return f"{self.user.name} → {self.workshop.title} ({self.status})"


class WhatsNextReviews(models.Model):
    user = models.ForeignKey(WhatsNextUsers, on_delete=models.CASCADE)
    workshop = models.ForeignKey(WhatsNextWorkshops, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "whats_next_reviews"

    def __str__(self):
        return f"{self.user.name}'s review for {self.workshop.title}"
