from apps.account.models import User


def get_unique_username_from_email(email, prefix="ven"):
    while True:
        username = prefix + email.split('@')[0]
        name, idx = username, 1
        try:
            # user with current username exists, so add numeral
            User.objects.get(username=username)
            name = username + str(idx)
        except User.DoesNotExist:
            username = name
            break
    return username
