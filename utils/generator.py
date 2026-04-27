import secrets
import string


combination = string.ascii_letters + string.digits + string.punctuation



def PassGenerator(length):
    
    
    password = ''.join(secrets.choice(combination) for i in range(length))

    return password
    