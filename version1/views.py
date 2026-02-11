from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import WhatsNextUsers, WhatsNextOrganizers, WhatsNextWorkshops, WhatsNextWorkshopCategories, WhatsNextBookings
from django.utils import timezone
from .decorators import login_required, organizer_required



def index(request):
    workshops = WhatsNextWorkshops.objects.select_related('category', 'organizer').order_by('-date')
    categories = WhatsNextWorkshopCategories.objects.all()
    durations = ["Any", "1-3", "3-6", "6+"]

    # Apply filters if present
    category = request.GET.get("category")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")
    duration = request.GET.get("duration")

    if category and category != "All":
        workshops = workshops.filter(category__name__iexact=category)

    if price_min:
        workshops = workshops.filter(price__gte=price_min)
    if price_max:
        workshops = workshops.filter(price__lte=price_max)

    if duration and duration != "Any":
        from datetime import datetime
        dur_map = {"1-3": (1, 3), "3-6": (3, 6), "6+": (6, 24)}
        min_dur, max_dur = dur_map.get(duration, (0, 24))
        workshops = [w for w in workshops if w.start_time and w.end_time and
                     min_dur <= ((datetime.combine(w.date, w.end_time) - datetime.combine(w.date, w.start_time)).total_seconds() / 3600) <= max_dur]

    return render(request, 'index.html', {
        'workshops': workshops,
        'categories': categories,
        'durations': durations,
    })



@organizer_required
def create_workshop_view(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        other_category = request.POST.get('other_category')
        location = request.POST.get('location')
        address = request.POST.get('address')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        price = request.POST.get('price')
        capacity = request.POST.get('capacity')
        poster = request.FILES.get('poster')
        instructor_name = request.POST.get('instructor_name')


        try:
            user_id = request.session.get('user_id')
            organizer = WhatsNextOrganizers.objects.get(user_id=user_id)
        except WhatsNextOrganizers.DoesNotExist:
            messages.error(request, "You must be an organizer to create workshops.")
            return redirect('/')

        # Handle "Other" category option
        if category_id == 'other' and other_category:
            category, created = WhatsNextWorkshopCategories.objects.get_or_create(name=other_category.strip())
        else:
            category = WhatsNextWorkshopCategories.objects.get(id=category_id)

        WhatsNextWorkshops.objects.create(
            organizer=organizer,
            title=title,
            description=description,
            instructor_name=instructor_name,
            category=category,
            location=location,
            address=address,
            date=date,
            start_time=start_time or None,
            end_time=end_time or None,
            price=price or 0,
            capacity=capacity or 50,
            poster=poster,
            created_at=timezone.now()
        )

        messages.success(request, "Workshop created successfully!")
        return redirect('/')  # Redirect to dashboard or list view

    categories = WhatsNextWorkshopCategories.objects.all()
    return render(request, "create_workshop.html", {"categories": categories})


def list_users(request):
    users = WhatsNextUsers.objects.all().order_by('-id')
    return render(request, 'list_users.html', {'users': users})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = WhatsNextUsers.objects.get(email=email)
            if check_password(password, user.password_hash):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['user_role'] = user.role
                if user.role == 'organizer':
                    try:
                        org = WhatsNextOrganizers.objects.get(user_id=user.id)
                        request.session['organizer_id'] = org.id
                    except WhatsNextOrganizers.DoesNotExist:
                        request.session['organizer_id'] = None
                else:
                    request.session['organizer_id'] = None

                messages.success(request, f"Welcome back, {user.name}!")
                next_url = request.GET.get('next', None)
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('index')
            else:
                messages.error(request, "Invalid password.")
        except WhatsNextUsers.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone')
        role = request.POST.get('role', 'user')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/')

        if WhatsNextUsers.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('/')

        user = WhatsNextUsers.objects.create(
            name=name,
            email=email,
            phone=phone,
            role=role,
            password_hash=make_password(password)
        )

        if role == 'organizer':
            org = WhatsNextOrganizers.objects.create(user=user)
            request.session['organizer_id'] = org.id
        else:
            request.session['organizer_id'] = None

        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        request.session['user_role'] = user.role

        messages.success(request, "Welcome, you're now logged in!")

        if role == 'organizer':
            return redirect('organizer_dashboard')

        return redirect('/')

    return render(request, 'signup.html')


@organizer_required
def organizer_dashboard(request):
    return render(request, 'organizer_dashboard.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('/')

@organizer_required
def add_workshop(request):
    return redirect('create_workshop')


@organizer_required
def upcoming_workshops(request):
    messages.info(request, "Upcoming Workshops - coming soon.")
    return redirect('organizer_dashboard')


@organizer_required
def previous_workshops(request):
    messages.info(request, "Previous Workshops - coming soon.")
    return redirect('organizer_dashboard')


@organizer_required
def promote_workshop(request):
    messages.info(request, "Promote Workshop - coming soon.")
    return redirect('organizer_dashboard')


@organizer_required
def organizer_profile(request):
    messages.info(request, "Organizer Profile - coming soon.")
    return redirect('organizer_dashboard')

def register_workshop_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone', '').strip() or None
        role = request.POST.get('role', 'user')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register_workshop')

        if WhatsNextUsers.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register_workshop')

        user = WhatsNextUsers.objects.create(
            name=name,
            email=email,
            phone=phone,
            role=role,
            password_hash=make_password(password),
        )

        if role == 'organizer':
            org = WhatsNextOrganizers.objects.create(user=user)
            request.session['organizer_id'] = org.id
        else:
            request.session['organizer_id'] = None

        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        request.session['user_role'] = user.role

        messages.success(request, "Welcome, you're now registered and logged in!")

        if role == 'organizer':
            return redirect('organizer_dashboard')
        return redirect('index')

    return render(request, 'register.html')


# Enroll
def enroll_workshop(request, workshop_id):
    """
    Display enrollment form for a workshop.
    """
    workshop = get_object_or_404(WhatsNextWorkshops, id=workshop_id)
    
    return render(request, "enroll.html", {"workshop": workshop})


def confirm_enroll(request, workshop_id):
    """
    Handle form submission and save booking.
    """
    workshop = get_object_or_404(WhatsNextWorkshops, id=workshop_id)
    
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        
        # Check if user exists; if not, create
        user, created = WhatsNextUsers.objects.get_or_create(
            email=email,
            defaults={
                "name": fullname,
                "phone": phone,
                "role": "user",
                "password_hash": ""  # You can leave blank or hash a default password
            }
        )
        
        # Save booking
        booking = WhatsNextBookings.objects.create(
            user=user,
            workshop=workshop,
            booked_at=timezone.now(),
            status="booked"
        )
        
        messages.success(request, f"Successfully enrolled in {workshop.title}!")
        return redirect("enroll_success", booking_id=booking.id)
    
    return redirect("enroll_workshop", workshop_id=workshop.id)


def enroll_success(request, booking_id):
    """
    Show success page after enrollment.
    """
    booking = get_object_or_404(WhatsNextBookings, id=booking_id)
    return render(request, "enroll_success.html", {"booking": booking})
