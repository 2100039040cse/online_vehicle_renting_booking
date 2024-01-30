from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.utils import timezone
from .models import PaymentDetails, Feedback, CancellationReason, CanceledBooking, Partner, Bike, Car, Auto, Traveller, Truck, Tractor, Jcb, BorewellTruck, CombineHarvester  
from .forms import User,LoginForm, ChangePasswordForm, SignupForm, PaymentForm, PartnerForm, BikeForm, CarForm, AutoForm, TravellerForm , TruckForm, TractorForm, JcbForm, BorewellTruckForm, CombineHarvesterForm 
from django.shortcuts import get_object_or_404
from django.db.models import Q
from decimal import Decimal
from datetime import timedelta



def index(request):
    return render(request, 'index.html')

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.', extra_tags='alert-error')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered. Please use a different email.', extra_tags='alert-error')
            else:
                form.save()
                messages.success(request, 'Registration successful!', extra_tags='alert-success')
                return redirect(reverse('signup') + '?registration_success=true')
        else:
            # Adding error messages for form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}', extra_tags='alert-error')
                
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
 
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_superuser:
                    return render(request, 'admin_dashboard.html')
                elif user.is_staff:
                    return render(request, 'staff_dashboard.html')  
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect username or password. Please try again.')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been changed successfully. Please log in again.')
                return redirect('logout')
            else:
                messages.error(request, 'Incorrect old password. Please try again.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')
        if user.check_password(password):
            user.delete()
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Incorrect password. Account deletion failed.')
    return render(request, 'delete_account.html')

@login_required
def admin_change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been changed successfully. Please log in again.')
                return redirect('logout')
            else:
                messages.error(request, 'Incorrect old password. Please try again.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'admin_change_password.html', {'form': form})


@login_required
def admin_change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been changed successfully. Please log in again.')
                return redirect('logout')
            else:
                messages.error(request, 'Incorrect old password. Please try again.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'admin_change_password.html', {'form': form})

@login_required
def admin_delete_account(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')
        if user.check_password(password):
            user.delete()
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Incorrect password. Account deletion failed.')
    return render(request, 'admin_delete_account.html')


def admin_redirect(request):
    if request.user.is_superuser:
        return render(request, 'admin_dashboard.html')  
    else:
        
        return redirect('home')




def admin_rides(request):
     return render(request, 'admin_rides.html')

# def admin_users_list(request):
#      return render(request, 'admin_users_list.html')
def admin_users_list(request):
    users = User.objects.all()
    return render(request, 'admin_users_list.html', {'users': users})



# @login_required
# def enable_user(request, user_id):
#     user_to_enable = User.objects.get(id=user_id)
#     if request.user.is_superuser and not request.user.id == user_id and not user_to_enable.is_superuser:
#         user_to_enable.is_active = True
#         user_to_enable.save()
#         messages.success(request, f"{user_to_enable.username} has been enabled.", extra_tags='success')
#     else:
#         messages.error(request, "You don't have permission to enable this user.", extra_tags='error')
#     return redirect('admin_users_list')


# @login_required
# def disable_user(request, user_id):
#     if request.user.is_superuser and not request.user.id == user_id:
#         user_to_disable = User.objects.get(id=user_id)
#         user_to_disable.is_active = False
#         user_to_disable.save()
#         messages.success(request, f"{user_to_disable.username} has been disabled.", extra_tags='success')
#     else:
#         messages.error(request, "You don't have permission to disable this user.", extra_tags='error')
#     return redirect('admin_users_list')

# @login_required
# def delete_user(request, user_id):
#     if request.user.is_superuser and not request.user.id == user_id:
#         user_to_delete = User.objects.get(id=user_id)
#         user_to_delete.delete()
#         messages.success(request, f"{user_to_delete.username} has been deleted.", extra_tags='success')
#     else:
#         messages.error(request, "You don't have permission to delete this user.", extra_tags='error')
#     return redirect('admin_users_list')



@login_required
def disable_user(request, user_id):
    user_to_disable = User.objects.get(id=user_id)
    if request.user.is_superuser and request.user.is_staff and not request.user.id == user_id and not user_to_disable.is_superuser:
        user_to_disable.is_active = False
        user_to_disable.save()
        messages.success(request, f"{user_to_disable.username} has been disabled.", extra_tags='success')
    else:
        messages.error(request, "You don't have permission to disable this user.", extra_tags='error')
    return redirect('admin_users_list')

@login_required
def enable_user(request, user_id):
    user_to_enable = User.objects.get(id=user_id)
    if request.user.is_superuser and request.user.is_staff and not request.user.id == user_id and not user_to_enable.is_superuser:
        user_to_enable.is_active = True
        user_to_enable.save()
        messages.success(request, f"{user_to_enable.username} has been enabled.", extra_tags='success')
    else:
        messages.error(request, "You don't have permission to enable this user.", extra_tags='error')
    return redirect('admin_users_list')

@login_required
def delete_user(request, user_id):
    user_to_delete = User.objects.get(id=user_id)
    if request.user.is_superuser and request.user.is_staff and not request.user.id == user_id and not user_to_delete.is_superuser:
        user_to_delete.delete()
        messages.success(request, f"{user_to_delete.username} has been deleted.", extra_tags='success')
    else:
        messages.error(request, "You don't have permission to delete this user.", extra_tags='error')
    return redirect('admin_users_list')


def admin_viz_a_rides_graph (request):
     return render(request, 'admin_viz_a_rides_graph .html')






def admin_khm_a_rides(request):
     return render(request, 'admin_khm_a_rides.html')

def admin_khm_b_rides(request):
     return render(request, 'admin_khm_b_rides.html')






def staff_rides(request):
     return render(request, 'staff_rides.html')



def staff_khm_a_rides(request):
     return render(request, 'staff_khm_a_rides.html')

def staff_khm_b_rides(request):
     return render(request, 'staff_khm_b_rides.html')


def staff_dashboard(request):
     return render(request, 'staff_dashboard.html')

def staff_account(request):
     return render(request, 'staff_account.html')





@login_required
def staff_change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your password has been changed successfully. Please log in again.')
                return redirect('logout')
            else:
                messages.error(request, 'Incorrect old password. Please try again.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'staff_change_password.html', {'form': form})


@login_required
def staff_delete_account(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')
        if user.check_password(password):
            user.delete()
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Incorrect password. Account deletion failed.')
    return render(request, 'staff_delete_account.html')


def become_partner_view(request):
    if request.method == 'POST':
        form = PartnerForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the Partner model
            messages.success(request, 'Your details have been submitted. The admin will contact you soon.', extra_tags='alert-success')
            return redirect('become_partner')
        else:
            # Adding error messages for form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}', extra_tags='alert-error')
    else:
        form = PartnerForm()

    return render(request, 'become_partner.html', {'form': form})


def admin_dashboard(request):
     return render(request, 'admin_dashboard.html')



@login_required
def admin_notification(request):
    if request.method == 'POST' and 'action' in request.POST:
        partner_id = request.POST.get('partner_id')
        partner = get_object_or_404(Partner, pk=partner_id)
        
        if request.POST['action'] == 'contact':
            # Update the status or perform the action you want when the admin clicks "Contact"
            partner.contact_status = 'Contracted'
            partner.contacted_by = request.user  # Assign the logged-in admin user
            partner.contact_date = timezone.now()  # Import timezone from django.utils if not imported
            
            partner.save()
            # Redirect or perform any other action after updating the status

    partners = Partner.objects.all()  
    return render(request, 'admin_notification.html', {'partners': partners})

def admin_account(request):
     return render(request, 'admin_account.html')

def admin_add_vehicle(request):
    return render(request, 'admin_add_vehicle.html')

def admin_add_bike(request):
    return render(request, 'admin_add_bike.html')

def admin_add_car(request):
    return render(request, 'admin_add_car.html')




def other_viz_a_list(request):
    return render(request, 'other_viz_a_list.html')

def other_viz_b_list(request):
    return render(request, 'other_viz_b_list.html')


@login_required
def admin_add_bike(request):
    if request.method == 'POST':
        form = BikeForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']

            if Bike.objects.filter(vehicle_id=vehicle_id).exists() or Bike.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Bike ID or Bike Number already exists.')
                return redirect('admin_add_bike')

            bike = form.save(commit=False)
            bike.added_by = request.user
            bike.date_added = timezone.now()

            location = request.POST.get('location')
            station = request.POST.get('station')

            # Adjust the logic based on your specific requirements for bike locations and stations
            if location == 'Vijayawada' and station == 'A Station':
                bike.save()
                messages.success(request, 'Bike successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_bike')
            elif location == 'Vijayawada' and station == 'B Station':
                bike.save()
                messages.success(request, 'Bike successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_bike')
            elif location == 'Khammam' and station == 'A Station':
                bike.save()
                messages.success(request, 'Bike successfully added, check in Khammam A Station list.')
                return redirect('admin_add_bike')
            elif location == 'Khammam' and station == 'B Station':
                bike.save()
                messages.success(request, 'Bike successfully added, check in Khammam B Station list.')
                return redirect('admin_add_bike')
            else:
                messages.success(request, 'Data is not added in the correct location.')
                return redirect('admin_add_bike')
        else:
            messages.error(request, 'Bike not added. Please check the form inputs.')
    else:
        form = BikeForm()
    return render(request, 'admin_add_bike.html', {'form': form})



 

def delete_bike(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    # Check if the logged-in admin is the one who added the vehicle
    if bike.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this vehicle.')
        return redirect('admin_add_bike')

    if request.method == 'POST':
        bike.delete()
        messages.success(request, 'Vehicle deleted successfully.')
        return redirect('admin_add_bike')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_bike')

# admin_bike_viz_a_list
def admin_bike_viz_a_list(request):
    bikes_viz_a = Bike.objects.filter(location='Vijayawada', station='A Station')

    return render(request, 'admin_bike_viz_a_list.html', {'bikes_viz_a': bikes_viz_a})


# bike_viz_a_list
def bike_viz_a_list(request):
    bikes_viz_a = Bike.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'bike_viz_a_list.html', {'bikes_viz_a': bikes_viz_a})


def admin_bike_viz_b_list(request):
    bikes_viz_b = Bike.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'admin_bike_viz_b_list.html', {'bikes_viz_b': bikes_viz_b})

def bike_viz_b_list(request):
    bikes_viz_b = Bike.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'bike_viz_b_list.html', {'bikes_viz_b': bikes_viz_b})


@login_required
def bike_viz_a_payment(request, bike_id):
    bike = get_object_or_404(Bike, pk=bike_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=bike.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')
            
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=bike.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'bike_viz_a_payment.html', {'bike': bike, 'form': form, 'error_message': error_message})
            
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=bike.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 
                
                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'bike_viz_a_payment.html', {'bike': bike, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})
                
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=bike.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'bike_viz_a_payment.html', {'bike': bike, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = bike.vehicle_id
                payment.vehicle_number = bike.vehicle_number
                payment.vehicle_name = bike.vehicle_name
                # payment.driver_name = bike.driver_name 
                # payment.driver_contact = bike.driver_contact
                payment.driver_cost = 0
                payment.rent_cost = bike.rent_cost
                payment.save()
                bike.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('bike_viz_a_payment', kwargs={'bike_id': bike_id}))  # Redirect with bike_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'bike_viz_a_payment.html', {'bike': bike, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'bike_viz_a_payment.html', {'bike': bike, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm() 
    return render(request, 'bike_viz_a_payment.html', {'bike': bike, 'booked_dates': booked_dates, 'form': form})





@login_required
def bike_viz_b_payment(request, bike_id):
    bike = get_object_or_404(Bike, pk=bike_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=bike.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')
            
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=bike.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'bike_viz_b_payment.html', {'bike': bike, 'form': form, 'error_message': error_message})
            
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=bike.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 
                
                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'bike_viz_b_payment.html', {'bike': bike, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})
                
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=bike.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'bike_viz_b_payment.html', {'bike': bike, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = bike.vehicle_id
                payment.vehicle_number = bike.vehicle_number
                payment.vehicle_name = bike.vehicle_name
                # payment.driver_name = bike.driver_name 
                # payment.driver_contact = bike.driver_contact
                payment.driver_cost = 0
                payment.rent_cost = bike.rent_cost
                payment.save()
                bike.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('bike_viz_b_payment', kwargs={'bike_id': bike_id}))  # Redirect with bike_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'bike_viz_b_payment.html', {'bike': bike, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'bike_viz_b_payment.html', {'bike': bike, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm() 
    return render(request, 'bike_viz_b_payment.html', {'bike': bike, 'booked_dates': booked_dates, 'form': form})






@login_required
def admin_add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']

            if Car.objects.filter(vehicle_id=vehicle_id).exists() or Car.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Car ID or Car Number already exists.')
                return redirect('admin_add_car')

            car = form.save(commit=False)
            car.added_by = request.user
            car.date_added = timezone.now()

            location = request.POST.get('location')
            station = request.POST.get('station')

            # Adjust the logic based on your specific requirements for car locations and stations
            if location == 'Vijayawada' and station == 'A Station':
                car.save()
                messages.success(request, 'Car successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_car')
            elif location == 'Vijayawada' and station == 'B Station':
                car.save()
                messages.success(request, 'Car successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_car')
            elif location == 'Khammam' and station == 'A Station':
                car.save()
                messages.success(request, 'Car successfully added, check in Khammam A Station list.')
                return redirect('admin_add_car')
            elif location == 'Khammam' and station == 'B Station':
                car.save()
                messages.success(request, 'Car successfully added, check in Khammam B Station list.')
                return redirect('admin_add_car')
            else:
                messages.success(request, 'Data is not added in the correct location.')
                return redirect('admin_add_car')
        else:
            messages.error(request, 'Car not added. Please check the form inputs.')
    else:
        form = CarForm()
    return render(request, 'admin_add_car.html', {'form': form})






def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    # Check if the logged-in admin is the one who added the vehicle
    if car.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this vehicle.')
        return redirect('admin_add_car')

    if request.method == 'POST':
        car.delete()
        messages.success(request, 'Vehicle deleted successfully.')
        return redirect('admin_add_car')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_car')
    





# admin_car_viz_a_list
def admin_car_viz_a_list(request):
    cars_viz_a = Car.objects.filter(location='Vijayawada', station='A Station')

    return render(request, 'admin_car_viz_a_list.html', {'cars_viz_a': cars_viz_a})


# car_viz_a_list
def car_viz_a_list(request):
    cars_viz_a = Car.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'car_viz_a_list.html', {'cars_viz_a': cars_viz_a})



def admin_car_viz_b_list(request):
    cars_viz_b = Car.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'admin_car_viz_b_list.html', {'cars_viz_b': cars_viz_b})

def car_viz_b_list(request):
    cars_viz_b = Car.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'car_viz_b_list.html', {'cars_viz_b': cars_viz_b})






@login_required
def car_viz_a_payment(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=car.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')
            
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=car.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'car_viz_a_payment.html', {'car': car, 'form': form, 'error_message': error_message})
            
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=car.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 
                
                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'car_viz_a_payment.html', {'car': car, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})
                
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=car.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'car_viz_a_payment.html', {'car': car, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = car.vehicle_id
                payment.vehicle_number = car.vehicle_number
                payment.vehicle_name = car.vehicle_name
                payment.driver_name = car.driver_name 
                payment.driver_contact = car.driver_contact
                payment.driver_cost = car.driver_cost
                payment.rent_cost = car.rent_cost
                payment.save()
                car.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('car_viz_a_payment', kwargs={'car_id': car_id}))  # Redirect with car_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'car_viz_a_payment.html', {'car': car, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'car_viz_a_payment.html', {'car': car, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm() 
    return render(request, 'car_viz_a_payment.html', {'car': car, 'booked_dates': booked_dates, 'form': form})



@login_required
def car_viz_b_payment(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=car.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')
            
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=car.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'car_viz_b_payment.html', {'car': car, 'form': form, 'error_message': error_message})
            
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=car.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 
                
                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'car_viz_b_payment.html', {'car': car, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})
                
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=car.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'car_viz_b_payment.html', {'car': car, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = car.vehicle_id
                payment.vehicle_number = car.vehicle_number
                payment.vehicle_name = car.vehicle_name
                payment.driver_name = car.driver_name 
                payment.driver_contact = car.driver_contact
                payment.driver_cost = car.driver_cost
                payment.rent_cost = car.rent_cost
                payment.save()
                car.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('car_viz_b_payment', kwargs={'car_id': car_id}))  # Redirect with car_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'car_viz_b_payment.html', {'car': car, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'car_viz_b_payment.html', {'car': car, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm() 
    return render(request, 'car_viz_b_payment.html', {'car': car, 'booked_dates': booked_dates, 'form': form})





#Auto functionalities 

#admin add auto
def admin_add_auto(request): 
    if request.method == 'POST':
        form = AutoForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']
            
            # Check if the entered vehicle ID or vehicle number already exists
            if Auto.objects.filter(vehicle_id=vehicle_id).exists() or Auto.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Vehicle ID or Vehicle Number already exists.')
                return redirect('admin_add_auto')
            auto = form.save(commit=False)
            auto.added_by = request.user  
            auto.date_added = timezone.now()
            
            location = request.POST.get('location')
            station = request.POST.get('station')
            
            if location == 'Vijayawada' and station == 'A Station':
                auto.save()
                messages.success(request, 'Successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_auto')
            elif location == 'Vijayawada' and station == 'B Station':
                auto.save()
                messages.success(request, 'Successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_auto')
            elif location == 'Khammam' and station == 'A Station':
                auto.save()
                messages.success(request, 'Successfully added, check in Khammam A Station list.')
                return redirect('admin_add_auto')
            elif location == 'Khammam' and station == 'B Station':
                auto.save()
                messages.success(request, 'Successfully added, check in Khammam B Station list.')
                return redirect('admin_add_auto')
            else:
                messages.success(request, 'Data is not added in correct location.')
                return redirect('admin_add_auto')
        else:
            messages.error(request, 'Data not added. Please check the form inputs.')
    else:
        form = AutoForm()
    return render(request, 'admin_add_auto.html', {'form': form})


# admin delete auto
def delete_auto(request, auto_id):
    auto = get_object_or_404(Auto, id=auto_id)

    # Check if the logged-in admin is the one who added the vehicle
    if auto.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this vehicle.')
        return redirect('admin_add_auto')

    if request.method == 'POST':
        auto.delete()
        messages.success(request, 'Vehicle deleted successfully.')
        return redirect('admin_add_auto')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_auto')
    


#Auto A
    
#admin auto viz a list
def admin_auto_viz_a_list(request):
    autos_viz_a = Auto.objects.filter(location='Vijayawada', station='A Station')

    return render(request, 'admin_auto_viz_a_list.html', {'autos_viz_a': autos_viz_a})



#auto viz a list
def auto_viz_a_list(request):
    autos_viz_a = Auto.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'auto_viz_a_list.html', {'autos_viz_a': autos_viz_a})



#auto viz a payment
@login_required
def auto_viz_a_payment(request, auto_id):
    auto = Auto.objects.get(pk=auto_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=auto.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')
            # Check for overlapping bookings
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=auto.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )
            if overlapping_bookings.exists():
                # Get the details of the overlapping booking
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
 
                # Prepare the error message with booked timings
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'auto_viz_a_payment.html', {'auto': auto, 'form': form, 'error_message': error_message})
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                # Check again for overlaps before saving the payment
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=auto.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 
                if overlapping_bookings_after_password_check.exists():
                    # If overlaps detected again after password check, show error
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'auto_viz_a_payment.html', {'auto': auto, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})
                

                # Check for 30-minute gap before and after the new booking
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=auto.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'auto_viz_a_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})


                # No overlap after password check, proceed with payment save
                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = auto.vehicle_id
                payment.vehicle_number = auto.vehicle_number
                payment.vehicle_name = auto.vehicle_name
                payment.driver_name = auto.driver_name 
                payment.driver_contact = auto.driver_contact
                payment.driver_cost = auto.driver_cost
                payment.rent_cost = auto.rent_cost
                payment.save()
                auto.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('auto_viz_a_payment', kwargs={'auto_id': auto_id}))  # Redirect with auto_id
            else:
                # Handle incorrect password input
                error_message = "Incorrect password. Please try again."
                return render(request, 'auto_viz_a_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            # Handle form validation errors
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'auto_viz_a_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm() 
    return render(request, 'auto_viz_a_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form})



def get_booked_vehicles_viz_a():
    return PaymentDetails.objects.filter(
        vehicle_id__in=Auto.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Traveller.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Truck.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Tractor.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Jcb.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=BorewellTruck.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=CombineHarvester.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Bike.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Car.objects.filter(location='Vijayawada', station='A Station').values_list('vehicle_id', flat=True)
    )

def admin_staff_common_viz_a_rides(request, template_name, role):
    booked_vehicles_viz_a = get_booked_vehicles_viz_a()
    for booked_vehicle in booked_vehicles_viz_a:
        booked_vehicle.feedback_exists = Feedback.objects.filter(payment__id=booked_vehicle.id).exists()
        booked_vehicle.is_canceled = CancellationReason.objects.filter(payment_id=booked_vehicle.id).exists()

    context = {'booked_vehicles_viz_a': booked_vehicles_viz_a, 'role': role}
    return render(request, template_name, context)

def admin_viz_a_rides(request):
    return admin_staff_common_viz_a_rides(request, 'admin_viz_a_rides.html', 'admin')

def admin_viz_a_rides_graph(request):
    return render(request, 'admin_viz_a_rides_graph.html')

def staff_viz_a_rides(request):
    return admin_staff_common_viz_a_rides(request, 'staff_viz_a_rides.html', 'staff')



#Auto B

def admin_auto_viz_b_list(request):
    autos_viz_b = Auto.objects.filter(location='Vijayawada', station='B Station')

    return render(request, 'admin_auto_viz_b_list.html', {'autos_viz_b': autos_viz_b})

def auto_viz_b_list(request):
    autos_viz_b = Auto.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'auto_viz_b_list.html', {'autos_viz_b': autos_viz_b})


 

@login_required
def auto_viz_b_payment(request, auto_id):
    auto = Auto.objects.get(pk=auto_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=auto.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            # Check for overlapping bookings
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=auto.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                # Get the details of the overlapping booking
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime

                # Prepare the error message with booked timings
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'auto_viz_b_payment.html', {'auto': auto, 'form': form, 'error_message': error_message})
            
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                # Check again for overlaps before saving the payment
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=auto.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    # If overlaps detected again after password check, show error
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'auto_viz_b_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
                


                # Check for 30-minute gap before and after the new booking
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=auto.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'auto_viz_b_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
                


                # No overlap after password check, proceed with payment save
                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = auto.vehicle_id
                payment.vehicle_number = auto.vehicle_number
                payment.vehicle_name = auto.vehicle_name
                payment.driver_name = auto.driver_name 
                payment.driver_contact = auto.driver_contact
                payment.driver_cost = auto.driver_cost
                payment.rent_cost = auto.rent_cost
                payment.save()
                auto.update_status("In work, Available after some time")

                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('auto_viz_b_payment', kwargs={'auto_id': auto_id}))  # Redirect with auto_id
            else:
                # Handle incorrect password input
                error_message = "Incorrect password. Please try again."
                return render(request, 'auto_viz_b_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            # Handle form validation errors
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'auto_viz_b_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()

    return render(request, 'auto_viz_b_payment.html', {'auto': auto, 'booked_dates': booked_dates, 'form': form})



def get_booked_vehicles_viz_b():
    return PaymentDetails.objects.filter(
        vehicle_id__in=Auto.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Traveller.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Tractor.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Jcb.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=BorewellTruck.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Truck.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=CombineHarvester.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Bike.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    ) | PaymentDetails.objects.filter(
        vehicle_id__in=Car.objects.filter(location='Vijayawada', station='B Station').values_list('vehicle_id', flat=True)
    )  


def admin_staff_common_viz_b_rides(request, template_name, role):
    booked_vehicles_viz_b = get_booked_vehicles_viz_b()
    for booked_vehicle in booked_vehicles_viz_b:
        booked_vehicle.feedback_exists = Feedback.objects.filter(payment__id=booked_vehicle.id).exists()
        booked_vehicle.is_canceled = CancellationReason.objects.filter(payment_id=booked_vehicle.id).exists()

    context = {'booked_vehicles_viz_b': booked_vehicles_viz_b, 'role': role}
    return render(request, template_name, context)

def admin_viz_b_rides(request):
    return admin_staff_common_viz_b_rides(request, 'admin_viz_b_rides.html', 'admin')

def staff_viz_b_rides(request):
    return admin_staff_common_viz_b_rides(request, 'staff_viz_b_rides.html', 'staff')






def admin_add_traveller(request): 
    if request.method == 'POST':
        form = TravellerForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']
            
            # Check if the entered vehicle ID or vehicle number already exists
            if Traveller.objects.filter(vehicle_id=vehicle_id).exists() or Traveller.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Vehicle ID or Vehicle Number already exists.')
                return redirect('admin_add_traveller')
            traveller = form.save(commit=False)
            traveller.added_by = request.user  
            traveller.date_added = timezone.now()
            
            location = request.POST.get('location')
            station = request.POST.get('station')
            
            if location == 'Vijayawada' and station == 'A Station':
                traveller.save()
                messages.success(request, 'Successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_traveller')
            elif location == 'Vijayawada' and station == 'B Station':
                traveller.save()
                messages.success(request, 'Successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_traveller')
            elif location == 'Khammam' and station == 'A Station':
                traveller.save()
                messages.success(request, 'Successfully added, check in Khammam A Station list.')
                return redirect('admin_add_traveller')
            elif location == 'Khammam' and station == 'B Station':
                traveller.save()
                messages.success(request, 'Successfully added, check in Khammam B Station list.')
                return redirect('admin_add_traveller')
            else:
                messages.success(request, 'Data is not added in correct location.')
                return redirect('admin_add_traveller')
        else:
            messages.error(request, 'Data not added. Please check the form inputs.')
    else:
        form = TravellerForm()
    return render(request, 'admin_add_traveller.html', {'form': form})


def delete_traveller(request, traveller_id):
    traveller = get_object_or_404(Traveller, id=traveller_id)

    # Check if the logged-in admin is the one who added the vehicle
    if traveller.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this vehicle.')
        return redirect('admin_add_traveller')

    if request.method == 'POST':
        traveller.delete()
        messages.success(request, 'Vehicle deleted successfully.')
        return redirect('admin_add_traveller')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_traveller')
 

def admin_traveller_viz_a_list(request):
    travellers_viz_a = Traveller.objects.filter(location='Vijayawada', station='A Station')

    return render(request, 'admin_traveller_viz_a_list.html', {'travellers_viz_a': travellers_viz_a})

def admin_traveller_viz_b_list(request):
    travellers_viz_b = Traveller.objects.filter(location='Vijayawada', station='B Station')

    return render(request, 'admin_traveller_viz_b_list.html', {'travellers_viz_b': travellers_viz_b})

def traveller_viz_a_list(request):
    travellers_viz_a = Traveller.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'traveller_viz_a_list.html', {'travellers_viz_a': travellers_viz_a})

def traveller_viz_b_list(request):
    travellers_viz_b = Traveller.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'traveller_viz_b_list.html', {'travellers_viz_b': travellers_viz_b})


@login_required
def traveller_viz_a_payment(request, traveller_id):
    traveller = Traveller.objects.get(pk=traveller_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=traveller.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')
            
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=traveller.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'traveller_viz_a_payment.html', {'traveller': traveller, 'form': form, 'error_message': error_message})
            
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=traveller.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 
                
                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'traveller_viz_a_payment.html', {'traveller': traveller, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})
                
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=traveller.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'traveller_viz_a_payment.html', {'traveller': traveller, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = traveller.vehicle_id
                payment.vehicle_number = traveller.vehicle_number
                payment.vehicle_name = traveller.vehicle_name
                payment.driver_name = traveller.driver_name 
                payment.driver_contact = traveller.driver_contact
                payment.driver_cost = traveller.driver_cost
                payment.rent_cost = traveller.rent_cost
                payment.save()
                traveller.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('traveller_viz_a_payment', kwargs={'traveller_id': traveller_id}))  # Redirect with traveller_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'traveller_viz_a_payment.html', {'traveller': traveller, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'traveller_viz_a_payment.html', {'traveller': traveller, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm() 
    return render(request, 'traveller_viz_a_payment.html', {'traveller': traveller, 'booked_dates': booked_dates, 'form': form})




@login_required
def traveller_viz_b_payment(request, traveller_id):
    traveller = Traveller.objects.get(pk=traveller_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=traveller.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=traveller.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'traveller_viz_b_payment.html', {'traveller': traveller, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=traveller.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'traveller_viz_b_payment.html', {'traveller': traveller, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=traveller.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'traveller_viz_b_payment.html', {'traveller': traveller, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = traveller.vehicle_id
                payment.vehicle_number = traveller.vehicle_number
                payment.vehicle_name = traveller.vehicle_name
                payment.driver_name = traveller.driver_name 
                payment.driver_contact = traveller.driver_contact
                payment.driver_cost = traveller.driver_cost
                payment.rent_cost = traveller.rent_cost
                payment.save()
                traveller.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('traveller_viz_b_payment', kwargs={'traveller_id': traveller_id}))  # Redirect with traveller_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'traveller_viz_b_payment.html', {'traveller': traveller, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'traveller_viz_b_payment.html', {'traveller': traveller, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()

    return render(request, 'traveller_viz_b_payment.html', {'traveller': traveller, 'booked_dates': booked_dates, 'form': form})


def admin_add_truck(request): 
    if request.method == 'POST':
        form = TruckForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']
            
            if Truck.objects.filter(vehicle_id=vehicle_id).exists() or Truck.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Truck ID or Truck Number already exists.')
                return redirect('admin_add_truck')
            truck = form.save(commit=False)
            truck.added_by = request.user  
            truck.date_added = timezone.now()
            
            location = request.POST.get('location')
            station = request.POST.get('station')
            
            # Adjust the logic based on your specific requirements for truck locations and stations
            if location == 'Vijayawada' and station == 'A Station':
                truck.save()
                messages.success(request, 'Truck successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_truck')
            elif location == 'Vijayawada' and station == 'B Station':
                truck.save()
                messages.success(request, 'Truck successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_truck')
            elif location == 'Khammam' and station == 'A Station':
                truck.save()
                messages.success(request, 'Truck successfully added, check in Khammam A Station list.')
                return redirect('admin_add_truck')
            elif location == 'Khammam' and station == 'B Station':
                truck.save()
                messages.success(request, 'Truck successfully added, check in Khammam B Station list.')
                return redirect('admin_add_truck')
            else:
                messages.success(request, 'Data is not added in the correct location.')
                return redirect('admin_add_truck')
        else:
            messages.error(request, 'Truck not added. Please check the form inputs.')
    else:
        form = TruckForm()
    return render(request, 'admin_add_truck.html', {'form': form})


def delete_truck(request, truck_id):
    truck = get_object_or_404(Truck, id=truck_id)

    if truck.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this truck.')
        return redirect('admin_add_truck')

    if request.method == 'POST':
        truck.delete()
        messages.success(request, 'Truck deleted successfully.')
        return redirect('admin_add_truck')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_truck')





def admin_truck_viz_a_list(request):
    trucks_viz_a = Truck.objects.filter(location='Vijayawada', station='A Station')

    return render(request, 'admin_truck_viz_a_list.html', {'trucks_viz_a': trucks_viz_a})

def admin_truck_viz_b_list(request):
    trucks_viz_b = Truck.objects.filter(location='Vijayawada', station='B Station')

    return render(request, 'admin_truck_viz_b_list.html', {'trucks_viz_b': trucks_viz_b})

def admin_truck_khm_a_list(request):
    trucks_khm_a = Truck.objects.filter(location='Khammam', station='A Station')

    return render(request, 'admin_truck_khm_a_list.html', {'trucks_khm_a': trucks_khm_a})

def admin_truck_khm_b_list(request):
    trucks_khm_b = Truck.objects.filter(location='Khammam', station='B Station')

    return render(request, 'admin_truck_khm_b_list.html', {'trucks_khm_b': trucks_khm_b})

def truck_viz_a_list(request):
    trucks_viz_a = Truck.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'truck_viz_a_list.html', {'trucks_viz_a': trucks_viz_a})

def truck_viz_b_list(request):
    trucks_viz_b = Truck.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'truck_viz_b_list.html', {'trucks_viz_b': trucks_viz_b})



@login_required
def truck_viz_a_payment(request, truck_id):
    truck = Truck.objects.get(pk=truck_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=truck.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')
            
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=truck.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'truck_viz_a_payment.html', {'truck': truck, 'form': form, 'error_message': error_message})
            
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=truck.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 
                
                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'truck_viz_a_payment.html', {'truck': truck, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})
                
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=truck.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'truck_viz_a_payment.html', {'truck': truck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = truck.vehicle_id
                payment.vehicle_number = truck.vehicle_number
                payment.vehicle_name = truck.vehicle_name
                payment.driver_name = truck.driver_name 
                payment.driver_contact = truck.driver_contact
                payment.driver_cost = truck.driver_cost
                payment.rent_cost = truck.rent_cost
                payment.save()
                truck.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('truck_viz_a_payment', kwargs={'truck_id': truck_id}))  # Redirect with truck_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'truck_viz_a_payment.html', {'truck': truck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'truck_viz_a_payment.html', {'truck': truck, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm() 
    return render(request, 'truck_viz_a_payment.html', {'truck': truck, 'booked_dates': booked_dates, 'form': form})


@login_required
def truck_viz_b_payment(request, truck_id):
    truck = Truck.objects.get(pk=truck_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=truck.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')
            
            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=truck.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'truck_viz_b_payment.html', {'truck': truck, 'form': form, 'error_message': error_message})
            
            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=truck.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                ) 
                
                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'truck_viz_b_payment.html', {'truck': truck, 'booked_dates': booked_dates,'form': form, 'error_message': error_message})
                
                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=truck.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'truck_viz_b_payment.html', {'truck': truck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = truck.vehicle_id
                payment.vehicle_number = truck.vehicle_number
                payment.vehicle_name = truck.vehicle_name
                payment.driver_name = truck.driver_name 
                payment.driver_contact = truck.driver_contact
                payment.driver_cost = truck.driver_cost
                payment.rent_cost = truck.rent_cost
                payment.save()
                truck.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('truck_viz_b_payment', kwargs={'truck_id': truck_id}))  # Redirect with truck_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'truck_viz_b_payment.html', {'truck': truck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'truck_viz_b_payment.html', {'truck': truck, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm() 
    return render(request, 'truck_viz_b_payment.html', {'truck': truck, 'booked_dates': booked_dates, 'form': form})





@login_required
def admin_add_tractor(request): 
    if request.method == 'POST':
        form = TractorForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']
            
            if Tractor.objects.filter(vehicle_id=vehicle_id).exists() or Tractor.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Tractor ID or Tractor Number already exists.')
                return redirect('admin_add_tractor')
            tractor = form.save(commit=False)
            tractor.added_by = request.user  
            tractor.date_added = timezone.now()
            
            location = request.POST.get('location')
            station = request.POST.get('station')
            
            # Adjust the logic based on your specific requirements for tractor locations and stations
            if location == 'Vijayawada' and station == 'A Station':
                tractor.save()
                messages.success(request, 'Tractor successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_tractor')
            elif location == 'Vijayawada' and station == 'B Station':
                tractor.save()
                messages.success(request, 'Tractor successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_tractor')
            elif location == 'Khammam' and station == 'A Station':
                tractor.save()
                messages.success(request, 'Tractor successfully added, check in Khammam A Station list.')
                return redirect('admin_add_tractor')
            elif location == 'Khammam' and station == 'B Station':
                tractor.save()
                messages.success(request, 'Tractor successfully added, check in Khammam B Station list.')
                return redirect('admin_add_tractor')
            else:
                messages.success(request, 'Data is not added in the correct location.')
                return redirect('admin_add_tractor')
        else:
            messages.error(request, 'Tractor not added. Please check the form inputs.')
    else:
        form = TractorForm()
    return render(request, 'admin_add_tractor.html', {'form': form})




def delete_tractor(request, tractor_id):
    tractor = get_object_or_404(Tractor, id=tractor_id)

    if tractor.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this Tractor.')
        return redirect('admin_add_tractor')

    if request.method == 'POST':
        tractor.delete()
        messages.success(request, 'Tractor deleted successfully.')
        return redirect('admin_add_tractor')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_tractor')




def admin_tractor_viz_a_list(request):
    tractors_viz_a = Tractor.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'admin_tractor_viz_a_list.html', {'tractors_viz_a': tractors_viz_a})

def admin_tractor_viz_b_list(request):
    tractors_viz_b = Tractor.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'admin_tractor_viz_b_list.html', {'tractors_viz_b': tractors_viz_b})

def admin_tractor_khm_a_list(request):
    tractors_khm_a = Tractor.objects.filter(location='Khammam', station='A Station')
    return render(request, 'admin_tractor_khm_a_list.html', {'tractors_khm_a': tractors_khm_a})

def admin_tractor_khm_b_list(request):
    tractors_khm_b = Tractor.objects.filter(location='Khammam', station='B Station')
    return render(request, 'admin_tractor_khm_b_list.html', {'tractors_khm_b': tractors_khm_b})

def tractor_viz_a_list(request):
    tractors_viz_a = Tractor.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'tractor_viz_a_list.html', {'tractors_viz_a': tractors_viz_a})

def tractor_viz_b_list(request):
    tractors_viz_b = Tractor.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'tractor_viz_b_list.html', {'tractors_viz_b': tractors_viz_b})


@login_required
def tractor_viz_a_payment(request, tractor_id):
    tractor = Tractor.objects.get(pk=tractor_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=tractor.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=tractor.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'tractor_viz_a_payment.html', {'tractor': tractor, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=tractor.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'tractor_viz_a_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=tractor.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'tractor_viz_a_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = tractor.vehicle_id
                payment.vehicle_number = tractor.vehicle_number
                payment.vehicle_name = tractor.vehicle_name
                payment.driver_name = tractor.driver_name
                payment.driver_contact = tractor.driver_contact
                payment.driver_cost = tractor.driver_cost
                payment.rent_cost = tractor.rent_cost
                payment.save()
                tractor.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('tractor_viz_a_payment', kwargs={'tractor_id': tractor_id}))  # Redirect with tractor_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'tractor_viz_a_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'tractor_viz_a_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()
    return render(request, 'tractor_viz_a_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form})



@login_required
def tractor_viz_b_payment(request, tractor_id):
    tractor = Tractor.objects.get(pk=tractor_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=tractor.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=tractor.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'tractor_viz_b_payment.html', {'tractor': tractor, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=tractor.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'tractor_viz_b_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=tractor.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'tractor_viz_b_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = tractor.vehicle_id
                payment.vehicle_number = tractor.vehicle_number
                payment.vehicle_name = tractor.vehicle_name
                payment.driver_name = tractor.driver_name
                payment.driver_contact = tractor.driver_contact
                payment.driver_cost = tractor.driver_cost
                payment.rent_cost = tractor.rent_cost
                payment.save()
                tractor.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('tractor_viz_b_payment', kwargs={'tractor_id': tractor_id}))  # Redirect with tractor_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'tractor_viz_b_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'tractor_viz_b_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()
    return render(request, 'tractor_viz_b_payment.html', {'tractor': tractor, 'booked_dates': booked_dates, 'form': form})









@login_required
def admin_add_jcb(request): 
    if request.method == 'POST':
        form = JcbForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']
            
            if Jcb.objects.filter(vehicle_id=vehicle_id).exists() or Jcb.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'JCB ID or JCB Number already exists.')
                return redirect('admin_add_jcb')
            jcb = form.save(commit=False)
            jcb.added_by = request.user  
            jcb.date_added = timezone.now()
            
            location = request.POST.get('location')
            station = request.POST.get('station')
            
            # Adjust the logic based on your specific requirements for JCB locations and stations
            if location == 'Vijayawada' and station == 'A Station':
                jcb.save()
                messages.success(request, 'JCB successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_jcb')
            elif location == 'Vijayawada' and station == 'B Station':
                jcb.save()
                messages.success(request, 'JCB successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_jcb')
            elif location == 'Khammam' and station == 'A Station':
                jcb.save()
                messages.success(request, 'JCB successfully added, check in Khammam A Station list.')
                return redirect('admin_add_jcb')
            elif location == 'Khammam' and station == 'B Station':
                jcb.save()
                messages.success(request, 'JCB successfully added, check in Khammam B Station list.')
                return redirect('admin_add_jcb')
            else:
                messages.success(request, 'Data is not added in the correct location.')
                return redirect('admin_add_jcb')
        else:
            messages.error(request, 'JCB not added. Please check the form inputs.')
    else:
        form = JcbForm()
    return render(request, 'admin_add_jcb.html', {'form': form})






def delete_jcb(request, jcb_id):
    jcb = get_object_or_404(Jcb, id=jcb_id)

    if jcb.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this JCB.')
        return redirect('admin_add_jcb')

    if request.method == 'POST':
        jcb.delete()
        messages.success(request, 'JCB deleted successfully.')
        return redirect('admin_add_jcb')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_jcb')





def admin_jcb_viz_a_list(request):
    jcbs_viz_a = Jcb.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'admin_jcb_viz_a_list.html', {'jcbs_viz_a': jcbs_viz_a})

def admin_jcb_viz_b_list(request):
    jcbs_viz_b = Jcb.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'admin_jcb_viz_b_list.html', {'jcbs_viz_b': jcbs_viz_b})

def admin_jcb_khm_a_list(request):
    jcbs_khm_a = Jcb.objects.filter(location='Khammam', station='A Station')
    return render(request, 'admin_jcb_khm_a_list.html', {'jcbs_khm_a': jcbs_khm_a})

def admin_jcb_khm_b_list(request):
    jcbs_khm_b = Jcb.objects.filter(location='Khammam', station='B Station')
    return render(request, 'admin_jcb_khm_b_list.html', {'jcbs_khm_b': jcbs_khm_b})

def jcb_viz_a_list(request):
    jcbs_viz_a = Jcb.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'jcb_viz_a_list.html', {'jcbs_viz_a': jcbs_viz_a})

def jcb_viz_b_list(request):
    jcbs_viz_b = Jcb.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'jcb_viz_b_list.html', {'jcbs_viz_b': jcbs_viz_b})








@login_required
def jcb_viz_a_payment(request, jcb_id):
    jcb = Jcb.objects.get(pk=jcb_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=jcb.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=jcb.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'jcb_viz_a_payment.html', {'jcb': jcb, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=jcb.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'jcb_viz_a_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=jcb.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'jcb_viz_a_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = jcb.vehicle_id
                payment.vehicle_number = jcb.vehicle_number
                payment.vehicle_name = jcb.vehicle_name
                payment.driver_name = jcb.driver_name
                payment.driver_contact = jcb.driver_contact
                payment.driver_cost = jcb.driver_cost
                payment.rent_cost = jcb.rent_cost
                payment.save()
                jcb.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('jcb_viz_a_payment', kwargs={'jcb_id': jcb_id}))  # Redirect with jcb_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'jcb_viz_a_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'jcb_viz_a_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()
    return render(request, 'jcb_viz_a_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form})





@login_required
def jcb_viz_b_payment(request, jcb_id):
    jcb = Jcb.objects.get(pk=jcb_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=jcb.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=jcb.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'jcb_viz_b_payment.html', {'jcb': jcb, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=jcb.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'jcb_viz_b_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=jcb.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'jcb_viz_b_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = jcb.vehicle_id
                payment.vehicle_number = jcb.vehicle_number
                payment.vehicle_name = jcb.vehicle_name
                payment.driver_name = jcb.driver_name
                payment.driver_contact = jcb.driver_contact
                payment.driver_cost = jcb.driver_cost
                payment.rent_cost = jcb.rent_cost
                payment.save()
                jcb.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('jcb_viz_b_payment', kwargs={'jcb_id': jcb_id}))  # Redirect with jcb_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'jcb_viz_b_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'jcb_viz_b_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()
    return render(request, 'jcb_viz_b_payment.html', {'jcb': jcb, 'booked_dates': booked_dates, 'form': form})










@login_required
def admin_add_borewelltruck(request): 
    if request.method == 'POST':
        form = BorewellTruckForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']
            
            if BorewellTruck.objects.filter(vehicle_id=vehicle_id).exists() or BorewellTruck.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Borewell Truck ID or Borewell Truck Number already exists.')
                return redirect('admin_add_borewelltruck')
            borewell_truck = form.save(commit=False)
            borewell_truck.added_by = request.user  
            borewell_truck.date_added = timezone.now()
            
            location = request.POST.get('location')
            station = request.POST.get('station')
            
            # Adjust the logic based on your specific requirements for Borewell Truck locations and stations
            if location == 'Vijayawada' and station == 'A Station':
                borewell_truck.save()
                messages.success(request, 'Borewell Truck successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_borewelltruck')
            elif location == 'Vijayawada' and station == 'B Station':
                borewell_truck.save()
                messages.success(request, 'Borewell Truck successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_borewelltruck')
            elif location == 'Khammam' and station == 'A Station':
                borewell_truck.save()
                messages.success(request, 'Borewell Truck successfully added, check in Khammam A Station list.')
                return redirect('admin_add_borewelltruck')
            elif location == 'Khammam' and station == 'B Station':
                borewell_truck.save()
                messages.success(request, 'Borewell Truck successfully added, check in Khammam B Station list.')
                return redirect('admin_add_borewelltruck')
            else:
                messages.success(request, 'Data is not added in the correct location.')
                return redirect('admin_add_borewelltruck')
        else:
            messages.error(request, 'Borewell Truck not added. Please check the form inputs.')
    else:
        form = BorewellTruckForm()
    return render(request, 'admin_add_borewelltruck.html', {'form': form})



def delete_borewelltruck(request, borewelltruck_id):
    borewelltruck = get_object_or_404(BorewellTruck, id=borewelltruck_id)

    if borewelltruck.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this BorewellTruck.')
        return redirect('admin_add_borewelltruck')

    if request.method == 'POST':
        borewelltruck.delete()
        messages.success(request, 'BorewellTruck deleted successfully.')
        return redirect('admin_add_borewelltruck')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_borewelltruck')



def admin_borewelltruck_viz_a_list(request):
    borewelltrucks_viz_a = BorewellTruck.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'admin_borewelltruck_viz_a_list.html', {'borewelltrucks_viz_a': borewelltrucks_viz_a})

def admin_borewelltruck_viz_b_list(request):
    borewelltrucks_viz_b = BorewellTruck.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'admin_borewelltruck_viz_b_list.html', {'borewelltrucks_viz_b': borewelltrucks_viz_b})

def admin_borewelltruck_khm_a_list(request):
    borewelltrucks_khm_a = BorewellTruck.objects.filter(location='Khammam', station='A Station')
    return render(request, 'admin_borewelltruck_khm_a_list.html', {'borewelltrucks_khm_a': borewelltrucks_khm_a})

def admin_borewelltruck_khm_b_list(request):
    borewelltrucks_khm_b = BorewellTruck.objects.filter(location='Khammam', station='B Station')
    return render(request, 'admin_borewelltruck_khm_b_list.html', {'borewelltrucks_khm_b': borewelltrucks_khm_b})

def borewelltruck_viz_a_list(request):
    borewelltrucks_viz_a = BorewellTruck.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'borewelltruck_viz_a_list.html', {'borewelltrucks_viz_a': borewelltrucks_viz_a})

def borewelltruck_viz_b_list(request):
    borewelltrucks_viz_b = BorewellTruck.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'borewelltruck_viz_b_list.html', {'borewelltrucks_viz_b': borewelltrucks_viz_b})






@login_required
def borewelltruck_viz_a_payment(request, borewelltruck_id):
    borewelltruck = BorewellTruck.objects.get(pk=borewelltruck_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=borewelltruck.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=borewelltruck.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'borewelltruck_viz_a_payment.html', {'borewelltruck': borewelltruck, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=borewelltruck.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'borewelltruck_viz_a_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=borewelltruck.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'borewelltruck_viz_a_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = borewelltruck.vehicle_id
                payment.vehicle_number = borewelltruck.vehicle_number
                payment.vehicle_name = borewelltruck.vehicle_name
                payment.driver_name = borewelltruck.driver_name
                payment.driver_contact = borewelltruck.driver_contact
                payment.driver_cost = borewelltruck.driver_cost
                payment.rent_cost = borewelltruck.rent_cost
                payment.save()
                borewelltruck.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('borewelltruck_viz_a_payment', kwargs={'borewelltruck_id': borewelltruck_id}))  # Redirect with borewelltruck_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'borewelltruck_viz_a_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'borewelltruck_viz_a_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()
    return render(request, 'borewelltruck_viz_a_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form})




@login_required
def borewelltruck_viz_b_payment(request, borewelltruck_id):
    borewelltruck = BorewellTruck.objects.get(pk=borewelltruck_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=borewelltruck.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=borewelltruck.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'borewelltruck_viz_b_payment.html', {'borewelltruck': borewelltruck, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=borewelltruck.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'borewelltruck_viz_b_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=borewelltruck.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'borewelltruck_viz_b_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = borewelltruck.vehicle_id
                payment.vehicle_number = borewelltruck.vehicle_number
                payment.vehicle_name = borewelltruck.vehicle_name
                payment.driver_name = borewelltruck.driver_name
                payment.driver_contact = borewelltruck.driver_contact
                payment.driver_cost = borewelltruck.driver_cost
                payment.rent_cost = borewelltruck.rent_cost
                payment.save()
                borewelltruck.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('borewelltruck_viz_b_payment', kwargs={'borewelltruck_id': borewelltruck_id}))  # Redirect with borewelltruck_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'borewelltruck_viz_b_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'borewelltruck_viz_b_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()
    return render(request, 'borewelltruck_viz_b_payment.html', {'borewelltruck': borewelltruck, 'booked_dates': booked_dates, 'form': form})





@login_required
def admin_add_combineharvester(request): 
    if request.method == 'POST':
        form = CombineHarvesterForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle_id = form.cleaned_data['vehicle_id']
            vehicle_number = form.cleaned_data['vehicle_number']
            
            if CombineHarvester.objects.filter(vehicle_id=vehicle_id).exists() or CombineHarvester.objects.filter(vehicle_number=vehicle_number).exists():
                messages.error(request, 'Combine Harvester ID or Combine Harvester Number already exists.')
                return redirect('admin_add_combineharvester')
            combine_harvester = form.save(commit=False)
            combine_harvester.added_by = request.user  
            combine_harvester.date_added = timezone.now()
            
            location = request.POST.get('location')
            station = request.POST.get('station')
            
            # Adjust the logic based on your specific requirements for Combine Harvester locations and stations
            if location == 'Vijayawada' and station == 'A Station':
                combine_harvester.save()
                messages.success(request, 'Combine Harvester successfully added, check in Vijayawada A Station list.')
                return redirect('admin_add_combineharvester')
            elif location == 'Vijayawada' and station == 'B Station':
                combine_harvester.save()
                messages.success(request, 'Combine Harvester successfully added, check in Vijayawada B Station list.')
                return redirect('admin_add_combineharvester')
            elif location == 'Khammam' and station == 'A Station':
                combine_harvester.save()
                messages.success(request, 'Combine Harvester successfully added, check in Khammam A Station list.')
                return redirect('admin_add_combineharvester')
            elif location == 'Khammam' and station == 'B Station':
                combine_harvester.save()
                messages.success(request, 'Combine Harvester successfully added, check in Khammam B Station list.')
                return redirect('admin_add_combineharvester')
            else:
                messages.success(request, 'Data is not added in the correct location.')
                return redirect('admin_add_combineharvester')
        else:
            messages.error(request, 'Combine Harvester not added. Please check the form inputs.')
    else:
        form = CombineHarvesterForm()
    return render(request, 'admin_add_combineharvester.html', {'form': form})



def delete_combineharvester(request, combineharvester_id):
    combineharvester = get_object_or_404(CombineHarvester, id=combineharvester_id)

    if combineharvester.added_by != request.user:
        messages.error(request, 'You do not have permission to delete this CombineHarvester.')
        return redirect('admin_add_combineharvester')

    if request.method == 'POST':
        combineharvester.delete()
        messages.success(request, 'CombineHarvester deleted successfully.')
        return redirect('admin_add_combineharvester')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect('admin_add_combineharvester')




def admin_combineharvester_viz_a_list(request):
    combineharvesters_viz_a = CombineHarvester.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'admin_combineharvester_viz_a_list.html', {'combineharvesters_viz_a': combineharvesters_viz_a})

def admin_combineharvester_viz_b_list(request):
    combineharvesters_viz_b = CombineHarvester.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'admin_combineharvester_viz_b_list.html', {'combineharvesters_viz_b': combineharvesters_viz_b})

def admin_combineharvester_khm_a_list(request):
    combineharvesters_khm_a = CombineHarvester.objects.filter(location='Khammam', station='A Station')
    return render(request, 'admin_combineharvester_khm_a_list.html', {'combineharvesters_khm_a': combineharvesters_khm_a})

def admin_combineharvester_khm_b_list(request):
    combineharvesters_khm_b = CombineHarvester.objects.filter(location='Khammam', station='B Station')
    return render(request, 'admin_combineharvester_khm_b_list.html', {'combineharvesters_khm_b': combineharvesters_khm_b})

def combineharvester_viz_a_list(request):
    combineharvesters_viz_a = CombineHarvester.objects.filter(location='Vijayawada', station='A Station')
    return render(request, 'combineharvester_viz_a_list.html', {'combineharvesters_viz_a': combineharvesters_viz_a})

def combineharvester_viz_b_list(request):
    combineharvesters_viz_b = CombineHarvester.objects.filter(location='Vijayawada', station='B Station')
    return render(request, 'combineharvester_viz_b_list.html', {'combineharvesters_viz_b': combineharvesters_viz_b})






@login_required
def combineharvester_viz_a_payment(request, combineharvester_id):
    combineharvester = CombineHarvester.objects.get(pk=combineharvester_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=combineharvester.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=combineharvester.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'combineharvester_viz_a_payment.html', {'combineharvester': combineharvester, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=combineharvester.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'combineharvester_viz_a_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=combineharvester.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'combineharvester_viz_a_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = combineharvester.vehicle_id
                payment.vehicle_number = combineharvester.vehicle_number
                payment.vehicle_name = combineharvester.vehicle_name
                payment.driver_name = combineharvester.driver_name
                payment.driver_contact = combineharvester.driver_contact
                payment.driver_cost = combineharvester.driver_cost
                payment.rent_cost = combineharvester.rent_cost
                payment.save()
                combineharvester.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('combineharvester_viz_a_payment', kwargs={'combineharvester_id': combineharvester_id}))  # Redirect with combineharvester_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'combineharvester_viz_a_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'combineharvester_viz_a_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()
    return render(request, 'combineharvester_viz_a_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form})










@login_required
def combineharvester_viz_b_payment(request, combineharvester_id):
    combineharvester = CombineHarvester.objects.get(pk=combineharvester_id)
    booked_dates = PaymentDetails.objects.filter(
        vehicle_id=combineharvester.vehicle_id,
        ride_completed=False
    ).values_list('start_datetime', 'end_datetime')

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            start_datetime = form.cleaned_data.get('start_datetime')
            end_datetime = form.cleaned_data.get('end_datetime')

            overlapping_bookings = PaymentDetails.objects.filter(
                vehicle_id=combineharvester.vehicle_id,
                end_datetime__gt=start_datetime,
                start_datetime__lt=end_datetime
            )

            if overlapping_bookings.exists():
                overlapping_booking = overlapping_bookings.first()
                booked_start = overlapping_booking.start_datetime
                booked_end = overlapping_booking.end_datetime
                error_message = (
                    f"Selected timings overlap with an existing booking. Please select another date or timings. "
                    f"Booked timings: Start - {booked_start}, End - {booked_end}"
                )
                return render(request, 'combineharvester_viz_b_payment.html', {'combineharvester': combineharvester, 'form': form, 'error_message': error_message})

            entered_password = form.cleaned_data.get('password')
            if request.user.check_password(entered_password):
                overlapping_bookings_after_password_check = PaymentDetails.objects.filter(
                    vehicle_id=combineharvester.vehicle_id,
                    end_datetime__gt=start_datetime,
                    start_datetime__lt=end_datetime
                )

                if overlapping_bookings_after_password_check.exists():
                    error_message = "Selected timings were booked by another user. Please choose different timings."
                    return render(request, 'combineharvester_viz_b_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                min_gap = timedelta(minutes=30)
                previous_bookings = PaymentDetails.objects.filter(
                    vehicle_id=combineharvester.vehicle_id,
                    end_datetime__gt=start_datetime - min_gap,
                    start_datetime__lt=end_datetime + min_gap
                )

                if previous_bookings.exists():
                    error_message = "There must be a 30-minute gap between bookings. Please choose different timings."
                    return render(request, 'combineharvester_viz_b_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})

                payment = form.save(commit=False)
                payment.user_name = request.user.username
                payment.user = request.user
                payment.vehicle_id = combineharvester.vehicle_id
                payment.vehicle_number = combineharvester.vehicle_number
                payment.vehicle_name = combineharvester.vehicle_name
                payment.driver_name = combineharvester.driver_name
                payment.driver_contact = combineharvester.driver_contact
                payment.driver_cost = combineharvester.driver_cost
                payment.rent_cost = combineharvester.rent_cost
                payment.save()
                combineharvester.update_status("In work, Check Schedule and continue")
                messages.success(request, 'Vehicle booked successfully!')
                return redirect(reverse('combineharvester_viz_b_payment', kwargs={'combineharvester_id': combineharvester_id}))  # Redirect with combineharvester_id
            else:
                error_message = "Incorrect password. Please try again."
                return render(request, 'combineharvester_viz_b_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid form input. Please check your entries."
            return render(request, 'combineharvester_viz_b_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form})
    else:
        form = PaymentForm()
    return render(request, 'combineharvester_viz_b_payment.html', {'combineharvester': combineharvester, 'booked_dates': booked_dates, 'form': form})




























@login_required
def user_bookings(request):
    if request.user.is_authenticated:
        user_bookings = PaymentDetails.objects.filter(user=request.user)

        for booking in user_bookings:

            if booking.vehicle_id.startswith('T'):
                try:
                    traveller_info = Traveller.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = traveller_info.vehicle_name
                    booking.rent_cost = traveller_info.rent_cost
                    booking.location = traveller_info.location
                    booking.station = traveller_info.station
                    booking.driver_cost = traveller_info.driver_cost
                except Traveller.DoesNotExist:
                    messages.error(request, f"Traveller with vehicle_id {booking.vehicle_id} does not exist.")


            elif booking.vehicle_id.startswith('A'):
                try:
                    auto_info = Auto.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = auto_info.vehicle_name
                    booking.rent_cost = auto_info.rent_cost
                    booking.location = auto_info.location
                    booking.station = auto_info.station
                    booking.driver_cost = auto_info.driver_cost
                except Auto.DoesNotExist:
                    messages.error(request, f"Auto with vehicle_id {booking.vehicle_id} does not exist.")


            elif booking.vehicle_id.startswith('TRK'):  
                try:
                    truck_info = Truck.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = truck_info.vehicle_name
                    booking.rent_cost = truck_info.rent_cost
                    booking.location = truck_info.location
                    booking.station = truck_info.station
                    booking.driver_cost = truck_info.driver_cost
                except Truck.DoesNotExist:
                    messages.error(request, f"Truck with vehicle_id {booking.vehicle_id} does not exist.")

            elif booking.vehicle_id.startswith('TRC'):
                try:
                    tractor_info = Tractor.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = tractor_info.vehicle_name
                    booking.rent_cost = tractor_info.rent_cost
                    booking.location = tractor_info.location
                    booking.station = tractor_info.station
                    booking.driver_cost = tractor_info.driver_cost
                except Tractor.DoesNotExist:
                    messages.error(request, f"Tractor with vehicle_id {booking.vehicle_id} does not exist.")
            elif booking.vehicle_id.startswith('JCB'):
                try:
                    jcb_info = Jcb.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = jcb_info.vehicle_name
                    booking.rent_cost = jcb_info.rent_cost
                    booking.location = jcb_info.location
                    booking.station = jcb_info.station
                    booking.driver_cost = jcb_info.driver_cost
                except Jcb.DoesNotExist:
                    messages.error(request, f"JCB with vehicle_id {booking.vehicle_id} does not exist.")
            elif booking.vehicle_id.startswith('BT'):
                try:
                    borewell_truck_info = BorewellTruck.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = borewell_truck_info.vehicle_name
                    booking.rent_cost = borewell_truck_info.rent_cost
                    booking.location = borewell_truck_info.location
                    booking.station = borewell_truck_info.station
                    booking.driver_cost = borewell_truck_info.driver_cost
                except BorewellTruck.DoesNotExist:
                    messages.error(request, f"Borewell Truck with vehicle_id {booking.vehicle_id} does not exist.")
            elif booking.vehicle_id.startswith('CH'):
                try:
                    combine_harvester_info = CombineHarvester.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = combine_harvester_info.vehicle_name
                    booking.rent_cost = combine_harvester_info.rent_cost
                    booking.location = combine_harvester_info.location
                    booking.station = combine_harvester_info.station
                    booking.driver_cost = combine_harvester_info.driver_cost
                except CombineHarvester.DoesNotExist:
                    messages.error(request, f"Combine Harvester with vehicle_id {booking.vehicle_id} does not exist.")

            elif booking.vehicle_id.startswith('BK'):
                try:
                    bike_info = Bike.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = bike_info.vehicle_name
                    booking.rent_cost = bike_info.rent_cost
                    booking.location = bike_info.location
                    booking.station = bike_info.station
                    booking.driver_cost = bike_info.driver_cost
                except Bike.DoesNotExist:
                    messages.error(request, f"Bike with vehicle_id {booking.vehicle_id} does not exist.")
            elif booking.vehicle_id.startswith('CR'):
                try:
                    car_info = Car.objects.get(vehicle_id=booking.vehicle_id)
                    booking.vehicle_name = car_info.vehicle_name
                    booking.rent_cost = car_info.rent_cost
                    booking.location = car_info.location
                    booking.station = car_info.station
                    booking.driver_cost = car_info.driver_cost
                except Car.DoesNotExist:
                    messages.error(request, f"Car with vehicle_id {booking.vehicle_id} does not exist.")
            else:
                # Skip displaying an error message for unrecognized vehicle_id format
                continue

        return render(request, 'user_bookings.html', {'user_bookings': user_bookings})
    else:
        return HttpResponse("You need to log in to view your bookings.")


    
    
# @login_required
# def ride_completed(request, booking_id):
#     if request.method == 'POST':
#         booking = get_object_or_404(PaymentDetails, pk=booking_id)
#         try:
#             auto_info = Auto.objects.get(vehicle_id=booking.vehicle_id)
#             vehicle_model = Auto
#         except Auto.DoesNotExist:
#             try:
#                 traveller_info = Traveller.objects.get(vehicle_id=booking.vehicle_id)
#                 vehicle_model = Traveller
#             except Traveller.DoesNotExist:
#                 try:
#                     truck_info = Truck.objects.get(vehicle_id=booking.vehicle_id)
#                     vehicle_model = Truck
#                 except Truck.DoesNotExist:
#                     try:
#                         tractor_info = Tractor.objects.get(vehicle_id=booking.vehicle_id)
#                         vehicle_model = Tractor
#                     except Tractor.DoesNotExist:
#                         try:
#                             jcb_info = Jcb.objects.get(vehicle_id=booking.vehicle_id)
#                             vehicle_model = Jcb
#                         except Jcb.DoesNotExist:
#                             try:
#                                 borewell_truck_info = BorewellTruck.objects.get(vehicle_id=booking.vehicle_id)
#                                 vehicle_model = BorewellTruck
#                             except BorewellTruck.DoesNotExist:
#                                 try:
#                                     combine_harvester_info = CombineHarvester.objects.get(vehicle_id=booking.vehicle_id)
#                                     vehicle_model = CombineHarvester
#                                 except CombineHarvester.DoesNotExist:

#                                     messages.error(request, f"Invalid vehicle_id format for booking with id {booking.id}")
#                                     return redirect('user_bookings')

#         if booking.ride_completed:
#             messages.error(request, 'This ride has already been completed.')
#         else:
#             entered_password = request.POST.get('password')
#             if request.user.check_password(entered_password):
#                 booking.ride_completed = True
#                 booking.save()

#                 active_bookings = PaymentDetails.objects.filter(
#                     vehicle_id=booking.vehicle_id,
#                     ride_completed=False
#                 ).exclude(id=booking_id)

#                 if not active_bookings.exists():
#                     if vehicle_model == Auto:
#                         auto_info.update_status("Available")
#                     elif vehicle_model == Traveller:
#                         traveller_info.update_status("Available")
#                     elif vehicle_model == Truck:
#                         truck_info.update_status("Available")
#                     elif vehicle_model == Tractor:
#                         tractor_info.update_status("Available")
#                     elif vehicle_model == Jcb:
#                         jcb_info.update_status("Available")
#                     elif vehicle_model == BorewellTruck:
#                         borewell_truck_info.update_status("Available")
#                     elif vehicle_model == CombineHarvester:
#                         combine_harvester_info.update_status("Available")
#                 else:
#                     if vehicle_model == Auto:
#                         auto_info.update_status("In Work, Check Schedule and continue")
#                     elif vehicle_model == Traveller:
#                         traveller_info.update_status("In Work, Check Schedule and continue")
#                     elif vehicle_model == Truck:
#                         truck_info.update_status("In Work, Check Schedule and continue")
#                     elif vehicle_model == Tractor:
#                         tractor_info.update_status("In Work, Check Schedule and continue")
#                     elif vehicle_model == Jcb:
#                         jcb_info.update_status("In Work, Check Schedule and continue")
#                     elif vehicle_model == BorewellTruck:
#                         borewell_truck_info.update_status("In Work, Check Schedule and continue")
#                     elif vehicle_model == CombineHarvester:
#                         combine_harvester_info.update_status("In Work, Check Schedule and continue")

#                 messages.success(request, 'Ride completed, Thank you.')
#             else:
#                 messages.error(request, 'Incorrect password. Ride not completed.')

#         return redirect('user_bookings')

#     else:
#         messages.error(request, 'Invalid request method.')
#         return redirect('user_bookings')


@login_required
def ride_completed(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(PaymentDetails, pk=booking_id)
        try:
            auto_info = Auto.objects.get(vehicle_id=booking.vehicle_id)
            vehicle_model = Auto
        except Auto.DoesNotExist:
            try:
                traveller_info = Traveller.objects.get(vehicle_id=booking.vehicle_id)
                vehicle_model = Traveller
            except Traveller.DoesNotExist:
                try:
                    truck_info = Truck.objects.get(vehicle_id=booking.vehicle_id)
                    vehicle_model = Truck
                except Truck.DoesNotExist:
                    try:
                        tractor_info = Tractor.objects.get(vehicle_id=booking.vehicle_id)
                        vehicle_model = Tractor
                    except Tractor.DoesNotExist:
                        try:
                            jcb_info = Jcb.objects.get(vehicle_id=booking.vehicle_id)
                            vehicle_model = Jcb
                        except Jcb.DoesNotExist:
                            try:
                                borewell_truck_info = BorewellTruck.objects.get(vehicle_id=booking.vehicle_id)
                                vehicle_model = BorewellTruck
                            except BorewellTruck.DoesNotExist:
                                try:
                                    combine_harvester_info = CombineHarvester.objects.get(vehicle_id=booking.vehicle_id)
                                    vehicle_model = CombineHarvester
                                except CombineHarvester.DoesNotExist:
                                    try:
                                        bike_info = Bike.objects.get(vehicle_id=booking.vehicle_id)
                                        vehicle_model = Bike
                                    except Bike.DoesNotExist:
                                        try:
                                            car_info = Car.objects.get(vehicle_id=booking.vehicle_id)
                                            vehicle_model = Car
                                        except Car.DoesNotExist:
                                            messages.error(request, f"Invalid vehicle_id format for booking with id {booking.id}")
                                            return redirect('user_bookings')

        if booking.ride_completed:
            messages.error(request, 'This ride has already been completed.')
        else:
            entered_password = request.POST.get('password')
            if request.user.check_password(entered_password):
                booking.ride_completed = True
                booking.save()

                active_bookings = PaymentDetails.objects.filter(
                    vehicle_id=booking.vehicle_id,
                    ride_completed=False
                ).exclude(id=booking_id)

                if not active_bookings.exists():
                    if vehicle_model == Auto:
                        auto_info.update_status("Available")
                    elif vehicle_model == Traveller:
                        traveller_info.update_status("Available")
                    elif vehicle_model == Truck:
                        truck_info.update_status("Available")
                    elif vehicle_model == Tractor:
                        tractor_info.update_status("Available")
                    elif vehicle_model == Jcb:
                        jcb_info.update_status("Available")
                    elif vehicle_model == BorewellTruck:
                        borewell_truck_info.update_status("Available")
                    elif vehicle_model == CombineHarvester:
                        combine_harvester_info.update_status("Available")
                    elif vehicle_model == Bike:
                        bike_info.update_status("Available")
                    elif vehicle_model == Car:
                        car_info.update_status("Available")
                else:
                    if vehicle_model == Auto:
                        auto_info.update_status("In Work, Check Schedule and continue")
                    elif vehicle_model == Traveller:
                        traveller_info.update_status("In Work, Check Schedule and continue")
                    elif vehicle_model == Truck:
                        truck_info.update_status("In Work, Check Schedule and continue")
                    elif vehicle_model == Tractor:
                        tractor_info.update_status("In Work, Check Schedule and continue")
                    elif vehicle_model == Jcb:
                        jcb_info.update_status("In Work, Check Schedule and continue")
                    elif vehicle_model == BorewellTruck:
                        borewell_truck_info.update_status("In Work, Check Schedule and continue")
                    elif vehicle_model == CombineHarvester:
                        combine_harvester_info.update_status("In Work, Check Schedule and continue")
                    elif vehicle_model == Bike:
                        bike_info.update_status("In Work, Check Schedule and continue")
                    elif vehicle_model == Car:
                        car_info.update_status("In Work, Check Schedule and continue")

                messages.success(request, 'Ride completed, Thank you.')
            else:
                messages.error(request, 'Incorrect password. Ride not completed.')

        return redirect('user_bookings')

    else:
        messages.error(request, 'Invalid request method.')
        return redirect('user_bookings')




    


def user_feed_back(request, payment_id):
    payment = get_object_or_404(PaymentDetails, pk=payment_id)
    existing_feedback = Feedback.objects.filter(user=request.user, payment=payment)

    if request.method == 'POST':
        if existing_feedback.exists():
            messages.error(request, 'You have already given feedback for this vehicle.')
            return redirect('user_bookings')
        ease_of_booking = request.POST.get('ease_of_booking')
        vehicle_condition = request.POST.get('vehicle_condition')
        driver_team_service = request.POST.get('driver_team_service')
        experience = request.POST.get('experience')
        additional_comments = request.POST.get('additional_comments')

        try:
            Feedback.objects.create(
                user=request.user,
                payment=payment,
                ease_of_booking=ease_of_booking,
                vehicle_condition=vehicle_condition,
                driver_team_service=driver_team_service,
                experience=experience,
                additional_comments=additional_comments
            )
            messages.success(request, 'Thank you for giving feedback!')
            return redirect('user_bookings')
        except Exception as e:
            messages.error(request, 'Failed to save feedback. Please try again.')
            # Log the exception or handle it as needed

    return render(request, 'user_feed_back.html', {'payment': payment})



@login_required
def user_cancel_form(request, payment_id):
    payment = get_object_or_404(PaymentDetails, pk=payment_id)
    return render(request, 'user_cancel.html', {'payment': payment})


# @login_required
# def user_cancel(request, payment_id):
#     payment = get_object_or_404(PaymentDetails, pk=payment_id)
    
#     # Check if the payment has already been canceled
#     existing_cancellation = CancellationReason.objects.filter(user=request.user, payment=payment).exists()
#     if existing_cancellation:
#         messages.error(request, 'This booking has already been canceled.')
#         return redirect('user_bookings')  # Redirect to the rides page or any other appropriate page
    
#     if request.method == 'POST':
#         entered_password = request.POST.get('password')
        
#         if request.user.check_password(entered_password):
#             # Check if the ride is already marked as completed
#             if payment.ride_completed:
#                 messages.error(request, 'This ride has already been completed.')
#                 return redirect('user_bookings')

#             vehicle_model = None
            
#             try:
#                 auto_info = Auto.objects.get(vehicle_id=payment.vehicle_id)
#                 vehicle_model = auto_info
#             except Auto.DoesNotExist:
#                 try:
#                     traveller_info = Traveller.objects.get(vehicle_id=payment.vehicle_id)
#                     vehicle_model = traveller_info
#                 except Traveller.DoesNotExist:
#                     try:
#                         truck_info = Truck.objects.get(vehicle_id=payment.vehicle_id)
#                         vehicle_model = truck_info
#                     except Truck.DoesNotExist:
#                         try:
#                             tractor_info = Tractor.objects.get(vehicle_id=payment.vehicle_id)
#                             vehicle_model = tractor_info
#                         except Tractor.DoesNotExist:
#                             try:
#                                 jcb_info = Jcb.objects.get(vehicle_id=payment.vehicle_id)
#                                 vehicle_model = jcb_info
#                             except Jcb.DoesNotExist:
#                                 try:
#                                     borewell_truck_info = BorewellTruck.objects.get(vehicle_id=payment.vehicle_id)
#                                     vehicle_model = borewell_truck_info
#                                 except BorewellTruck.DoesNotExist:
#                                     try:
#                                         combine_harvester_info = CombineHarvester.objects.get(vehicle_id=payment.vehicle_id)
#                                         vehicle_model = combine_harvester_info
#                                     except CombineHarvester.DoesNotExist:
#                                         messages.error(request, f"Invalid vehicle_id format for booking with id {payment.id}")
#                                         return redirect('user_bookings')

#             # Password matches, save the cancellation reason
#             original_total_cost = payment.total_cost
#             reason = request.POST.get('reason')
#             CancellationReason.objects.create(reason=reason, user=request.user, payment=payment)

#             # Calculate the new total cost (reduced by 60%)
#             new_total_cost = original_total_cost * Decimal('0.4')  # Assuming 60% reduction
            
#             # Update the total cost in the database
#             payment.total_cost = new_total_cost
#             payment.save()
#             payment.is_canceled = True  # Assuming "is_canceled" is a field in your PaymentDetails model
#             payment.save()

#             # Calculate the remaining 60% cost
#             remaining_cost = original_total_cost - new_total_cost
#             CanceledBooking.objects.create(
#                 payment=payment,
#                 original_total_cost=original_total_cost,
#                 remaining_cost=remaining_cost
#             )
#             messages.success(request, f'Reservation canceled successfully. 60% of the total cost ({remaining_cost}) is retained, please check in your refunds.')

#             if not payment.ride_completed:
#                 # If not completed, mark it as completed and update vehicle status
#                 payment.ride_completed = True
#                 payment.save()

#                 # Check if there are any active bookings for the vehicle except the current one
#                 active_bookings = PaymentDetails.objects.filter(
#                     vehicle_id=payment.vehicle_id,
#                     ride_completed=False
#                 ).exclude(id=payment_id)

#                 if not active_bookings.exists():
#                     # If no active bookings, update the vehicle status to "Available"
#                     vehicle_model.update_status("Available")
#                 else:
#                     # If there are still active bookings, keep the status as "In Work"
#                     vehicle_model.update_status("In Work, Check Schedule and continue")
#             return redirect('user_bookings')  # Redirect to the rides page or any other appropriate page
#         else:
#             messages.error(request, 'Incorrect password. Please try again.')
    
#     return render(request, 'user_cancel.html', {'payment': payment})


@login_required
def user_cancel(request, payment_id):
    payment = get_object_or_404(PaymentDetails, pk=payment_id)

    # Check if the payment has already been canceled
    existing_cancellation = CancellationReason.objects.filter(user=request.user, payment=payment).exists()
    if existing_cancellation:
        messages.error(request, 'This booking has already been canceled.')
        return redirect('user_bookings')  # Redirect to the rides page or any other appropriate page

    if request.method == 'POST':
        entered_password = request.POST.get('password')

        if request.user.check_password(entered_password):
            # Check if the ride is already marked as completed
            if payment.ride_completed:
                messages.error(request, 'This ride has already been completed.')
                return redirect('user_bookings')

            vehicle_model = None

            try:
                auto_info = Auto.objects.get(vehicle_id=payment.vehicle_id)
                vehicle_model = auto_info
            except Auto.DoesNotExist:
                try:
                    traveller_info = Traveller.objects.get(vehicle_id=payment.vehicle_id)
                    vehicle_model = traveller_info
                except Traveller.DoesNotExist:
                    try:
                        truck_info = Truck.objects.get(vehicle_id=payment.vehicle_id)
                        vehicle_model = truck_info
                    except Truck.DoesNotExist:
                        try:
                            tractor_info = Tractor.objects.get(vehicle_id=payment.vehicle_id)
                            vehicle_model = tractor_info
                        except Tractor.DoesNotExist:
                            try:
                                jcb_info = Jcb.objects.get(vehicle_id=payment.vehicle_id)
                                vehicle_model = jcb_info
                            except Jcb.DoesNotExist:
                                try:
                                    borewell_truck_info = BorewellTruck.objects.get(vehicle_id=payment.vehicle_id)
                                    vehicle_model = borewell_truck_info
                                except BorewellTruck.DoesNotExist:
                                    try:
                                        combine_harvester_info = CombineHarvester.objects.get(vehicle_id=payment.vehicle_id)
                                        vehicle_model = combine_harvester_info
                                    except CombineHarvester.DoesNotExist:
                                        try:
                                            bike_info = Bike.objects.get(vehicle_id=payment.vehicle_id)
                                            vehicle_model = bike_info
                                        except Bike.DoesNotExist:
                                            try:
                                                car_info = Car.objects.get(vehicle_id=payment.vehicle_id)
                                                vehicle_model = car_info
                                            except Car.DoesNotExist:
                                                messages.error(request, f"Invalid vehicle_id format for booking with id {payment.id}")
                                                return redirect('user_bookings')

            # Password matches, save the cancellation reason
            original_total_cost = payment.total_cost
            reason = request.POST.get('reason')
            CancellationReason.objects.create(reason=reason, user=request.user, payment=payment)

            # Calculate the new total cost (reduced by 60%)
            new_total_cost = original_total_cost * Decimal('0.4')  # Assuming 60% reduction

            # Update the total cost in the database
            payment.total_cost = new_total_cost
            payment.save()
            payment.is_canceled = True  # Assuming "is_canceled" is a field in your PaymentDetails model
            payment.save()

            # Calculate the remaining 60% cost
            remaining_cost = original_total_cost - new_total_cost
            CanceledBooking.objects.create(
                payment=payment,
                original_total_cost=original_total_cost,
                remaining_cost=remaining_cost
            )
            messages.success(request, f'Reservation canceled successfully. 60% of the total cost ({remaining_cost}) is retained, please check in your refunds.')

            if not payment.ride_completed:
                # If not completed, mark it as completed and update vehicle status
                payment.ride_completed = True
                payment.save()

                # Check if there are any active bookings for the vehicle except the current one
                active_bookings = PaymentDetails.objects.filter(
                    vehicle_id=payment.vehicle_id,
                    ride_completed=False
                ).exclude(id=payment_id)

                if not active_bookings.exists():
                    # If no active bookings, update the vehicle status to "Available"
                    vehicle_model.update_status("Available")
                else:
                    # If there are still active bookings, keep the status as "In Work"
                    vehicle_model.update_status("In Work, Check Schedule and continue")
            return redirect('user_bookings')  # Redirect to the rides page or any other appropriate page
        else:
            messages.error(request, 'Incorrect password. Please try again.')

    return render(request, 'user_cancel.html', {'payment': payment})





@login_required
def user_refund(request):
    canceled_bookings = CanceledBooking.objects.filter(payment__user=request.user)

    return render(request, 'user_refund.html', {'canceled_bookings': canceled_bookings})


























def admin_cancel(request, payment_id):
    payment_details = get_object_or_404(PaymentDetails, id=payment_id)
    cancellation_reasons = CancellationReason.objects.filter(payment=payment_details)
    
    return render(request, 'admin_cancel.html', {'cancellation_reasons': cancellation_reasons})

def admin_feed_back(request, payment_id):
    
    payment_details = get_object_or_404(PaymentDetails, id=payment_id)

    feedback_list = Feedback.objects.filter(payment=payment_details)

    return render(request, 'admin_feed_back.html', {'feedback_list': feedback_list})

def staff_cancel(request, payment_id):
    payment_details = get_object_or_404(PaymentDetails, id=payment_id)
    cancellation_reasons = CancellationReason.objects.filter(payment=payment_details)
    
    return render(request, 'staff_cancel.html', {'cancellation_reasons': cancellation_reasons})
    
def staff_feed_back(request, payment_id):
    
    payment_details = get_object_or_404(PaymentDetails, id=payment_id)

    feedback_list = Feedback.objects.filter(payment=payment_details)

    return render(request, 'staff_feed_back.html', {'feedback_list': feedback_list})



    
    
# def admin_add_borewelltruck(request):
#     return render(request, 'admin_add_borewelltruck.html')

# def admin_add_truck(request):
#     return render(request, 'admin_add_truck.html')

# def admin_add_traveller(request):
#     return render(request, 'admin_add_traveller.html')

# def admin_add_combineharvester(request):
#     return render(request, 'admin_add_combineharvester.html')

# def admin_add_tractor(request):
#     return render(request, 'admin_add_tractor.html')

# def admin_add_jcb(request):
#     return render(request, 'admin_add_jcb.html')

def admin_add_others(request):
    return render(request, 'admin_add_others.html')





# def admin_bike_list(request):
#     return render(request, 'admin_bike_list.html')

# def admin_car_list(request):
    # return render(request, 'admin_car_list.html')



def admin_auto_khm_a_list(request):
    autos_khm_a = Auto.objects.filter(location='Khammam', station='A Station')

    return render(request, 'admin_auto_khm_a_list.html', {'autos_khm_a': autos_khm_a})

def admin_auto_khm_b_list(request):
    autos_khm_b = Auto.objects.filter(location='Khammam', station='B Station')

    return render(request, 'admin_auto_khm_b_list.html', {'autos_khm_b': autos_khm_b})


def admin_borewelltruck_list(request):
    return render(request, 'admin_borewelltruck_list.html')

def admin_truck_list(request):
    return render(request, 'admin_truck_list.html')

def admin_traveller_list(request):
    return render(request, 'admin_traveller_list.html')

def admin_combineharvester_list(request):
    return render(request, 'admin_combineharvester_list.html')

def admin_tractor_list(request):
    return render(request, 'admin_tractor_list.html')

def admin_jcb_list(request):
    return render(request, 'admin_jcb_list.html')

def admin_others_list(request):
    return render(request, 'admin_others_list.html')



def dashboard_view(request):
    return render(request, 'dashboard.html')

def account_view(request):
    return render(request, 'account.html')

def viz_station_list(request):
    return render(request, 'viz_station_list.html')

def khm_station_list(request):
    return render(request, 'khm_station_list.html')

def viz_a_vehicle_list(request):
    return render(request, 'viz_a_vehicle_list.html')

def viz_b_vehicle_list(request):
    return render(request, 'viz_b_vehicle_list.html')

def khm_a_vehicle_list(request):
    return render(request, 'khm_a_vehicle_list.html')

def khm_b_vehicle_list(request):
    return render(request, 'khm_b_vehicle_list.html')




    


#Auto A
    
#admin auto viz a list


def admin_traveller_khm_a_list(request):
    travellers_khm_a = Traveller.objects.filter(location='Khammam', station='A Station')

    return render(request, 'admin_traveller_khm_a_list.html', {'travellers_khm_a': travellers_khm_a})

def admin_traveller_khm_b_list(request):
    travellers_khm_b = Traveller.objects.filter(location='Khammam', station='B Station')

    return render(request, 'admin_traveller_khm_b_list.html', {'travellers_khm_b': travellers_khm_b})


#auto viz a list










