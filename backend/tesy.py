from security import hash_password, verify_password

hashed = hash_password("test123")

print(hashed)
print(verify_password("test123", hashed))
print(verify_password("wrong123", hashed))