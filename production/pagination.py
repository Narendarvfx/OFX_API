from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ShotModelPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class OFXPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, draw, data):
        res_data = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'recordsFiltered': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'recordsTotal': self.page.paginator.count,
            'data': data
        }
        if draw:
            res_data['draw'] = draw
        return Response(res_data)
