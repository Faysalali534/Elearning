from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import UserProfile


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)
    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            registerd_user = authenticate(
                email=email, password='Q5RQ38sZE7Zr0qWWHnXNwf41'
            )
            return {
                'username': registerd_user.username,
                'email': registerd_user.email,
                'tokens': registerd_user.tokens()
            }
        else:
            return AuthenticationFailed(
                detail="Login using " + filtered_user_by_email[0].auth_provider
            )
    else:
        user = {
            'username': name, 'email': email,
            'password': 'Q5RQ38sZE7Zr0qWWHnXNwf41'
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()
        new_user = authenticate(
            email=email, password='Q5RQ38sZE7Zr0qWWHnXNwf41'
        )
        return {
            'username': new_user.username,
            'email': new_user.email,
            'tokens': new_user.tokens()
        }


class Google:
    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())

            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        except:
            return "Token is either invalid or expired"
