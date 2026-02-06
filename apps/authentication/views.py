"""
Authentication views for MFU Web Portal.
Handles login, registration, email confirmation, and password reset.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from allauth.account.models import EmailAddress
from apps.core.models import User


def home_redirect(request):
    """Redirect home page to appropriate location based on auth status."""
    if request.user.is_authenticated:
        return redirect('profiles:dashboard')
    return redirect('authentication:login')


@require_http_methods(["GET", "POST"])
def custom_login(request):
    """
    Custom login page that supports both manual login and Google OAuth.
    """
    if request.user.is_authenticated:
        return redirect('profiles:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Please enter both email and password.')
            return render(request, 'authentication/login.html')

        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Check if user is active
            if not user.is_active:
                messages.error(request, 'Your account is inactive. Please contact support.')
                return render(request, 'authentication/login.html')

            # Check if email is confirmed
            if not user.email_confirmed:
                messages.warning(
                    request,
                    'Please confirm your email address before logging in. '
                    'Check your inbox for the confirmation link.'
                )
                return render(request, 'authentication/login.html')

            # Login successful
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_short_name()}!')

            # Redirect to next or dashboard
            next_url = request.GET.get('next', 'profiles:dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'authentication/login.html')


@require_http_methods(["GET", "POST"])
def custom_register(request):
    """
    Custom registration page with email confirmation.
    """
    if request.user.is_authenticated:
        return redirect('profiles:dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validation
        errors = []

        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not email:
            errors.append('Email is required.')
        if not password:
            errors.append('Password is required.')
        if password != password_confirm:
            errors.append('Passwords do not match.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append('An account with this email already exists.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'authentication/register.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })

        # Create user (inactive until email confirmed)
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_active=False,  # Will be activated after email confirmation
            email_confirmed=False
        )

        # Create EmailAddress record for allauth
        EmailAddress.objects.create(
            user=user,
            email=email,
            primary=True,
            verified=False
        )

        # Send confirmation email (allauth handles this)
        from allauth.account.utils import send_email_confirmation
        send_email_confirmation(request, user)

        messages.success(
            request,
            'Registration successful! Please check your email to confirm your account.'
        )
        return redirect('authentication:email_confirmation_sent')

    return render(request, 'authentication/register.html')


def email_confirmation_sent(request):
    """Display message that email confirmation has been sent."""
    return render(request, 'authentication/email_confirmation_sent.html')


@login_required
def custom_logout(request):
    """Custom logout view."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('authentication:login')


@require_http_methods(["GET", "POST"])
def forgot_password(request):
    """
    Forgot password page - user enters email to receive reset link.
    """
    if request.user.is_authenticated:
        return redirect('profiles:dashboard')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()

        if not email:
            messages.error(request, 'Please enter your email address.')
            return render(request, 'authentication/forgot_password.html')

        try:
            user = User.objects.get(email=email)

            # Generate token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build reset URL
            reset_url = request.build_absolute_uri(
                reverse('authentication:reset_password', kwargs={'uidb64': uid, 'token': token})
            )

            # Send email
            subject = 'Password Reset Request - MFU Web Portal'
            html_message = render_to_string(
                'authentication/emails/password_reset_email.html',
                {
                    'user': user,
                    'reset_url': reset_url,
                    'token': token,
                }
            )
            send_mail(
                subject,
                f'Click here to reset your password: {reset_url}',
                'noreply@mfuportal.com',
                [email],
                html_message=html_message,
                fail_silently=False,
            )

            messages.success(
                request,
                'Password reset link has been sent to your email. Please check your inbox.'
            )
            return redirect('authentication:login')

        except User.DoesNotExist:
            # Don't reveal if email exists for security
            messages.success(
                request,
                'If an account exists with this email, a password reset link has been sent.'
            )
            return redirect('authentication:login')

    return render(request, 'authentication/forgot_password.html')


@require_http_methods(["GET", "POST"])
def reset_password(request, uidb64, token):
    """
    Reset password page - user enters new password with valid token.
    """
    if request.user.is_authenticated:
        return redirect('profiles:dashboard')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, 'Invalid password reset link.')
        return redirect('authentication:login')

    # Verify token
    if not default_token_generator.check_token(user, token):
        messages.error(request, 'Password reset link has expired. Please request a new one.')
        return redirect('authentication:forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Validation
        errors = []
        if not password:
            errors.append('Password is required.')
        if password != password_confirm:
            errors.append('Passwords do not match.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'authentication/reset_password.html', {'uidb64': uidb64, 'token': token})

        # Set new password
        user.set_password(password)
        user.save()

        messages.success(request, 'Your password has been reset successfully. You can now log in.')
        return redirect('authentication:login')

    return render(request, 'authentication/reset_password.html', {'uidb64': uidb64, 'token': token})
