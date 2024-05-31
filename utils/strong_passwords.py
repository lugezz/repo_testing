import string
import secrets


def generate_password(length=12):
    # Define character sets
    alphabet = string.ascii_letters + string.digits + string.punctuation
    # Generate password using random choices from the alphabet
    password = ''.join(secrets.choice(alphabet) for i in range(length))
    return password


password = generate_password(15)
print(password)
