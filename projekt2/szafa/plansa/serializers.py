from rest_framework import serializers
from .models import Gra

class GraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gra
        fields = '__all__'

    def validate(self, data):
        min_g = data.get('min_graczy')
        max_g = data.get('max_graczy')
        if min_g is not None and max_g is not None:
            if min_g > max_g:
                raise serializers.ValidationError(
                    {"min_graczy": "Minimalna liczba graczy nie może być większa niż maksymalna!"}
                )
            if min_g < 1:
                raise serializers.ValidationError(
                    {"min_graczy": "Gra musi być przynajmniej dla 1 osoby."}
                )
        czas = data.get('czas_gry')
        if czas is not None and czas <= 0:
            raise serializers.ValidationError(
                {"czas_gry": "Czas gry musi być wartością dodatnią."}
            )
        return data

class MasowySerializer(serializers.Serializer):
    bgg_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="Lista ID gier z BGG do masowego zaimportowania"
    )