from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            phone_number=validated_data["phone_number"]
        )
        user.set_password(validated_data["password"])
        user.save()
        owner_id = User.objects.get(username=user.username).id
        print(f'owner_id: {owner_id}')

        return user

    class Meta:
        model = User
        fields = ["pk", "username", "password", "phone_number"]
