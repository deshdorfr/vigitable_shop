from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User, Address
from .serializers import SignInSerializer, UserProfileSerializer, AddressSerializer


# ✅ Manual schema for SignIn (shows fields in swagger)
signin_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=["mobile", "password"],
    properties={
        "mobile": openapi.Schema(type=openapi.TYPE_STRING, example="9999999999"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, example="1234"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, example="Test User"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, example="test@gmail.com"),
    },
)


@api_view(["POST"])
@permission_classes([AllowAny])
@swagger_auto_schema(
    request_body=signin_request_schema,
    responses={200: "Login Success", 400: "Invalid Credentials"},
)
def signin_view(request):
    serializer = SignInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    mobile = serializer.validated_data["mobile"]
    password = serializer.validated_data["password"]
    name = serializer.validated_data.get("name")
    email = serializer.validated_data.get("email")

    user = User.objects.filter(mobile=mobile).first()

    # create account automatically (first login)
    if not user:
        user = User.objects.create_user(
            mobile=mobile,
            password=password,
            name=name or "Customer",
            email=email
        )

    # login
    user_auth = authenticate(request, mobile=mobile, password=password)
    if not user_auth:
        return Response({"success": False, "message": "Invalid password"}, status=400)

    token, _ = Token.objects.get_or_create(user=user_auth)

    return Response({
        "success": True,
        "token": token.key,
        "user": UserProfileSerializer(user_auth).data
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(responses={200: UserProfileSerializer()})
def profile_view(request):
    return Response({"success": True, "user": UserProfileSerializer(request.user).data})


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "email": openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={200: UserProfileSerializer()},
)
def update_profile_view(request):
    user = request.user
    serializer = UserProfileSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"success": True, "user": serializer.data})


# ---------------- ADDRESSES ---------------- #

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(responses={200: AddressSerializer(many=True)})
def list_addresses(request):
    addresses = Address.objects.filter(user=request.user).order_by("-is_default", "-id")
    serializer = AddressSerializer(addresses, many=True)
    return Response({"success": True, "data": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    request_body=AddressSerializer,
    responses={200: AddressSerializer()},
)
def add_address(request):
    serializer = AddressSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if serializer.validated_data.get("is_default"):
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)

    address = serializer.save(user=request.user)
    return Response({"success": True, "data": AddressSerializer(address).data})


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    request_body=AddressSerializer,
    responses={200: AddressSerializer()},
)
def update_address(request, pk):
    address = Address.objects.filter(user=request.user, pk=pk).first()
    if not address:
        return Response({"success": False, "message": "Address not found"}, status=404)

    serializer = AddressSerializer(address, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    if serializer.validated_data.get("is_default"):
        Address.objects.filter(user=request.user, is_default=True).exclude(pk=pk).update(is_default=False)

    serializer.save()
    return Response({"success": True, "data": serializer.data})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(responses={200: "Address deleted"})
def delete_address(request, pk):
    address = Address.objects.filter(user=request.user, pk=pk).first()
    if not address:
        return Response({"success": False, "message": "Address not found"}, status=404)

    address.delete()
    return Response({"success": True, "message": "Address deleted"})
