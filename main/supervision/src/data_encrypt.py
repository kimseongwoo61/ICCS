# AES 알고리즘 및 안전한 난수생성 용도
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets

# 경로 설정 등의 목적
import os

# 동작 로깅용도
import logging
logger = logging.getLogger('django')


# 암복호를 위한 AES 키 생성
# input : AES 키가 저장될 절대 경로
# output : void
def generate_aes_key(save_dir):
    
    # 저장경로가 없다고 판단되면 생성한다.
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    
    # 키를 저장할 경로를 설정한다.
    key_dir = os.path.join(save_dir, "aes.key")
    
    # 안전한 랜덤키 256-bit를 생성 후 파일로 저장한다.
    with open(key_dir, "wb") as f:
        key = secrets.token_bytes(32)  # 256-bit AES key
        f.write(key)
        f.close()


# AES 암호화를 진행하는 함수 
# input : 암호화할 평문, AES 키 경로
# return : 암호화된 데이터(bytes)
def encrypt_aes(plaintext, aes_key_dir):
    
    # 키 파일이 없으면 종료
    if not os.path.exists(aes_key_dir):
        return False
    
    # AES 키를 읽어드린다.
    with open(aes_key_dir, "rb") as f:
        aes_key = f.read()  # 256-bit AES key
        f.close()
    
    # iv 및 암호화를 위한 세팅을 진행한다.
    iv = secrets.token_bytes(16)  # Initialization Vector
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    
    # 바이트형 암호문을 반환한다.
    ciphertext = encryptor.update(plaintext.encode("utf-8")) + encryptor.finalize()
    return iv + ciphertext


# AES 복호화를 진행하는 함수
# input : 복호화할 암호문, AES 키 경로
# return : 복호화된 평문 데이터(string)
def decrypt_aes(ciphertext, aes_key_dir):
    
    # 키 파일이 없으면 종료
    if not os.path.exists(aes_key_dir):
        return False
    
    with open(aes_key_dir, "rb") as f:
        aes_key = f.read()  # 256-bit AES key
        f.close()
    
    # iv 및 복호화를 위한 세팅을 진행한다.
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    
    # 바이트형 복호화된 평문을 반환한다.
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode("utf-8")




