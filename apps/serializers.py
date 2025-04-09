from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import Stadium, Order, PlatformStadium
from authentication.models import User
from authentication.serializers import RegisterModelSerializer


class StadiumModelSerializer(ModelSerializer):
    class Meta:
        model = Stadium
        fields = 'id', 'name', 'region', 'location_note', 'price'
        extra_kwargs = {'id': {'read_only': True}}

    def save(self, **kwargs):
        owner = self.context["request"].user
        self.validated_data['owner'] = owner
        return Stadium.objects.create(**self.validated_data)


class ManagerModelSerializer(ModelSerializer):
    full_name = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name


class StadiumDetailSerializer(ModelSerializer):
    manager = SerializerMethodField()
    booked_count=SerializerMethodField()

    class Meta:
        model = Stadium
        fields = 'id', 'name', 'region', 'location_note', 'price','booked_count', 'manager'

    def get_manager(self, obj):
        return ManagerModelSerializer(obj.manager).data if obj.manager is not None else None

    def get_booked_count(self, obj):
        booked_count = Order.objects.filter(stadium=obj).count()
        return booked_count


class OrderModelSerializer(ModelSerializer):
    stadium = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'start_time', 'end_time', 'user', 'stadium']

    def get_stadium(self, obj):
        return StadiumDetailSerializer(obj.stadium, context=self.context).data

    def get_user(self, obj):
        return RegisterModelSerializer(obj.user).data


class CollectManagerSerializer(Serializer):
    manager_id = IntegerField()

    def validate(self, attrs):
        manager_id = attrs['manager_id']
        if not User.objects.filter(pk=manager_id).exists():
            raise NotFound('Manager is not found')
        return attrs


class PlatFormStadiumSerializer(ModelSerializer):
    class Meta:
        model = PlatformStadium
        fields = ['stadium']


class StadiumUpdateSerializer(ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['name', 'region', 'location_note', 'price']
        extra_kwargs = {
            'id': {'read_only': True},
            'owner': {'read_only': True},
            'manager': {'read_only': True},
        }


class StadiumListModelSerializer(ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['name', 'region', 'location_note', 'price']


class CreateOrderModelSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['stadium', 'start_time', 'end_time']

    def save(self, **kwargs):
        data = self.validated_data
        user = self.context.get('request').user
        data['user'] = user
        return Order.objects.create(**data)
