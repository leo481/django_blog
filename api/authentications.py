from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class MyAuth(BaseAuthentication):
    '''
    自定义认证示例
    '''
    def authenticate(self, request):
        if request.method in ["POST", "PUT", "DELETE"]:
            request_token = request.data.get("token", None)
            if not request_token:
                raise AuthenticationFailed('缺少token')
            # token_obj = models.Token.objects.filter(token_code=request_token).first()
            # if not token_obj:
            #     raise AuthenticationFailed('无效的token')
            # return token_obj.user.username, None
        else:
            return None, None