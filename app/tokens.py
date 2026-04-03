import jwt
import datetime
from django.conf import settings
from .models import tokens, user
from pytz import timezone

secret_key = settings.SECRET_KEY
def generateToken(userId):
    currentTime = datetime.datetime.now(timezone('Asia/Kolkata'))
    expireTime = currentTime + datetime.timedelta(hours=500)
    payload = {
        'user_id': userId,
        'exp': expireTime
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    try:
        userData = user.objects.get(user_id=userId)
    except user.DoesNotExist:
        return {"error":"User not found."}
    tokens.objects.create(user_id=userData, tokens=token,exp_time=expireTime)
    return token

def verifyToken(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload['user_id']
        try:
            userData = user.objects.get(user_id=user_id)
        except user.DoesNotExist:
            return {"error":"User not found."}
        tokenObject = tokens.objects.filter(user_id=userData, tokens=token).first()
        if not tokenObject:
            return {"error": "Token not found."}
        return user_id
    except jwt.ExpiredSignatureError:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'], options={"verify_exp": False})
        user_id = payload['user_id']
        tokenObject = tokens.objects.filter(user_id=user_id, tokens=token).first()
        if tokenObject:
            tokenObject.delete()
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}
    except:
        return {"error": "Token verification failed."}
    
def expireToken(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'], options={"verify_exp": False})
        user_id = payload['user_id']
        try:
            userObj = user.objects.get(user_id=user_id)
        except user.DoesNotExist:
            return {'error': 'User not found.'}
        tokenObject = tokens.objects.filter(user_id=userObj, tokens=token).first()
        if tokenObject:
            tokenObject.delete()
        return "Token expired successfully."
    except:
        return {'error': 'Failed to expire token.'}