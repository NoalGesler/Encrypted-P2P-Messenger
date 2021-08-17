from datetime import datetime
from flask import session


class DataBase:
    """
    used to connect, write to and read from a local sqlite3 database
    """

    def __init__(self):
        self.list_of_messages = []
        self.public_key = ''

    def get_all_messages(self, limit=100, name=None):
        """
        returns all messages
        :param name:
        :param limit: int
        :return: list[dict]
        """
        # return messages
        results = []
        print(results)

        for r in results:
            data = [r['Name'], r['Cipher'], str(r['TS'])]
            results.append(data)

        print(results)

        return list(reversed(results))

    def save_message(self, name, msg):
        """
        saves the ciphertext message to the mock database
        :param publickey: str
        :param messages: list
        :param name: str
        :param msg: str
        :return: None
        """
        # encrypt plaintext
        ciphertext = msg
        self.list_of_messages.append({'Name': name, 'Cipher': ciphertext, 'TS': datetime.now()})
        print(self.list_of_messages)

    def save_key(self, key):
        """
        saves the key in mock database
        :param key:
        :return: none
        """
        self.public_key = key

    def get_key(self):
        """
        returns stored key
        :return: key str
        """
        return self.public_key
