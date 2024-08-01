from cryptography.fernet import Fernet
import base64

def get_encryption_key():
    key_file = 'encryption_key.key'
    try:
        with open(key_file, 'rb') as file:
            key = file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as file:
            file.write(key)
    return key

def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()

def write_to_csv(data_to_write, dfile):
    key = get_encryption_key()
    encrypted_data = encrypt_data('\n'.join([','.join(row) for row in data_to_write]), key)
    with open(dfile, 'wb') as file:
        file.write(encrypted_data)
