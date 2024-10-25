from django.shortcuts import render, get_object_or_404, redirect
from .models import Study , Register
from .forms import StudyForm  # Import the ModelForm for Study
from django.contrib import messages
from django.db import IntegrityError
import hashlib
from django.contrib.auth import logout as django_logout

# List all studies
def study_list(request):
    studies = Study.objects.all()  # Fetch all studies from the database
    return render(request, 'study_list.html', {'studies': studies})  # Render the study list


# Show study details
def study_detail(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    return render(request, 'study_detail.html', {'study': study})


# Add a new study
def add_study(request):
    if request.method == "POST":
        form = StudyForm(request.POST)
        if form.is_valid():  # Validate form input
            form.save()  # Save the form data to the database
            return redirect('study_list')  # Redirect to study list after successful submission
    else:
        form = StudyForm()  # Display empty form
    return render(request, 'add_study.html', {'form': form})  # Render the add study form


# Edit an existing study
def edit_study(request, study_id):
    study = get_object_or_404(Study, pk=study_id)
    if request.method == "POST":
        form = StudyForm(request.POST, instance=study)
        if form.is_valid():  # Validate form input
            form.save()  # Save the updated form data
            return redirect('study_list')  # Redirect to study list after editing
    else:
        form = StudyForm(instance=study)  # Pre-fill form with existing study data
    return render(request, 'edit_study.html', {'form': form, 'study': study})  # Render the edit study form


# Delete a study
# def delete_study(request, study_id):
#     study = get_object_or_404(Study, pk=study_id)
#     study.delete()  # Delete the study from the database
#     return redirect('study_list')  # Redirect to the study list
def delete_selected_studies(request):
    if request.method == 'POST':
        study_ids = request.POST.getlist('study_ids')  # Get the list of selected study IDs
        if study_ids:  # Check if any study was selected
            Study.objects.filter(id__in=study_ids).delete()  # Delete all selected studies
        return redirect('study_list')  # Redirect back to the study list

    return redirect('study_list')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        try:
            # Validation: Check if passwords match
            if password != confirm_password:
                raise ValueError("Passwords do not match")

            # Check if email is already registered
            if Register.objects.filter(email=email).exists():
                raise ValueError("Email is already registered")

            # Hash the password before storing it in the database
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Create and save the new user
            user = Register(email=email, password=hashed_password)
            user.save()

            messages.success(request, "Registration successful! Please login.")
            return redirect('login')

        except ValueError as ve:
            messages.error(request, str(ve))  # Handle validation errors
        except IntegrityError:
            messages.error(request, "Database error occurred during registration.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'register.html')


# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Hash the password before checking it in the database
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Authenticate user
            user = Register.objects.filter(email=email, password=hashed_password).first()

            if user:
                # Set session or cookies if needed
                request.session['user_id'] = user.id  # You can also use Django's login system here
                messages.success(request, "Login successful!")
                return redirect(study_list)  # Redirect to home or dashboard after successful login
            else:
                raise ValueError("Invalid email or password")

        except ValueError as ve:
            messages.error(request, str(ve))  # Handle login errors
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'login.html')

def logout_page(request):
    return render(request, 'logout.html')


# Handle Logout Confirmation and Log Out the User
def logout_confirm(request):
    if request.method == 'POST':
        try:
            django_logout(request)  # This logs out the user and clears the session.
            messages.success(request, "You have been logged out successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred during logout: {e}")
        return redirect(login_view)  # Redirect to login page after logout

    return redirect(login_view)  # If it's not POST, redirect back to home
