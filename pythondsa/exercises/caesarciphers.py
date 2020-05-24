from random import shuffle


class SubstitutionCipher:
    """Class for doing encryption and decryption using a Substitution cipher."""

    def __init__(self, mapping):
        """Construct cipher using a 26-letter mapping for substitution."""
        if len(mapping) != 26:
            raise ValueError('SubstitutionCipher requires a 26-letter mapping.')
        self.charsets = [
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'abcdefghijklmnopqrstuvwxyz'
        ]
        self.mappings = [
            ''.join([l.upper() for l in mapping]),
            ''.join([l.lower() for l in mapping])
        ]
        self._original = ''.join(ch for charset in self.charsets for ch in charset)
        self._shifted = ''.join(ch for mapping in self.mappings for ch in mapping)
        self._encoder = str.maketrans(self._original, self._shifted)
        self._decoder = str.maketrans(self._shifted, self._original)

    def encrypt(self, message):
        """Return string representing encrypted message."""
        return str.translate(message, self._encoder)

    def decrypt(self, secret):
        """Return decrypted message given encrypted secret."""
        return str.translate(secret, self._decoder)


class CaesarCipher(SubstitutionCipher):
    """Class for doing encryption and decryption using a Caesar cipher."""

    def __init__(self, shift):
        """Construct Caesar cipher using given integer shift for rotation."""
        self.charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.mapping = [
            chr((k + shift) % len(self.charset) + ord(self.charset[0]))
            for k in range(len(self.charset))
        ]
        super().__init__(self.mapping)


class RandomCipher(SubstitutionCipher):
    """Class for doing encryption and decryption using a random sequence."""

    def __init__(self):
        """Construct a cipher using a randomly generated letter sequence."""
        self.charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.mapping = [ch for ch in self.charset]
        shuffle(self.mapping)
        super().__init__(self.mapping)


if __name__ == '__main__':
    print('----------------------------------------')
    print('Testing original CaesarCipher in P-5.35:')
    cipher = CaesarCipher(3)
    message = "THE EAGLE IS IN PLAY; MEET AT JOE'S"
    coded = cipher.encrypt(message)
    print('Secret: ', coded)
    answer = cipher.decrypt(coded)
    print('Message: ', answer, '\n')

    print('----------------------------------------')
    print('Testing modification in P-5.36:')
    cipher2 = CaesarCipher(3)
    message2 = "The Eagle is in play; Meet at Joe's"
    coded2 = cipher2.encrypt(message2)
    print('Secret: ', coded2)
    answer2 = cipher2.decrypt(coded2)
    print('Message: ', answer2, '\n')

    print('----------------------------------------')
    print('Testing SubstitutionCipher in P-5.37:')
    m = 'DBEWGFHILJKMOVPCTQARSUXNYZ'
    subs_cipher = SubstitutionCipher(m)
    message3 = "The Eagle is in play; Meet at Joe's"
    coded3 = subs_cipher.encrypt(message3)
    print('Secret: ', coded3)
    answer3 = subs_cipher.decrypt(coded3)
    print('Message: ', answer3, '\n')

    print('----------------------------------------')
    print('Testing SubstitutionCipher in P-5.38:')
    cipher4 = CaesarCipher(3)
    message4 = "The EAGLE is in play; Meet at Joe's"
    coded4 = cipher4.encrypt(message4)
    print('Secret: ', coded4)
    answer4 = cipher4.decrypt(coded4)
    print('Message: ', answer4, '\n')

    print('----------------------------------------')
    print('Testing RandomCipher in P-5.39:')
    cipher5 = RandomCipher()
    message5 = "The EAGLE is in play; Meet at Joe's"
    coded5 = cipher5.encrypt(message5)
    print('Secret: ', coded5)
    answer5 = cipher5.decrypt(coded5)
    print('Message: ', answer5, '\n')
