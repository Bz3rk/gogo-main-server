from django.db import transaction
from .utils import send_sms
from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import BookingSummary, Junction, Ride, PriceTable, Car
from .serializers import BookingSummarySerializer, RideSerializer, PriceTableSerializer, JunctionSerializer, UserSerializer, UserRideSerializer, CarSerializer
#from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from drf_spectacular.utils import extend_schema

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .permissions import IsAdminOrReadOnly
from geopy.distance import geodesic

# from django.conf import settings

# CustomUser = settings.AUTH_USER_MODEL


from django.contrib.auth import get_user_model 

User = get_user_model() 


@extend_schema(request = BookingSummarySerializer,  responses = BookingSummarySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createBooking(request):
    def calculate_total_price(base_price, distance, passengers):
        # function calculate total price based on base price, distance, and number of passengers
        return round(base_price * distance * passengers)

    if request.method == 'POST':
        data = request.data
        # checks if the required fields are inputted
        
                
        longitude = data.get('pickup_long')
        latitude = data.get('pickup_lat')
        destination_longitude = data.get('dest_long')
        destination_latitude = data.get('dest_lat')
        passengers = data.get('no_of_passengers')   
        two_way = data.get('two_way')
        user_location = data.get('user_location')
        destination = data.get('destination')

       # checkes if each field is provided
        required_fields = ['user_location','destination','pickup_long', 'pickup_lat', 'dest_long', 'dest_lat', 'no_of_passengers', 'two_way']

        for field in required_fields:
            if field not in data:
                return Response({'message': f'{field.replace("_", " ").capitalize()} is required'}, status=status.HTTP_400_BAD_REQUEST)

        if longitude is not None and latitude is not None and passengers is not None and destination_latitude is not None and destination_latitude is not None:
            try:
                pickup_location = (float(latitude), float(longitude))
                destination = (float(destination_latitude), float(destination_longitude))
            except ValueError:
                return Response({'message': 'Invalid longitude or latitude format'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                cal_distance = geodesic(pickup_location, destination).kilometers
                distance = round(cal_distance, 2)
            except Exception as e:
                return Response({'message': f'Error calculating distance: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

            base_price = 500  # Setting a default base price of 500


            if two_way is True:
                price = (calculate_total_price(base_price, distance, passengers) * 2)
            else:
                price = calculate_total_price(base_price, distance, passengers)
                
            print(price)
            print(distance)

            user = request.user 
            serializer = BookingSummarySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    distance=distance,
                    price=price,
                    user = user
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'user_location, destination, two_way, no_of_passengers, pickup_long, pickup_lat, dest_long, dest_lat are required'}, status=status.HTTP_400_BAD_REQUEST)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    return Response({'message': 'Method not allowed. Use POST to create a booking.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



@extend_schema(request = BookingSummarySerializer, responses = BookingSummarySerializer)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def bookingReceipt(request, user_id):
    if request.method == 'GET':
        try:
            user = request.user 

            if str(user.id) != user_id:
                return Response({'message': 'Unauthorized access'}, status=status.HTTP_401_UNAUTHORIZED)
            data = user.bookingsummary_set.filter(user_id=user_id).order_by('-id')
            serializer = BookingSummarySerializer(data=data, many=True)
            if serializer.is_valid():
                data = serializer.data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BookingSummary.DoesNotExist:
            return Response({'message': 'Booking Receipt not found'}, status=status.HTTP_404_NOT_FOUND)



# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def BookingReceipt(request, user_id):
#     if request.method == 'GET':
#         try:
#             user = request.user 
#             data = user.BookingSummary_set.filter(user_id=user_id)
#         except BookingSummary.DoesNotExist:
#             return Response({'message': 'Booking Receipt not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = BookingSummarySerializer(data, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)



@authentication_classes([TokenAuthentication, BasicAuthentication])
@extend_schema(request = RideSerializer, responses = RideSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookRide(request):
    if request.user.is_authenticated:
        start_junction_name = request.data.get('start_junction')
        end_junction_name = request.data.get('end_junction')
        two_way = request.data.get('two_way', False)
        no_of_passengers = int(request.data.get('no_of_passengers', 1))

        User = get_user_model()
        user = request.user

        try:
            start_junction = Junction.objects.get(name=start_junction_name)
            end_junction = Junction.objects.get(name=end_junction_name)
        except Junction.DoesNotExist:
            return Response({'error': 'Invalid junction names'}, status=status.HTTP_400_BAD_REQUEST)
    
        # Fetching the price from the PriceTable function and multiplies the no of passengers availiable 
        price = get_price_from_table(start_junction, end_junction)
        

        if price is not None:   
            #  checks if the ride is two way or not
            pass_price = price * no_of_passengers
            if two_way is True:
                final_price = pass_price * 2
            else:
                final_price = pass_price

            avaliable_driver = Car.objects.filter(is_active=True)
            # print (avaliable_driver)
            
            if not avaliable_driver:
                return Response({'message': 'No availiable rides'}, status=status.HTTP_404_NOT_FOUND)
            
            selected_driver = avaliable_driver.first()
            # print(selected_driver)

            driver = selected_driver.driver 
            # driver = User.objects.get(car=selected_driver)
            driver_no = driver.phone_no
            print (driver)
            # print(driver_no)
            driver_serializer = UserSerializer(driver)


            twilio_message = f"Ride booked! Pickup: {start_junction_name}, Dropoff: {end_junction_name}"
            twilio_phone_number = driver_no  # Use the driver's phone number

            if send_sms(twilio_phone_number, twilio_message):
                print("Twilio SMS notification sent successfully")
            else:
                return Response({"Error":"Driver notification not successful"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            selected_driver.is_active = False
            selected_driver.save()


            response_data = {
        'message': 'Booking successful',
        'driver_details': driver_serializer.data,
        'car_name': selected_driver.car_model
        }


            ride = Ride(user=user, start_junction=start_junction, end_junction=end_junction,  no_of_passengers=no_of_passengers, two_way=two_way, price=final_price,)
            ride.save()

            serializer = RideSerializer(ride)
            return Response({"Ride-info":serializer.data, "Driver-info":response_data}, status=status.HTTP_201_CREATED)
        else:
            final_price = price
            return Response({'error': 'Price information not available'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

#function to determine the price from the price table
def get_price_from_table(start_junction, end_junction):

    try:
        # Try to get the price for the normal order
        price = PriceTable.objects.get(start_junction=start_junction, end_junction=end_junction).price
    except PriceTable.DoesNotExist:
        try:
            # Try to get the price for the reverse order
            price = PriceTable.objects.get(start_junction=end_junction, end_junction=start_junction).price
        except PriceTable.DoesNotExist:
            # Set the price to None if both normal and reverse orders are not found
            price = None

    return price



@extend_schema(request = RideSerializer, responses = RideSerializer)
@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def rideSummary(request, ride_id):
    user = request.user

    try:
        ride = Ride.objects.get(pk=ride_id, user=user)
        serializer = RideSerializer(ride)
        return Response(serializer.data)
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found for this user'}, status=400)



@extend_schema(request = JunctionSerializer, responses = JunctionSerializer)
@api_view(['GET'])
def junctionList(request):
    junctions = Junction.objects.all()
    serializer = JunctionSerializer(junctions, many=True)
    return Response(serializer.data)


@extend_schema(request = PriceTableSerializer, responses = PriceTableSerializer)
@api_view(['GET'])
def priceTableList(request):
    prices = PriceTable.objects.all()
    serializer = PriceTableSerializer(prices, many=True)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userRideList(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            rides = Ride.objects.filter(user=user)
            rideserializer = UserRideSerializer(rides, many=True)
            userSerializer = UserSerializer(user)
            return Response({'user': userSerializer.data, 'history' : rideserializer.data})
        except Ride.DoesNotExist:
            return Response({'error': 'No ride found for this user'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(request = CarSerializer, responses = CarSerializer)
@api_view(['POST'])
@permission_classes([IsAdminOrReadOnly, IsAuthenticated])
def driverCars(request):
    car_model = request.data.get('car_model')
    license_plate = request.data.get('license_plate')
    phone = request.data.get('phone')
    print(phone)
    print (request.data)

    try:
        # phone_no = User.objects.filter(phone_no=driver_no).first()
        driver = User.objects.get(phone_no=phone)
    except User.DoesNotExist:
            return Response({'error': 'Driver with this phone no does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if driver.is_driver:
        car_detail = Car(car_model=car_model, license_plate=license_plate, driver=driver)
        car_detail.save()

        serializer = CarSerializer(car_detail)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'Error': 'User is not a driver'}, status=status.HTTP_400_BAD_REQUEST)