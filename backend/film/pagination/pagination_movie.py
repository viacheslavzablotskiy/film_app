
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from film.models import Movie


class PaginationMovies(PageNumberPagination):
    page_size = 2
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


# class Pagination(PageNumberPagination):
#     page_size = 20
#     page_query_param = 'page_size'


#
# def validate_size_image(file_obj):
#     """ Проверка размера файла
#     """
#     megabyte_limit = 2
#     if file_obj.size > megabyte_limit * 1024 * 1024:
#         raise ValidationError(f"Максимальный размер файла {megabyte_limit}MB")



# class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass
#
#
# class MovieFilter(filters.FilterSet):
#     genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
#     year = filters.RangeFilter()
#
#     class Meta:
#         model = Movie
#         fields = ['genres', 'year']
