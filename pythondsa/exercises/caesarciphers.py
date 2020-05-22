class CaesarCipher:
    """Class for doing encryption and decryption using a CaesarCipher."""

    def __init__(self, shift):
        """Construct Caesar cipher using given integer shift for rotation."""
        charsets = [
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'abcdefghijklmnopqrstuvwxyz'
        ]
        original_seq = []
        shifted_seq = []
        for c in charsets:
            original_seq.extend(ch for ch in c)
            shifted_seq.extend(
                [chr((k + shift) % len(c) + ord(c[0])) for k in range(len(c))])
        self._original = ''.join(original_seq)
        self._shifted = ''.join(shifted_seq)
        self._encoder = str.maketrans(self._original, self._shifted)
        self._decoder = str.maketrans(self._shifted, self._original)

    def encrypt(self, message):
        """Return string representing encrypted message."""
        return str.translate(message, self._encoder)

    def decrypt(self, secret):
        """Return decrypted message given encrypted secret."""
        return str.translate(secret, self._decoder)


if __name__ == '__main__':
    print('Testing original CaesarCipher example:')
    cipher = CaesarCipher(3)
    message = "THE EAGLE IS IN PLAY; MEET AT JOE'S"
    coded = cipher.encrypt(message)
    print('Secret: ', coded)
    answer = cipher.decrypt(coded)
    print('Message: ', answer, '\n')

    print('Testing modification in P-5.36')
    cipher2 = CaesarCipher(3)
    message2 = "The Eagle is in play; Meet at Joe's"
    coded2 = cipher2.encrypt(message2)
    print('Secret: ', coded2)
    answer2 = cipher2.decrypt(coded2)
    print('Message: ', answer2, '\n')
