from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page_size'


def validate_size_image(file_obj):
    """ Проверка размера файла
    """
    megabyte_limit = 2
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {megabyte_limit}MB")
