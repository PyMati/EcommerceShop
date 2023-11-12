from django.shortcuts import render
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .models import Product
from .serializers import ProductSerializer


# Endpoints section connected to authentication
class Auth(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request):
        pass


# Endpoints section connected to workflow with products
class GetSpecificProduct(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("product_id")
        product = self.queryset.filter(id=product_id).first()

        if product:
            serializer = self.serializer_class(product)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)

        return Response(
            {"message": "Product with this id doesn't exist in database."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductOperations(APIView):
    queryset = Product.objects.all()
    serializer = ProductSerializer

    def get(self, request, *args, **kwargs):
        params = request.query_params
        params_filter = params.get("filter_by")
        params_filter_value = params.get("filter_value")
        params_sort = params.get("sort_by")

        if params_filter:
            if params_filter_value:
                if params_filter == "name":
                    self.queryset = self.queryset.filter(name=params_filter_value)
                elif params_filter == "category":
                    filter_kwargs = {f"{params_filter}__category": params_filter_value}
                    self.queryset = self.queryset.filter(**filter_kwargs)
                elif params_filter == "description":
                    self.queryset = self.queryset.filter(
                        description=params_filter_value
                    )
                elif params_filter == "price":
                    self.queryset = self.queryset.filter(price=params_filter_value)
            else:
                return Response(
                    {
                        "message": "In order to use filtration you have to provide filter_value."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        if params_sort:
            if params_sort == "name":
                self.queryset = self.queryset.order_by("name")
            elif params_sort == "category":
                self.queryset = self.queryset.order_by("category__category")
            elif params_sort == "price":
                self.queryset = self.queryset.order_by("price")
        if len(self.queryset.values()) == 0:
            return Response({"message": "Database is empty"})

        return Response(
            {"data": self.serializer(self.queryset.all(), many=True).data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"message": "New product was created."}, status=status.HTTP_201_CREATED
            )

        return Response(
            {"message": "An occurred error while creating product."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def put(self, request):
        product_id = request.data.get("id")
        if not product_id:
            return Response(
                {"message": "In order to update product you have to prodive ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.queryset.filter(id=product_id).first()
        if not instance:
            return Response(
                {
                    "message": "Product with this id doesn't exist, so it cannot be updated."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer(data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.update(instance, serializer.validated_data)
            return Response(
                {"message": "Product was updated."}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "An error occured while updating product."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def delete(self, request):
        product_id = request.data.get("id")
        if not product_id:
            return Response(
                {"message": "In order to delete product you have to prodive ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance = self.queryset.filter(id=product_id).first()
        if not instance:
            return Response(
                {
                    "message": "Product with this id doesn't exist, so it cannot be deleted."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()

        return Response({"message": "Product was deleted."}, status=status.HTTP_200_OK)
