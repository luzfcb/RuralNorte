from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def paginate_queryset(self, queryset, request, view=None):
        # q = queryset.only('pk')
        return super(StandardResultsSetPagination, self).paginate_queryset(queryset, request, view)


class CemResultsSetPagination(StandardResultsSetPagination):
    page_size = 100


class OnlyOnePerPagePaginator(StandardResultsSetPagination):
    page_size = 1
    max_page_size = 1
