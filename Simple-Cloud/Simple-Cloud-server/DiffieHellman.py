import hashlib
import os


class DiffieHellman:
    # RFC3526
    # 6.  6144-bit MODP Group
    #    This group is assigned id 17.
    #    This prime is: 2^6144 - 2^6080 - 1 + 2^64 * { [2^6014 pi] + 929484 }
    #    Its hexadecimal value is:
    #    FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1 29024E08
    #    8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD EF9519B3 CD3A431B
    #    302B0A6D F25F1437 4FE1356D 6D51C245 E485B576 625E7EC6 F44C42E9
    #    A637ED6B 0BFF5CB6 F406B7ED EE386BFB 5A899FA5 AE9F2411 7C4B1FE6
    #    49286651 ECE45B3D C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8
    #    FD24CF5F 83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
    #    670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B E39E772C
    #    180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9 DE2BCBF6 95581718
    #    3995497C EA956AE5 15D22618 98FA0510 15728E5A 8AAAC42D AD33170D
    #    04507A33 A85521AB DF1CBA64 ECFB8504 58DBEF0A 8AEA7157 5D060C7D
    #    B3970F85 A6E1E4C7 ABF5AE8C DB0933D7 1E8C94E0 4A25619D CEE3D226
    #    1AD2EE6B F12FFA06 D98A0864 D8760273 3EC86A64 521F2B18 177B200C
    #    BBE11757 7A615D6C 770988C0 BAD946E2 08E24FA0 74E5AB31 43DB5BFC
    #    E0FD108E 4B82D120 A9210801 1A723C12 A787E6D7 88719A10 BDBA5B26
    #    99C32718 6AF4E23C 1A946834 B6150BDA 2583E9CA 2AD44CE8 DBBBC2DB
    #    04DE8EF9 2E8EFC14 1FBECAA6 287C5947 4E6BC05D 99B2964F A090C3A2
    #    233BA186 515BE7ED 1F612970 CEE2D7AF B81BDD76 2170481C D0069127
    #    D5B05AA9 93B4EA98 8D8FDDC1 86FFB7DC 90A6C08F 4DF435C9 34028492
    #    36C3FAB4 D27C7026 C1D4DCB2 602646DE C9751E76 3DBA37BD F8FF9406
    #    AD9E530E E5DB382F 413001AE B06A53ED 9027D831 179727B0 865A8918
    #    DA3EDBEB CF9B14ED 44CE6CBA CED4BB1B DB7F1447 E6CC254B 33205151
    #    2BD7AF42 6FB8F401 378CD2BF 5983CA01 C64B92EC F032EA15 D1721D03
    #    F482D7CE 6E74FEF6 D55E702F 46980C82 B5A84031 900B1C9E 59E7C97F
    #    BEC7E8F3 23A97A7E 36CC88BE 0F1D45B7 FF585AC5 4BD407B2 2B4154AA
    #    CC8F6D7E BF48E1D8 14CC5ED2 0F8037E0 A79715EE F29BE328 06A1D58B
    #    B7C5DA76 F550AA3D 8A1FBFF0 EB19CCB1 A313D55C DA56C9EC 2EF29632
    #    387FE8D7 6E3C0468 043E8F66 3F4860EE 12BF2D5B 0B7474D6 E694F91E
    #    6DCC4024 FFFFFFFF FFFFFFFF
    #    The generator is: 2.
    __predefined_P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AAAC42DAD33170D04507A33A85521ABDF1CBA64ECFB850458DBEF0A8AEA71575D060C7DB3970F85A6E1E4C7ABF5AE8CDB0933D71E8C94E04A25619DCEE3D2261AD2EE6BF12FFA06D98A0864D87602733EC86A64521F2B18177B200CBBE117577A615D6C770988C0BAD946E208E24FA074E5AB3143DB5BFCE0FD108E4B82D120A92108011A723C12A787E6D788719A10BDBA5B2699C327186AF4E23C1A946834B6150BDA2583E9CA2AD44CE8DBBBC2DB04DE8EF92E8EFC141FBECAA6287C59474E6BC05D99B2964FA090C3A2233BA186515BE7ED1F612970CEE2D7AFB81BDD762170481CD0069127D5B05AA993B4EA988D8FDDC186FFB7DC90A6C08F4DF435C93402849236C3FAB4D27C7026C1D4DCB2602646DEC9751E763DBA37BDF8FF9406AD9E530EE5DB382F413001AEB06A53ED9027D831179727B0865A8918DA3EDBEBCF9B14ED44CE6CBACED4BB1BDB7F1447E6CC254B332051512BD7AF426FB8F401378CD2BF5983CA01C64B92ECF032EA15D1721D03F482D7CE6E74FEF6D55E702F46980C82B5A84031900B1C9E59E7C97FBEC7E8F323A97A7E36CC88BE0F1D45B7FF585AC54BD407B22B4154AACC8F6D7EBF48E1D814CC5ED20F8037E0A79715EEF29BE32806A1D58BB7C5DA76F550AA3D8A1FBFF0EB19CCB1A313D55CDA56C9EC2EF29632387FE8D76E3C0468043E8F663F4860EE12BF2D5B0B7474D6E694F91E6DCC4024FFFFFFFFFFFFFFFF
    __predefined_G = 2

    def __init__(self, prime_number=None, generator=None, key_length=2048):
        if prime_number is None:
            self.primeNumber = self.__predefined_P
        else:
            self.primeNumber = prime_number
        if generator is None:
            self.generator = self.__predefined_G
        else:
            self.generator = generator
        self.__generate_private_key(key_length)
        self.__generate_public_key()

    def __generate_private_key(self, key_length=2048):
        self.privateKey = int.from_bytes(os.urandom(key_length), byteorder='big')

    def __generate_public_key(self):
        self.publicKey = pow(self.generator, self.privateKey, self.primeNumber)

    def generateKey(self, collaborator_key):
        _sharedSecret = pow(collaborator_key, self.privateKey, self.primeNumber)
        self.symmectricKey = hashlib.sha256(str(_sharedSecret).encode('utf-8')).digest()


if __name__ == '__main__':

    alice = DiffieHellman()
    bob = DiffieHellman()

    alice.generateKey(bob.publicKey)
    bob.generateKey(alice.publicKey)

    if alice.symmectricKey == bob.symmectricKey:
        print("OK")
    else:
        print("keys does NOT match!")
