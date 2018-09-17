import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token':token,
        'user_id':user.id,
        'username':user.username
    }


class UsernameMobileAuthBackend(ModelBackend):
    # 自定义用户名或手机号验证
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 匹配手机格式
            if re.match(r'^1[3-9]\d{9}$', username):
                user = User.objects.get(mobile=username)
            else:
                user = User.objects.get(username=username)
        except:
            user = None

        # 密码校验
        if user is not None and user.check_password(password):
            return user
        return user
