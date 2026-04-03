import jwt
import datetime
from django.conf import settings
from .models import deliveryTokens, deliveryPerson
from pytz import timezone

secret_key = settings.SECRET_KEY


def generateDeliveryToken(deliveryId):
    currentTime = datetime.datetime.now(timezone('Asia/Kolkata'))
    expireTime = currentTime + datetime.timedelta(hours=500)

    payload = {
        'delivery_id': deliveryId,
        'exp': expireTime
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')

    try:
        deliveryData = deliveryPerson.objects.get(
            delivery_person_id=deliveryId
        )
    except deliveryPerson.DoesNotExist:
        return {"error": "Delivery person not found."}

    deliveryTokens.objects.create(
        delivery_person_id=deliveryData,
        tokens=token,
        exp_time=expireTime
    )

    return token

def verifyDeliveryToken(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        delivery_id = payload['delivery_id']

        try:
            deliveryData = deliveryPerson.objects.get(
                delivery_person_id=delivery_id
            )
        except deliveryPerson.DoesNotExist:
            return {"error": "Delivery person not found."}

        tokenObject = deliveryTokens.objects.filter(
            delivery_person_id=deliveryData,
            tokens=token
        ).first()

        if not tokenObject:
            return {"error": "Token not found."}

        return delivery_id

    except jwt.ExpiredSignatureError:
        return {"error": "Token expired."}

    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}

    except:
        return {"error": "Token verification failed."}
    
def expireDeliveryToken(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'], options={"verify_exp": False})
        delivery_id = payload['delivery_id']

        deliveryObj = deliveryPerson.objects.get(
            delivery_person_id=delivery_id
        )

        tokenObject = deliveryTokens.objects.filter(
            delivery_person_id=deliveryObj,
            tokens=token
        ).first()

        if tokenObject:
            tokenObject.delete()

        return "Token expired successfully."

    except:
        return {"error": "Failed to expire token."}