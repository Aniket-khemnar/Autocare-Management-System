# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth import get_user_model
# from vehicles.models import Vehicle
# from bookings.models import ServiceBooking

# User = get_user_model()

# # ------------ ADMIN APIs ------------

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_all_users(request):
#     users = User.objects.all().values("id", "username", "email", "role")
#     return Response(list(users))


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_all_bookings(request):
#     bookings = ServiceBooking.objects.all().values(
#         "id", "customer__username", "date", "status"
#     )
#     formatted = [
#         {
#             "customer_name": b["customer__username"],
#             "date": b["date"],
#             "status": b["status"]
#         } for b in bookings
#     ]
#     return Response(formatted)

# # ------------ CUSTOMER APIs ------------

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def customer_vehicles(request):
#     user = request.user
#     vehicles = Vehicle.objects.filter(user=user).values("id", "vehicle_number", "model")
#     return Response(list(vehicles))


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def customer_bookings(request):
#     user = request.user
#     bookings = ServiceBooking.objects.filter(customer=user).values("id", "date", "status")
#     return Response(list(bookings))

# # ------------ MECHANIC APIs ------------

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def mechanic_jobs(request):
#     user = request.user
#     jobs = ServiceBooking.objects.filter(assigned_mechanic=user).values(
#         "id", "vehicle__vehicle_number", "date", "status"
#     )
#     formatted = [
#         {
#             "vehicle_number": j["vehicle__vehicle_number"],
#             "date": j["date"],
#             "status": j["status"]
#         } for j in jobs
#     ]
#     return Response(formatted)
