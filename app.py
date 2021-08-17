from urllib.request import localhost

from flask import session
from flask_socketio import SocketIO
import time
from Application import create_app
from Application.crypt import des3_encrypt, des3_decrypt, Random, DES3
import config
from config import db

# SETUP
app = create_app()
socketio = SocketIO(app)  # used for user communication

# COMMUNICATION FUNCTIONS


@socketio.on('event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    """
    handles saving messages once received from web server
    and sending message to other clients
    :param json: json
    :param methods: POST GET
    :return: None
    """
    print(json)
    data = dict(json)
    # encrypt plaintext
    key = db.get_key()
    # iv = key[-8:]
    iv = Random.new().read(DES3.block_size)  # DES3.block_size==8

    ciphertext = des3_encrypt(key, iv, data["message"])
    print(str(ciphertext))

    # save encrypted messages in database
    if "name" in data:
        config.db.save_message(data["name"], str(ciphertext))

    data["message"] = ciphertext

    print("message:")
    print(data["message"])

    plaintext = des3_decrypt(key, iv, ciphertext)

    print("Ciphertext: ", ciphertext)
    print("Plaintext: ", plaintext)

    ciphertext = str(ciphertext)
    plaintext = str(plaintext)

    json["message"] = plaintext + "\nCiphertext:" + ciphertext

    socketio.emit('message response', json)

# MAINLINE


if __name__ == "__main__":  # start the web server
    socketio.run(app, debug=True, host=str(config.Config.SERVER))
