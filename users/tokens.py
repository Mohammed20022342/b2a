from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.timezone import now

class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Use str() directly for Python 3
        return str(user.pk) + str(user.is_email_verified) + str(timestamp)

email_verification_token = EmailVerificationTokenGenerator()
