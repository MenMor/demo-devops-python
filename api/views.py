from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import render
from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if request.accepted_renderer.format == "html":
            return Response(
                {'message': 'Hello, world!'}, status=status.HTTP_200_OK
            )

        return Response(serializer.data)

    def retrieve(self, request, pk):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def create(self, request):
        data = request.data

        if self.get_queryset().filter(dni=data.get("dni", "")).exists():
            return Response({"detail": "User already exists"}, status=400)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=201)


def home(request):
    return render(request, "home.html")
