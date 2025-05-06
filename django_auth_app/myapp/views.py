from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tweet, UserSettings

User = get_user_model()

# Home Page
@login_required
def index_view(request):
    tweets = Tweet.objects.select_related('user').order_by('-created_at')
    trending = ["#Django", "#Python", "#100DaysOfCode"]
    return render(request, 'index.html', {
        'tweets': tweets,
        'trending': trending
    })

# Explore Page
@login_required
def explore_view(request):
    return render(request, 'explore.html')

# Messages Page
@login_required
def messages_view(request):
    return render(request, 'messages.html')

# ✅ Settings Page with Account Update
@login_required
def settings_view(request):
    settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Update settings preferences
        settings.private_account = bool(request.POST.get('private_account'))
        settings.allow_tagging = bool(request.POST.get('allow_tagging'))
        settings.email_notifications = bool(request.POST.get('email_notifications'))
        settings.push_notifications = bool(request.POST.get('push_notifications'))
        settings.dark_mode = bool(request.POST.get('dark_mode'))
        settings.font_size = request.POST.get('font_size', 'Medium')
        settings.save()

        # Update username and password
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')








        if new_username and new_username != request.user.username:
            request.user.username = new_username

        if new_password:
            request.user.set_password(new_password)

        request.user.save()

        # Re-authenticate if password changed
        if new_password:
            login(request, request.user)

        messages.success(request, "Settings saved successfully!")
        return redirect('settings')

    return render(request, 'settings.html', {
        'settings': settings,
        'user': request.user
    })

# ✅ Login View (Supports Email or Username)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'login.html', {
        'form_type': 'login'
    })

# ✅ Registration View (UserSettings created by signal)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            # ❌ Removed: UserSettings.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome 🎉')
            return redirect('index')

    return render(request, 'login.html', {
        'form_type': 'register'
    })

# ✅ Logout View
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('login')

# ✅ Post Tweet View
@login_required
def post_tweet(request):
    if request.method == 'POST':
        content = request.POST.get('tweet', '').strip()
        if content:
            Tweet.objects.create(user=request.user, content=content)
            messages.success(request, 'Tweet posted!')
        else:
            messages.error(request, 'Tweet cannot be empty.')
    return redirect('index')
