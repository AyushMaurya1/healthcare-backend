from rest_framework.permissions import BasePermission
from .models import Patient, PatientDoctorMapping

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Patient):
            return obj.created_by == request.user
        elif isinstance(obj, PatientDoctorMapping):
            return obj.patient.created_by == request.user
        return True