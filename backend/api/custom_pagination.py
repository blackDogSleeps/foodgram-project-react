from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class PageLimitPagination(PageNumberPagination):
	page_size_query_param = 'limit'