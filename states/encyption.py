from aiogram.fsm.state import State, StatesGroup

class Encryption(StatesGroup):
    encrypt_text = State()

class Decryption(StatesGroup):
    decrypt_text = State()