from rest_framework import permissions


class Client(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer


class Seller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller
