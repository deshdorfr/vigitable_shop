from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LoginSerializer
import uuid

@api_view(["POST"])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    mobile = serializer.validated_data["mobile"]
    password = serializer.validated_data["password"]

    if mobile == "9999999999" and password == "1234":
        token = str(uuid.uuid4())
        return Response({
            "success": True,
            "token": token,
            "user": {"id": 1, "name": "Test User", "mobile": mobile}
        })

    return Response({"success": False, "message": "Invalid mobile or password"}, status=400)
