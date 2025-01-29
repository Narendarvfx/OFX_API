from rest_framework.response import Response
from rest_framework.views import APIView

# from .models import Elements

# from .serializers import ElementsSerializer

class Dynamicfilters(APIView):

    def get(self, request, format=None):
        return Response({})
        # """
        # Filter Arguments:
        #     'element_id',
        #     'project_id',
        #     'shot_id',
        #     'seq_id'.
        # [ref]: /api/production/elements/?element_id=''&project_id=''&shot_id=''
        # """
        # query_params = self.request.query_params
        # argumentos = {}
        # if query_params.get('element_id'):
        #     argumentos['pk'] = query_params.get('element_id')
        # if query_params.get('project_id'):
        #     argumentos['project_id'] = query_params.get('project_id')
        # if query_params.get('seq_id'):
        #     argumentos['seq_id'] = query_params.get('seq_id')
        # if query_params.get('shot_id'):
        #     argumentos['shot_id'] = query_params.get('shot_id')
        # if len(argumentos) > 0:
        #     element = Elements.objects.select_related('shot_id__sequence', 'shot_id__task_type',
        #                                               'shot_id__sequence__project',
        #                                               'shot_id__sequence__project__client', 'status',
        #                                               'shot_id__complexity', 'shot_id__team_lead',
        #                                               'shot_id__artist', 'location',
        #                                               'shot_id__sequence__project__client__locality').filter(
        #         **argumentos)

        # else:
        #     element = Elements.objects.select_related('shot_id__sequence', 'shot_id__task_type',
        #                                               'shot_id__sequence__project',
        #                                               'shot_id__sequence__project__client', 'status',
        #                                               'shot_id__complexity', 'shot_id__team_lead',
        #                                               'shot_id__artist', 'location',
        #                                               'shot_id__sequence__project__client__locality').all().exclude(
        #         shot_id__sequence__project__status="ARCHIVED")

        # serializer = ElementsSerializer(element, many=True, context={"request": request})
        # return Response(serializer.data)

