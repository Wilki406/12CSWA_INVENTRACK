from cryptography.fernet import Fernet
import os
import cryptography


def ensureDirectory(file_path):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)



def GetOrCreateKey(key_path):
    ensureDirectory(key_path)
    if os.path.exists(key_path):
        with open(key_path, 'rb') as file:
            key = file.read()
    else:
        key = Fernet.generate_key()
        with open(key_path, 'wb') as filekey:
            filekey.write(key)
    return Fernet(key)



def encryptCSV(fileToEncrypt, encryptedFileName, key_path="Data/filekey.key"):
    try:
        fernet = GetOrCreateKey(key_path)

        with open(fileToEncrypt, 'rb') as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        ensureDirectory(encryptedFileName)
        with open(encryptedFileName, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        return encryptedFileName

    except FileNotFoundError as e:
        print(f" en File not found: {e.filename}")
    except PermissionError:
        print(f"Permission denied when trying to access files")
    except Exception as e:
        print(f"Unexpected error in encryptCSV: {e}")
    return None



###

def decryptCSV(fileToDecrypt, decryptedFileName, key_path="Data/filekey.key"):
    try:
        fernet = GetOrCreateKey(key_path)

        with open(fileToDecrypt, 'rb') as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        ensureDirectory(decryptedFileName)
        with open(decryptedFileName, 'wb') as dec_file:
            dec_file.write(decrypted)

        return decryptedFileName

    except FileNotFoundError as e:
        print(f" de File not found: {e.filename}")
    except PermissionError:
        print(f"Permission denied when trying to access files")
    except cryptography.fernet.InvalidToken:
        print("Invalid token: The key may be incorrect or the data may be corrupted")
    except Exception as e:
        print(f"Unexpected error in decryptCSV: {e}")
    return None
