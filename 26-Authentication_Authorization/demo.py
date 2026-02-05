"""
JWT + Password Hashing Demo
---------------------------
This file demonstrates:
1. How passwords are hashed and verified
2. How a JWT access token is created
3. How a JWT is validated and used for authorization

Goal:
- Explain authentication vs authorization in simple terms
"""

import jwt
import bcrypt
import time

# =========================================================
# CONFIGURATION
# =========================================================

# Secret key used to SIGN the JWT
# IMPORTANT:
# - This is NOT encryption
# - This key must be kept secret
# - In real systems, store this in ENV variables
SECRET_KEY = "supersecretkey"

# Algorithm used to sign the token
ALGO = "HS256"


# =========================================================
# PASSWORD HASHING (AUTHENTICATION STEP)
# =========================================================

# User enters a password during signup
password = b"mypassword"

# Convert the password into a one-way hash
# - bcrypt automatically adds a salt
# - The original password can NEVER be recovered
hashed_pwd = bcrypt.hashpw(password, bcrypt.gensalt())

print("Stored password hash:")
print(hashed_pwd)

# ---- LOGIN CHECK ----
# User enters password during login
login_pwd = b"mypassword"

# We hash the login password and compare hashes
# If hashes match → password is correct
if bcrypt.checkpw(login_pwd, hashed_pwd):
    print("\nPassword verified ✅")
else:
    print("\nInvalid password ❌")


# =========================================================
# JWT CREATION (ACCESS TOKEN ISSUANCE)
# =========================================================

# Payload = user information + token rules
# NOTE:
# - Payload is NOT encrypted
# - Anyone can read it
# - Never store secrets here
payload = {
    "user_id": 101,              # Who the user is
    "role": "admin",             # What the user can do
    "exp": int(time.time()) + 30 # Token expires in 30 seconds
}

# Create (sign) the JWT
# Signature proves:
# - Token was issued by us
# - Token was not tampered with
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)

print("\nGenerated JWT (Access Token):")
print(token)


# =========================================================
# JWT VALIDATION (EVERY API REQUEST)
# =========================================================

try:
    # Decode + validate the token
    # This automatically checks:
    # 1. Signature validity
    # 2. Token expiry (exp)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])

    print("\nToken is valid ✅")
    print("Decoded payload:")
    print(decoded)

    # =====================================================
    # AUTHORIZATION CHECK
    # =====================================================

    # Even after authentication, we still check permissions
    if decoded["role"] == "admin":
        print("\nAccess granted → You can switch off the light 💡")
    else:
        print("\nAccess denied → Not allowed to switch off the light ❌")

# Token expired
except jwt.ExpiredSignatureError:
    print("\nToken expired ❌")

# Token invalid or tampered
except jwt.InvalidTokenError:
    print("\nInvalid token ❌")


"""
KEY TAKEAWAYS
---------------------
1. Passwords are never stored, only hashes
2. JWT proves trust using a signature
3. Expiry limits damage if token is stolen
4. Authentication ≠ Authorization
"""
