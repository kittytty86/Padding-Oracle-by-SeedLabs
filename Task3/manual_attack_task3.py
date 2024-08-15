#!/usr/bin/python3
import socket
from binascii import hexlify, unhexlify

# XOR two bytearrays
def xor(first, second):
   return bytearray(x^y for x,y in zip(first, second))

class PaddingOracle:

    def __init__(self, host, port) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        ciphertext = self.s.recv(4096).decode().strip()
        self.ctext = unhexlify(ciphertext)

    def decrypt(self, ctext: bytes) -> None:
        self._send(hexlify(ctext))
        return self._recv()

    def _recv(self):
        resp = self.s.recv(4096).decode().strip()
        return resp 

    def _send(self, hexstr: bytes):
        self.s.send(hexstr + b'\n')

    def __del__(self):
        self.s.close()


if __name__ == "__main__":
    oracle = PaddingOracle('10.9.0.80', 6000)

    # Get the IV + Ciphertext from the oracle
    iv_and_ctext = bytearray(oracle.ctext)
    IV    = iv_and_ctext[00:16]
    C1    = iv_and_ctext[16:32]  # 1st block of ciphertext
    C2    = iv_and_ctext[32:48]  # 2nd block of ciphertext
    C3    = iv_and_ctext[48:64]  # 3nd block of ciphertext
    print("iv_and_ctext:  " + iv_and_ctext.hex())
    print("IV:  " + IV.hex())
    print("C1:  " + C1.hex())
    print("C2:  " + C2.hex())
    print("C3:  " + C3.hex())

    ###############################################################
    # Here, we initialize D2 with C1, so when they are XOR-ed,
    # The result is 0. This is not required for the attack.
    # Its sole purpose is to make the printout look neat.
    # In the experiment, we will iteratively replace these values.
    D3 = bytearray(16)

    D3[0]  = C2[0]
    D3[1]  = C2[1]
    D3[2]  = C2[2]
    D3[3]  = C2[3]
    D3[4]  = C2[4]
    D3[5]  = C2[5]
    D3[6]  = C2[6]
    D3[7]  = C2[7]
    D3[8]  = C2[8]
    D3[9]  = C2[9]
    D3[10] = C2[10]
    D3[11] = C2[11]
    D3[12] = C2[12]
    D3[13] = C2[13]
    D3[14] = C2[14]
    D3[15] = C2[15]
    
    D2 = bytearray(16)

    D2[0]  = C1[0]
    D2[1]  = C1[1]
    D2[2]  = C1[2]
    D2[3]  = C1[3]
    D2[4]  = C1[4]
    D2[5]  = C1[5]
    D2[6]  = C1[6]
    D2[7]  = C1[7]
    D2[8]  = C1[8]
    D2[9]  = C1[9]
    D2[10] = C1[10]
    D2[11] = C1[11]
    D2[12] = C1[12]
    D2[13] = C1[13]
    D2[14] = C1[14]
    D2[15] = C1[15]
    
    D1 = bytearray(16)

    D1[0]  = IV[0]
    D1[1]  = IV[1]
    D1[2]  = IV[2]
    D1[3]  = IV[3]
    D1[4]  = IV[4]
    D1[5]  = IV[5]
    D1[6]  = IV[6]
    D1[7]  = IV[7]
    D1[8]  = IV[8]
    D1[9]  = IV[9]
    D1[10] = IV[10]
    D1[11] = IV[11]
    D1[12] = IV[12]
    D1[13] = IV[13]
    D1[14] = IV[14]
    D1[15] = IV[15]
    ###############################################################
    # In the experiment, we need to iteratively modify CC1
    # We will send this CC1 to the oracle, and see its response.
    CC2 = bytearray(16)

    CC2[0]  = 0x00
    CC2[1]  = 0x00
    CC2[2]  = 0x00
    CC2[3]  = 0x00
    CC2[4]  = 0x00
    CC2[5]  = 0x00
    CC2[6]  = 0x00
    CC2[7]  = 0x00
    CC2[8]  = 0x00
    CC2[9]  = 0x00
    CC2[10] = 0x00
    CC2[11] = 0x00
    CC2[12] = 0x00
    CC2[13] = 0x00
    CC2[14] = 0x00
    CC2[15] = 0x00
    
    CC1 = bytearray(16)

    CC1[0]  = 0x00
    CC1[1]  = 0x00
    CC1[2]  = 0x00
    CC1[3]  = 0x00
    CC1[4]  = 0x00
    CC1[5]  = 0x00
    CC1[6]  = 0x00
    CC1[7]  = 0x00
    CC1[8]  = 0x00
    CC1[9]  = 0x00
    CC1[10] = 0x00
    CC1[11] = 0x00
    CC1[12] = 0x00
    CC1[13] = 0x00
    CC1[14] = 0x00
    CC1[15] = 0x00

    CIV = bytearray(16)

    CIV[0]  = 0x00
    CIV[1]  = 0x00
    CIV[2]  = 0x00
    CIV[3]  = 0x00
    CIV[4]  = 0x00
    CIV[5]  = 0x00
    CIV[6]  = 0x00
    CIV[7]  = 0x00
    CIV[8]  = 0x00
    CIV[9]  = 0x00
    CIV[10] = 0x00
    CIV[11] = 0x00
    CIV[12] = 0x00
    CIV[13] = 0x00
    CIV[14] = 0x00
    CIV[15] = 0x00
    ###############################################################
    # In each iteration, we focus on one byte of CC1.  
    # We will try all 256 possible values, and send the constructed
    # ciphertext CC1 + C2 (plus the IV) to the oracle, and see 
    # which value makes the padding valid. 
    # As long as our construction is correct, there will be 
    # one valid value. This value helps us get one byte of D2. 
    # Repeating the method for 16 times, we get all the 16 bytes of D2.

    for K in range(1,17):
        for i in range(256):
            CC2[16 - K] = i
            status = oracle.decrypt(IV + C1 + CC2 + C3)
            if status == "Valid":
                #print("K = " + str(K))
                #print("Valid: i = 0x{:02x}".format(i))
                #print("CC2: " + CC2.hex())
                break
        P3 = xor(C2, D3)
        #print("P3:  " + P3.hex())
        D3[16 - K] = CC2[16 - K] ^ K
        #print("D3:  " + D3.hex())
        for j in range(1, K + 1):
            CC2[16 - j] = D3[16 - j] ^ (K + 1)
        #print("CC2_new: " + CC2.hex())
        #print("----------")
    P3 = xor(C2, D3)
    #print("P3:  " + P3.hex())
    #print("-----part1 finish-----")
    ###############################################################
    for K in range(1,17):
        for i in range(256):
            CC1[16 - K] = i
            status = oracle.decrypt(IV + CC1 + C2)
            if status == "Valid":
                #print("K = " + str(K))
                #print("Valid: i = 0x{:02x}".format(i))
                #print("CC1: " + CC1.hex())
                break
        P2 = xor(C1, D2)
        #print("P2:  " + P2.hex())
        D2[16 - K] = CC1[16 - K] ^ K
        #print("D2:  " + D2.hex())
        for j in range(1, K + 1):
            CC1[16 - j] = D2[16 - j] ^ (K + 1)
        #print("CC1_new: " + CC1.hex())
        #print("----------")
    P2 = xor(C1, D2)
    #print("P2:  " + P2.hex())
    #print("-----part2 finish-----")
    ###############################################################
    for K in range(1,17):
        for i in range(256):
            CIV[16 - K] = i
            status = oracle.decrypt(CIV + C1)
            if status == "Valid":
                #print("K = " + str(K))
                #print("Valid: i = 0x{:02x}".format(i))
                #print("IVC: " + CIV.hex())
                break
        P1 = xor(IV, D1)
        #print("P1:  " + P1.hex())
        D1[16 - K] = CIV[16 - K] ^ K
        #print("D1:  " + D1.hex())
        for j in range(1, K + 1):
            CIV[16 - j] = D1[16 - j] ^ (K + 1)
        #print("CIV_new: " + CIV.hex())
        #print("----------")
    P1 = xor(IV, D1)
    #print("P1:  " + P1.hex())
    #print("-----part3 finish-----") 
    print("----------")
    print("D1:  " + D1.hex())
    print("D2:  " + D2.hex())
    print("D3:  " + D3.hex()) 
    print("----------")
    print("P1:  " + P1.hex())  
    print("P2:  " + P2.hex())  
    print("P3:  " + P3.hex())
    
    
