from rest_framework.pagination import CursorPagination, PageNumberPagination

class FeedCursorPagination(CursorPagination):
    page_size = 10
    ordering = "-created_at"
    cursor_query_param = "cursor"

class CommentCursorPagination(CursorPagination):
    page_size = 20
    ordering = "-created_at"
    cursor_query_param = "cursor"

class LikePagePagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"

class SearchPagePagination(PageNumberPagination):
    page_size = 20
    page_query_param = "page"
