from cryptography.fernet import Fernet
import os
import cryptography

keyPath = "Data/filekey.key"

def fernKey():
    os.makedirs(os.path.dirname(keyPath), exist_ok=True)

    if os.path.exists(keyPath):
        with open(keyPath, 'rb') as file:
            key = file.read()
        fernet = Fernet(key)
    else:
        key = Fernet.generate_key()
        fernet = Fernet(key)

        # string the key in a file
        with open(keyPath, 'wb') as filekey:
            filekey.write(key)

    return fernet



def encryptCSV(fileToEncrypt, EncryptedFileName):
    key = Fernet.generate_key()

    # string the key in a file
    with open(keyPath, 'wb') as filekey:
        filekey.write(key)

    fernet = Fernet(key)

    with open(fileToEncrypt, 'rb') as file:
        original = file.read()

    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and
    # writing the encrypted data
    with open(EncryptedFileName, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

#encryptCSV("Data/userdata.csv","Data/deUserData.csv")

###

def decryptCSV(fileToDecrypt, DeEncryptedFileName):
    try:
        with open("Data/filekey.key", 'rb') as file:
            key = file.read()
        fernet = Fernet(key)

        with open(fileToDecrypt, 'rb') as enc_file:
            encrypted = enc_file.read()

        decrypted = fernet.decrypt(encrypted)

        with open(DeEncryptedFileName, 'wb') as dec_file:
            dec_file.write(decrypted)

        return DeEncryptedFileName
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except PermissionError:
        print(f"Permission denied when trying to access files")
    except cryptography.fernet.InvalidToken:
        print("Invalid token: The key may be incorrect or the data may be corrupted")
    except Exception as e:
        print(f"Unexpected error in decryptCSV: {e}")
    return None

#decryptCSV("Data/eUserData.csv","Data/deUserData.csv")