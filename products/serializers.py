from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializers(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(),
                                   required=True, allow_empty=False,
                                   allow_null=False)

    class Meta:
        model = ProductImage
        fields = ('images',)

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        images = validated_data.get('images', [])
        def upload_image(image):
            if image.name.split('.')[-1].lower() in ['png', 'jpg', 'gif'] and \
                    image.size < 3000:
                image_name = image.name
                image.name = get_random_string(30) + "." + image.split('.')[-1]
                return ProductImage(name=image_name,
                                    image=image,
                                    uploaded_by=user)
        bulk_data = list(map(upload_image, images))
        instance = ProductImage.objects.bulk_create(bulk_data)
        return instance


class ProductCreateSerializers(serializers.ModelSerializer):
    product_image = serializers.ListField(
        child=serializers.IntegerField(default=0), required=True,
        allow_empty=False, allow_null=False)
    product_price = serializers.DecimalField(required=True, allow_null=False,
                                             max_digits=200, decimal_places=2)
    available_stock = serializers.IntegerField(required=True, allow_null=False)

    class Meta:
        model = Product
        fields = ('name', 'description', 'product_price', 'available_stock',
                  'product_image',)

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        attrs['created_by'] = user
        if not attrs.get('name'):
            raise ValueError({'details': 'product name is required'})
        if not attrs.get('description'):
            raise ValueError({'details': 'product description is required'})
        if attrs.get('product_image'):
            product_image_obj = []
            for product_image_id in attrs.get('product_image'):
                if ProductImage.objects.filter(
                        id=product_image_id, uploaded_by=user).exists():
                    product_image_obj.append(ProductImage.objects.get(id=product_image_id))
            attrs['product_image'] = product_image_obj
        return attrs

    def create(self, validated_data):
        product_images = validated_data.pop('product_image', [])
        instance = super(ProductCreateSerializers, self).create(validated_data)
        if product_images:
            for product_image in product_images:
                product_image.product = instance
                product_image.save()
        return instance


class ProductListSerializers(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_price', 'available_stock',
                  'product_image',)

    def get_product_image(self, obj):
        return ProductImageSerializers(
            ProductImage.objects.filter(product=obj).first()).data


class ProductDetailSerializers(serializers.ModelSerializer):
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'product_price', 'description', 'available_stock',
                  'product_image',)

    def get_product_image(self, obj):
        return ProductImageSerializers(
            ProductImage.objects.filter(product=obj), many=True).data
