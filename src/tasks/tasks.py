from celery import Celery
from core.config import settings


celery = Celery("tasks", broker=settings.redis_url, backend=settings.redis_url)

# Not useful. Just for fun
@celery.task
def generate_referral_code():
    import uuid
    import hashlib

    # Generate a random UUID
    random_uuid = uuid.uuid4()

    # Create a SHA-256 hash of the UUID
    sha256_hash = hashlib.sha256(random_uuid.bytes).hexdigest()

    # Take the first 8 characters of the hash as the referral code
    referral_code = sha256_hash[:8].upper()
    return referral_code
