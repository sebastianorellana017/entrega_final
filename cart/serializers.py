from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ColourVariation, SizeVariation, Order, Product, OrderItem, Payment, Category, Address


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ColourVariationSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(required=False)
    class Meta:
        model = ColourVariation
        fields = ['name']
        read_only_fields = ['name']


class SizeVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariation
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):

    #available_sizes = serializers.SlugRelatedField(
    #    many=True,
    #    read_only=True,
    #    slug_field='name'
    #)

    #available_colours = ColourVariationSerializer(many=True, read_only=True)
    categoria = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'nombre', 'marca','image', 'descripcion', 'peso','valor', 'active', 'categoria', 'cantidad']

class OrderItemSerializer(serializers.ModelSerializer):

    product = serializers.SlugRelatedField(slug_field="nombre", queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    #billing_address = serializers.SlugRelatedField(slug_field="billing_address", queryset=Address.objects.all())
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    #last_name = serializers.SlugRelatedField(slug_field="last_name", queryset=User.objects.all())

    billing_address = serializers.SlugRelatedField(slug_field="address_line_1", queryset=Address.objects.all())
    shipping_address = serializers.SlugRelatedField(slug_field="address_line_2", queryset=Address.objects.all())
    
    class Meta:
        model = Order
        #fields = '__all__'
        fields = ['user','start_date', 'ordered_date', 'ordered','billing_address','shipping_address']

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validate_data):
        instance = User()
        instance.first_name = validate_data.get('first_name')
        instance.last_name = validate_data.get('last_name')
        instance.username = validate_data.get('username')
        instance.email = validate_data.get('email')
        instance.set_password(validate_data.get('password'))
        instance.save()

        return instance

    def validate_username(self, data):
        users = User.objects.filter(username=data)
        if len(users) != 0:
            raise serializers.ValidationError(
                "Este nombre de usuario ya existe")
        else:
            return data
