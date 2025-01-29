from rest_framework.response import Response
from rest_framework.views import APIView

from history.models import ShotsHistory
from history.serializers import ShotsHistorySerializer


class ShotHistoryAPI(APIView):

    def get(self, request, format=None):
        query_params = self.request.query_params
        from_date = query_params.get('from_date', None)
        to_date = query_params.get('to_date', None)
        argumentos = {}
        if query_params.get('shot_id'):
            argumentos['target__id'] = query_params.get('shot_id')
        if query_params.get('field'):
            argumentos['dataField__iexact'] = query_params.get('field')
        if query_params.get('toData'):
            argumentos['toData__iexact'] = query_params.get('toData')
        if from_date is not None and to_date is not None:
            argumentos['created_at__range'] = [from_date, to_date]

        if len(argumentos) > 0:
            shothistory = ShotsHistory.objects.select_related('target', 'parent_target').filter(
                **argumentos).all()
        else:
            shothistory = []

        serializer = ShotsHistorySerializer(shothistory, many=True, context={"request": request})
        return Response(serializer.data)