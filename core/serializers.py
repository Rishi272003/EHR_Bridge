from rest_framework import serializers

from .models import EHRConnection


class EHRConnectionSerializer(serializers.ModelSerializer):
    ehr_name = serializers.CharField()
    app_type = serializers.CharField()

    class Meta:
        model = EHRConnection
        fields = [
            "id",
            "uuid",
            "ehr_name",
            "app_type",
            "title",
            "client_id",
            "client_secret",
            "scope",
            "connection_status",
        ]


class EHRConnectionPostSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(write_only=True)
    client_secret = serializers.CharField(write_only=True)

    class Meta:
        model = EHRConnection
        exclude = ["access_token_generated_at", "access_token", "refresh_token","refresh_token_generated_at"]


class EHRConnectionPatchSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(write_only=True)
    client_secret = serializers.CharField(write_only=True)

    class Meta:
        model = EHRConnection
        fields = [
            "id",
            "uuid",
            "client_id",
            "client_secret",
            "title",
            "scope",
            "practice_id",
        ]
        read_only_fields = (
            "id",
            "uuid",
        )

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)
