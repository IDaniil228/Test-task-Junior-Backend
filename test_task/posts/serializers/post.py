from rest_framework import serializers

from posts.models import InstagramPost


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramPost
        fields = '__all__'