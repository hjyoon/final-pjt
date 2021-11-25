from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import UserSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def check_connection(request):
    data = {
        'success': True,
        'message': 'hello!', 
    }
    return Response(data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    # 데이터 입력
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        # 유저 모델 인스턴스 반환
        user = serializer.save()
        # 암호 저장
        user.set_password(request.data.get('password'))
        # 인스턴스 저장
        user.save()

        serializer.data.setdefault('success', True)
        return Response(serializer.data, status.HTTP_201_CREATED)

    else:
        data = {
            'success': False,
            'error': 'validation failed during serialization'
        }
        return Response(data, status.HTTP_422_UNPROCESSABLE_ENTITY)


def jwt_response_payload_handler(token, user=None, request=None):
    """
    로그인 시 response data에 사용자 ID와 이름을 추가해서 반환
    """
    return {
        'token': token,
        'user': UserSerializer(user).data,
    }