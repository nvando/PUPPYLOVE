from hashlib import sha3_512


# Note that this way of storing usernames and passwords is nothing like
# how it would be done in a real application, but it suffices for this
# exercise application.




def hash_password(password):
    return sha3_512(password.encode("utf-8")).hexdigest()
