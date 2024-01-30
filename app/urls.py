from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from .views import admin_redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('index/', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('admin/login/', LoginView.as_view(redirect_authenticated_user=True), name='admin_login'),
    path('admin/', admin_redirect, name='admin_redirect'),

    path('admin_account/', views.admin_account, name='admin_account'),
    path('admin_notification/', views.admin_notification, name='admin_notification'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_delete_account/', views.admin_delete_account, name='admin_delete_account'),
    path('admin_change_password/', views.admin_change_password, name='admin_change_password'),
    path('admin_feed_back/<int:payment_id>/', views.admin_feed_back, name='admin_feed_back'),
    path('admin_cancel/<int:payment_id>/', views.admin_cancel, name='admin_cancel'),
    path('admin_users_list/', views.admin_users_list, name='admin_users_list'),
    path('enable_user/<int:user_id>/', views.enable_user, name='enable_user'),
    path('disable_user/<int:user_id>/', views.disable_user, name='disable_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_viz_a_rides_graph /', views.admin_viz_a_rides_graph , name='admin_viz_a_rides_graph '),

    

    path('admin_add_vehicle/', views.admin_add_vehicle, name='admin_add_vehicle'),
    path('admin_bike_viz_a_list/', views.admin_bike_viz_a_list, name='admin_bike_viz_a_list'),
    path('admin_bike_viz_b_list/', views.admin_bike_viz_b_list, name='admin_bike_viz_b_list'),

# For Car
    path('admin_car_viz_a_list/', views.admin_car_viz_a_list, name='admin_car_viz_a_list'),
    path('admin_car_viz_b_list/', views.admin_car_viz_b_list, name='admin_car_viz_b_list'),




    path('admin_auto_viz_a_list/', views.admin_auto_viz_a_list, name='admin_auto_viz_a_list'),
    path('admin_auto_viz_b_list/', views.admin_auto_viz_b_list, name='admin_auto_viz_b_list'),
    path('admin_traveller_viz_a_list/', views.admin_traveller_viz_a_list, name='admin_traveller_viz_a_list'),
    path('admin_traveller_viz_b_list/', views.admin_traveller_viz_b_list, name='admin_traveller_viz_b_list'),
    path('admin_traveller_khm_a_list/', views.admin_traveller_khm_a_list, name='admin_traveller_khm_a_list'),
    path('admin_traveller_khm_b_list/', views.admin_traveller_khm_b_list, name='admin_traveller_khm_b_list'),

    path('admin_truck_viz_a_list/', views.admin_truck_viz_a_list, name='admin_truck_viz_a_list'),
    path('admin_truck_viz_b_list/', views.admin_truck_viz_b_list, name='admin_truck_viz_b_list'),
    path('admin_truck_khm_a_list/', views.admin_truck_khm_a_list, name='admin_truck_khm_a_list'),
    path('admin_truck_khm_b_list/', views.admin_truck_khm_b_list, name='admin_truck_khm_b_list'),

    path('admin_tractor_viz_a_list/', views.admin_tractor_viz_a_list, name='admin_tractor_viz_a_list'),
    path('admin_tractor_viz_b_list/', views.admin_tractor_viz_b_list, name='admin_tractor_viz_b_list'),
    path('admin_tractor_khm_a_list/', views.admin_tractor_khm_a_list, name='admin_tractor_khm_a_list'),
    path('admin_tractor_khm_b_list/', views.admin_tractor_khm_b_list, name='admin_tractor_khm_b_list'),

    path('admin_jcb_viz_a_list/', views.admin_jcb_viz_a_list, name='admin_jcb_viz_a_list'),
    path('admin_jcb_viz_b_list/', views.admin_jcb_viz_b_list, name='admin_jcb_viz_b_list'),
    path('admin_jcb_khm_a_list/', views.admin_jcb_khm_a_list, name='admin_jcb_khm_a_list'),
    path('admin_jcb_khm_b_list/', views.admin_jcb_khm_b_list, name='admin_jcb_khm_b_list'),

    path('admin_borewelltruck_viz_a_list/', views.admin_borewelltruck_viz_a_list, name='admin_borewelltruck_viz_a_list'),
    path('admin_borewelltruck_viz_b_list/', views.admin_borewelltruck_viz_b_list, name='admin_borewelltruck_viz_b_list'),
    path('admin_borewelltruck_khm_a_list/', views.admin_borewelltruck_khm_a_list, name='admin_borewelltruck_khm_a_list'),
    path('admin_borewelltruck_khm_b_list/', views.admin_borewelltruck_khm_b_list, name='admin_borewelltruck_khm_b_list'),

    path('admin_combineharvester_viz_a_list/', views.admin_combineharvester_viz_a_list, name='admin_combineharvester_viz_a_list'),
    path('admin_combineharvester_viz_b_list/', views.admin_combineharvester_viz_b_list, name='admin_combineharvester_viz_b_list'),
    path('admin_combineharvester_khm_a_list/', views.admin_combineharvester_khm_a_list, name='admin_combineharvester_khm_a_list'),
    path('admin_combineharvester_khm_b_list/', views.admin_combineharvester_khm_b_list, name='admin_combineharvester_khm_b_list'),











    path('admin_rides/', views.admin_rides, name='admin_rides'),
    path('admin_viz_a_rides/', views.admin_viz_a_rides, name='admin_viz_a_rides'),
    path('admin_viz_b_rides/', views.admin_viz_b_rides, name='admin_viz_b_rides'),
    path('admin_khm_a_rides/', views.admin_khm_a_rides, name='admin_khm_a_rides'),
    path('admin_khm_b_rides/', views.admin_khm_b_rides, name='admin_khm_b_rides'),

    path('admin_viz_a_rides_graph/', views.admin_viz_a_rides_graph, name='admin_viz_a_rides_graph'),
    # path('admin_viz_a_rides_graph_data/', views.admin_viz_a_rides_graph_data, name='admin_viz_a_rides_graph_data'),



    path('admin_add_bike/', views.admin_add_bike, name='admin_add_bike'),
    path('delete_bike/<int:bike_id>/', views.delete_bike, name='delete_bike'),

    path('admin_add_car/', views.admin_add_car, name='admin_add_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),

    path('admin_add_auto/', views.admin_add_auto, name='admin_add_auto'),
    path('delete_auto/<int:auto_id>/', views.delete_auto, name='delete_auto'),

    path('admin_add_traveller/', views.admin_add_traveller, name='admin_add_traveller'),
    path('delete_traveller/<int:traveller_id>/', views.delete_traveller, name='delete_traveller'),

    path('admin_add_truck/', views.admin_add_truck, name='admin_add_truck'),
    path('delete_truck/<int:truck_id>/', views.delete_truck, name='delete_truck'),

    path('admin_add_tractor/', views.admin_add_tractor, name='admin_add_tractor'),
    path('delete_tractor/<int:tractor_id>/', views.delete_tractor, name='delete_tractor'),

    path('admin_add_jcb/', views.admin_add_jcb, name='admin_add_jcb'),
    path('delete_jcb/<int:jcb_id>/', views.delete_jcb, name='delete_jcb'),

    path('admin_add_borewelltruck/', views.admin_add_borewelltruck, name='admin_add_borewelltruck'),
    path('delete_borewelltruck/<int:borewelltruck_id>/', views.delete_borewelltruck, name='delete_borewelltruck'),

    path('admin_add_combineharvester/', views.admin_add_combineharvester, name='admin_add_combineharvester'),
    path('delete_combineharvester/<int:combineharvester_id>/', views.delete_combineharvester, name='delete_combineharvester'),

    
    

    
     
    path('admin_add_others/', views.admin_add_others, name='admin_add_others'),

    path('other_viz_a_list/', views.other_viz_a_list, name='other_viz_a_list'),
    path('other_viz_b_list/', views.other_viz_b_list, name='other_viz_b_list'),


    # path('admin_bike_list/', views.admin_bike_list, name='admin_bike_list'),
    # path('admin_car_list/', views.admin_car_list, name='admin_car_list'),

    path('admin_auto_khm_a_list/', views.admin_auto_khm_a_list, name='admin_auto_khm_a_list'),
    path('admin_auto_khm_b_list/', views.admin_auto_khm_b_list, name='admin_auto_khm_b_list'),

    path('admin_borewelltruck_list/', views.admin_borewelltruck_list, name='admin_borewelltruck_list'),
    path('admin_truck_list/', views.admin_truck_list, name='admin_truck_list'),
    path('admin_traveller_list/', views.admin_traveller_list, name='admin_traveller_list'),
    path('admin_combineharvester_list/', views.admin_combineharvester_list, name='admin_combineharvester_list'),
    path('admin_tractor_list/', views.admin_tractor_list, name='admin_tractor_list'),
    path('admin_jcb_list/', views.admin_jcb_list, name='admin_jcb_list'),
    path('admin_others_list/', views.admin_others_list, name='admin_others_list'),

    
    path('staff_dashboard/', login_required(views.staff_dashboard), name='staff_dashboard'),
    path('staff_account/', views.staff_account, name='staff_account'),
    path('staff_delete_account/', views.staff_delete_account, name='staff_delete_account'),
    path('staff_change_password/', views.staff_change_password, name='staff_change_password'),
    path('staff_feed_back/<int:payment_id>/', views.staff_feed_back, name='staff_feed_back'),
    path('staff_cancel/<int:payment_id>/', views.staff_cancel, name='staff_cancel'),
    path('staff_rides/', views.staff_rides, name='staff_rides'),
    path('staff_viz_a_rides/', views.staff_viz_a_rides, name='staff_viz_a_rides'),
    path('staff_viz_b_rides/', views.staff_viz_b_rides, name='staff_viz_b_rides'),
    path('staff_khm_a_rides/', views.staff_khm_a_rides, name='staff_khm_a_rides'),
    path('staff_khm_b_rides/', views.staff_khm_b_rides, name='staff_khm_b_rides'),

    

    path('become_partner/', views.become_partner_view, name='become_partner'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('account/', views.account_view, name='account_view'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
    path('user_bookings/', views.user_bookings, name='user_bookings'),
    path('ride_completed/<int:booking_id>/', views.ride_completed, name='ride_completed'),
    path('user_cancel/<int:payment_id>/', views.user_cancel, name='user_cancel'),
    # path('user_cancel_form/<int:payment_id>/', views.user_cancel_form, name='user_cancel_form'),
    path('user_feed_back/<int:payment_id>/', views.user_feed_back, name='user_feed_back'),
    path('user_refund/', views.user_refund, name='user_refund'),

    path('viz_station_list/', views.viz_station_list, name='viz_station_list'),
    path('viz_a_vehicle_list/', views.viz_a_vehicle_list, name='viz_a_vehicle_list'),
    path('viz_b_vehicle_list/', views.viz_b_vehicle_list, name='viz_b_vehicle_list'),
    
    path('get_booked_vehicles_viz_a/', views.get_booked_vehicles_viz_a, name='get_booked_vehicles_viz_a'),
    path('get_booked_vehicles_viz_b/', views.get_booked_vehicles_viz_b, name='get_booked_vehicles_viz_b'),

    path('khm_station_list/', views.khm_station_list, name='khm_station_list'),
    path('khm_a_vehicle_list/', views.khm_a_vehicle_list, name='khm_a_vehicle_list'),
    path('khm_b_vehicle_list/', views.khm_b_vehicle_list, name='khm_b_vehicle_list'),


    # For Bike
    path('bike_viz_a_list/', views.bike_viz_a_list, name='bike_viz_a_list'),
    path('bike_viz_a_payment/<int:bike_id>/', views.bike_viz_a_payment, name='bike_viz_a_payment'),
    path('bike_viz_b_list/', views.bike_viz_b_list, name='bike_viz_b_list'),
    path('bike_viz_b_payment/<int:bike_id>/', views.bike_viz_b_payment, name='bike_viz_b_payment'),

# For Car
    path('car_viz_a_list/', views.car_viz_a_list, name='car_viz_a_list'),
    path('car_viz_a_payment/<int:car_id>/', views.car_viz_a_payment, name='car_viz_a_payment'),
    path('car_viz_b_list/', views.car_viz_b_list, name='car_viz_b_list'),
    path('car_viz_b_payment/<int:car_id>/', views.car_viz_b_payment, name='car_viz_b_payment'),

    
    
    path('auto_viz_a_list/', views.auto_viz_a_list, name='auto_viz_a_list'),
    path('auto_viz_a_payment/<int:auto_id>/', views.auto_viz_a_payment, name='auto_viz_a_payment'),

    path('auto_viz_b_list/', views.auto_viz_b_list, name='auto_viz_b_list'),
    path('auto_viz_b_payment/<int:auto_id>/', views.auto_viz_b_payment, name='auto_viz_b_payment'),


    path('traveller_viz_a_list/', views.traveller_viz_a_list, name='traveller_viz_a_list'),
    path('traveller_viz_a_payment/<int:traveller_id>/', views.traveller_viz_a_payment, name='traveller_viz_a_payment'),

    path('traveller_viz_b_list/', views.traveller_viz_b_list, name='traveller_viz_b_list'),
    path('traveller_viz_b_payment/<int:traveller_id>/', views.traveller_viz_b_payment, name='traveller_viz_b_payment'),

    path('truck_viz_a_list/', views.truck_viz_a_list, name='truck_viz_a_list'),
    path('truck_viz_a_payment/<int:truck_id>/', views.truck_viz_a_payment, name='truck_viz_a_payment'),

    path('truck_viz_b_list/', views.truck_viz_b_list, name='truck_viz_b_list'),
    path('truck_viz_b_payment/<int:truck_id>/', views.truck_viz_b_payment, name='truck_viz_b_payment'),


    path('tractor_viz_a_list/', views.tractor_viz_a_list, name='tractor_viz_a_list'),
    path('tractor_viz_a_payment/<int:tractor_id>/', views.tractor_viz_a_payment, name='tractor_viz_a_payment'),
    path('tractor_viz_b_list/', views.tractor_viz_b_list, name='tractor_viz_b_list'),
    path('tractor_viz_b_payment/<int:tractor_id>/', views.tractor_viz_b_payment, name='tractor_viz_b_payment'),

    path('jcb_viz_a_list/', views.jcb_viz_a_list, name='jcb_viz_a_list'),
    path('jcb_viz_a_payment/<int:jcb_id>/', views.jcb_viz_a_payment, name='jcb_viz_a_payment'),
    path('jcb_viz_b_list/', views.jcb_viz_b_list, name='jcb_viz_b_list'),
    path('jcb_viz_b_payment/<int:jcb_id>/', views.jcb_viz_b_payment, name='jcb_viz_b_payment'),

    path('borewelltruck_viz_a_list/', views.borewelltruck_viz_a_list, name='borewelltruck_viz_a_list'),
    path('borewelltruck_viz_a_payment/<int:borewelltruck_id>/', views.borewelltruck_viz_a_payment, name='borewelltruck_viz_a_payment'),
    path('borewelltruck_viz_b_list/', views.borewelltruck_viz_b_list, name='borewelltruck_viz_b_list'),
    path('borewelltruck_viz_b_payment/<int:borewelltruck_id>/', views.borewelltruck_viz_b_payment, name='borewelltruck_viz_b_payment'),

    path('combineharvester_viz_a_list/', views.combineharvester_viz_a_list, name='combineharvester_viz_a_list'),
    path('combineharvester_viz_a_payment/<int:combineharvester_id>/', views.combineharvester_viz_a_payment, name='combineharvester_viz_a_payment'),
    path('combineharvester_viz_b_list/', views.combineharvester_viz_b_list, name='combineharvester_viz_b_list'),
    path('combineharvester_viz_b_payment/<int:combineharvester_id>/', views.combineharvester_viz_b_payment, name='combineharvester_viz_b_payment'),


    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 