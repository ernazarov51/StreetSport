from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.models import Stadium, Order, PlatformStadium
from apps.permissions import AdminPermission, OwnerPermission
from apps.serializers import StadiumModelSerializer, StadiumDetailSerializer, OrderModelSerializer, \
    CollectManagerSerializer, PlatFormStadiumSerializer, StadiumUpdateSerializer, StadiumListModelSerializer, \
    CreateOrderModelSerializer


# Create your views here.
@extend_schema(tags=['Owner'])
class StadiumCreateApiView(CreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumModelSerializer
    permission_classes = (IsAuthenticated, OwnerPermission)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


@extend_schema(tags=['Owner'])
class StadiumDetailApiView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, OwnerPermission]
    queryset = Stadium.objects.all()
    lookup_field = 'pk'
    serializer_class = StadiumDetailSerializer

    def get_queryset(self):
        return Stadium.objects.filter(owner_id=self.request.user.id)


@extend_schema(tags=['Owner'])
class SelfStadiumsOrderListApiView(ListAPIView):
    permission_classes = [IsAuthenticated, OwnerPermission]
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer

    def get_queryset(self):
        return Order.objects.filter(stadium__owner_id=self.request.user.id)


@extend_schema(tags=['Owner'], request=CollectManagerSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated, OwnerPermission])
def collect_manager_api_view(request, stadium_id):
    serializer = CollectManagerSerializer(data=request.data)
    if serializer.is_valid():
        manager_id = serializer.validated_data['manager_id']
        try:
            stadium = Stadium.objects.get(id=stadium_id)
        except Stadium.DoesNotExist:
            return Response({'message': 'Stadium does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        stadium.manager_id = manager_id
        stadium.save()
        return Response({'message': 'Manager is successfully collected'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Admin'])
class SavePlatformStadium(CreateAPIView):
    permission_classes = [IsAuthenticated, AdminPermission]
    serializer_class = PlatFormStadiumSerializer


@extend_schema(tags=['Admin'], request=PlatFormStadiumSerializer)
class DeletePlatformStadium(DestroyAPIView):
    queryset = PlatformStadium.objects.all()
    permission_classes = [IsAuthenticated, AdminPermission]
    serializer_class = PlatFormStadiumSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'successfully deleted'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Admin'])
@api_view(['GET'])
@permission_classes([IsAuthenticated, AdminPermission])
def get_stadium_count_api_view(request):
    return Response({'count': PlatformStadium.objects.count()})


@extend_schema(tags=['Admin'])
class StadiumUpdateApiView(UpdateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated | AdminPermission]


@extend_schema(tags=['User'])
class GetAllStadiums(ListAPIView):
    queryset = Stadium.objects.all()
    serializer_class = StadiumListModelSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['User'])
class BookingStadiums(CreateAPIView):
    queryset = Stadium.objects.all()
    serializer_class = CreateOrderModelSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context
