from rest_framework.exceptions import APIException


class SelfSubscribe(APIException):
    status_code = 400
    default_detail = 'Нельзя подписаться на себя'
    default_code = 'bad_request'


class SameSubscribe(SelfSubscribe):
    default_detail = 'Вы уже подписаны на этого автора'
