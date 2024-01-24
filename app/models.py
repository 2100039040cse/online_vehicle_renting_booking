# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Partner(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=50)
    num_vehicles = models.IntegerField()
    contacted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    contact_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.fullname  # Customize as per your requirement
    


class Bike(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='bike_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    # driver_name = models.CharField(max_length=100)
    # driver_contact = models.CharField(max_length=20)
    # driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_bikes', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()

class Car(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='car_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=20)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_cars', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()

    

class Auto(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='auto_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=20)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_autos', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()

class Traveller(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='traveller_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=20)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_travellers', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()

class Truck(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='truck_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=20)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_trucks', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()

class Tractor(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='tractor_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=20)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_tractors', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()


class Jcb(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='jcb_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=20)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_jcbs', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()

class BorewellTruck(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='borewelltruck_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=20)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_borewelltrucks', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()


class CombineHarvester(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='combineharvester_images/')
    vehicle_name = models.CharField(max_length=100)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=20)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    station = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Available')
    # terms_conditions = models.TextField() 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='added_combineharvesters', default=1)
    date_added = models.DateTimeField(default=timezone.now)
 
    def __str__(self):
        return self.vehicle_name
    def update_status(self, new_status):
        self.status = new_status
        self.save()


class PaymentDetails(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_number = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100) 
    driver_contact = models.CharField(max_length=20)
    rent_cost = models.DecimalField(max_digits=10, decimal_places=2)
    driver_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=150)
    timestamp = models.DateTimeField(default=timezone.now)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=255)
    ride_completed = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for {self.vehicle_id} by {self.user.username}"
    


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE)
    

    ease_of_booking = models.IntegerField()
    vehicle_condition = models.IntegerField()
    driver_team_service = models.IntegerField()
    experience = models.IntegerField()
    additional_comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CancellationReason(models.Model):
    REASON_CHOICES = [
        ('change_of_plans', 'Change of Plans'),
        ('found_alternative', 'Found Alternative'),
        ('booking_mistake', 'Booking Mistake'),
        ('travel_restrictions', 'Travel Restrictions'),
        ('unforeseen_circumstances', 'Unforeseen Circumstances'),
    ]

    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    payment = models.ForeignKey(PaymentDetails, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
   

class CanceledBooking(models.Model):
    payment = models.OneToOneField(PaymentDetails, on_delete=models.CASCADE)
    original_total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_cost = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_id = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField(default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Canceled booking for {self.payment.vehicle_id} by {self.payment.user.username}"