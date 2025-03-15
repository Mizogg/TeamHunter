"""

@author: Team Mizogg
"""
import codecs, hashlib, ecdsa

# BrainWallet
class BrainWallet:
    @staticmethod
    def generate_address_from_passphrase(passphrase):
        private_key = str(hashlib.sha256(
            passphrase.encode('utf-8')).hexdigest())
        address =  BrainWallet.generate_address_from_private_key(private_key)
        return private_key, address

    @staticmethod
    def generate_address_from_private_key(private_key):
        public_key = BrainWallet.__private_to_public(private_key)
        address = BrainWallet.__public_to_address(public_key)
        return address

    @staticmethod
    def __private_to_public(private_key):
        private_key_bytes = codecs.decode(private_key, 'hex')
        key = ecdsa.SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
        key_bytes = key.to_string()
        key_hex = codecs.encode(key_bytes, 'hex')
        bitcoin_byte = b'04'
        public_key = bitcoin_byte + key_hex
        return public_key

    @staticmethod
    def __public_to_address(public_key):
        public_key_bytes = codecs.decode(public_key, 'hex')
        sha256_bdec = hashlib.sha256(public_key_bytes)
        sha256_bdec_digest = sha256_bdec.digest()
        ripemd160_bdec = hashlib.new('ripemd160')
        ripemd160_bdec.update(sha256_bdec_digest)
        ripemd160_bdec_digest = ripemd160_bdec.digest()
        ripemd160_bdec_hex = codecs.encode(ripemd160_bdec_digest, 'hex')
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemd160_bdec_hex
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex')
        sha256_nbdec = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_nbdec_digest = sha256_nbdec.digest()
        sha256_2_nbdec = hashlib.sha256(sha256_nbdec_digest)
        sha256_2_nbdec_digest = sha256_2_nbdec.digest()
        sha256_2_hex = codecs.encode(sha256_2_nbdec_digest, 'hex')
        checksum = sha256_2_hex[:8]
        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')
        wallet = BrainWallet.base58(address_hex)
        return wallet

    @staticmethod
    def base58(address_hex):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        b58_string = ''
        leading_zeros = len(address_hex) - len(address_hex.lstrip('0'))
        address_int = int(address_hex, 16)
        while address_int > 0:
            digit = address_int % 58
            digit_char = alphabet[digit]
            b58_string = digit_char + b58_string
            address_int //= 58
        ones = leading_zeros // 2
        for one in range(ones):
            b58_string = '1' + b58_string
        return b58_string
