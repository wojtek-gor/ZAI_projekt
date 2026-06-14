from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Gra
from .serializers import GraSerializer, MasowySerializer
from .services import pobieranie_bgg_games, szukaj_po_nazwie_bgg


class ListaGierView(generics.ListAPIView):
    queryset = Gra.objects.all()
    serializer_class = GraSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['min_graczy', 'max_graczy', 'publikacja']
    search_fields = ['tytul', 'opis']
    ordering_fields = ['czas_gry', 'publikacja', 'tytul']


class MasowyView(APIView):

    def post(self, request):
        serializer = MasowySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        bgg_ids = serializer.validated_data['bgg_ids']


        try:
            gry = pobieranie_bgg_games(bgg_ids)

            i = 0
            dodane = []

            for gra in gry:
                if not Gra.objects.filter(bgg_id=gra['bgg_id']).exists():
                    nowa_gra = Gra(
                        bgg_id=gra.get('bgg_id'),
                        tytul=gra.get('tytul'),
                        min_graczy=gra.get('min_graczy'),
                        max_graczy=gra.get('max_graczy'),
                        czas_gry=gra.get('czas_gry'),
                        opis=gra.get('opis'),
                        publikacja=gra.get('publikacja')
                    )
                    dodane.append(nowa_gra)
                    i += 1

            if dodane:
                Gra.objects.bulk_create(dodane)


            return Response({
                "message": f"Masowy import zakończony sukcesem.",
                "detale": f"Przeanalizowano {len(bgg_ids)} ID. Nowo dodanych gier: {i}."
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": "Wystąpił błąd podczas masowego importu.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NowaGraView(generics.ListCreateAPIView):
    queryset = Gra.objects.all()
    serializer_class = GraSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SzukanieNazwaView(APIView):

    def get(self, request):
        query = request.query_params.get('query', None)
        if not query:
            return Response(
                {"error": "Parametr 'query' jest wymagany. Przykład: ?query=catan"},
                status=status.HTTP_400_BAD_REQUEST
            )
        games_data = szukaj_po_nazwie_bgg(query)
        return Response(games_data, status=status.HTTP_200_OK)

class SzczegolyGryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gra.objects.all()
    serializer_class = GraSerializer