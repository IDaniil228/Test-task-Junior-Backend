from rest_framework import serializers

from posts.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)