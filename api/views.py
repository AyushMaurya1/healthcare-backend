from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import UserRegisterSerializer, PatientSerializer, DoctorSerializer, PatientDoctorMappingSerializer
from .permissions import IsOwner
from django.shortcuts import get_object_or_404

# Authentication View
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': serializer.data,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Patient ViewSet
class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_object(self):
        obj = get_object_or_404(Patient, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'message': 'Patient deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Doctor ViewSet
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'message': 'Doctor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Patient-Doctor Mapping ViewSet
class MappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id') or self.request.query_params.get('patient_id')
        if patient_id:
            return PatientDoctorMapping.objects.filter(patient_id=patient_id)
        return PatientDoctorMapping.objects.all()

    def perform_create(self, serializer):
        patient = serializer.validated_data['patient']
        if patient.created_by != self.request.user:
            raise ValidationError("You can only assign doctors to your own patients.")
        serializer.save()

    def get_object(self):
        obj = get_object_or_404(PatientDoctorMapping, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Mapping deleted successfully'}, status=status.HTTP_204_NO_CONTENT)