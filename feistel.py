import hmac
import random
import hashlib

def gen_keylist(keylenbytes, numkeys, seed):
    keylist = []
    random.seed(seed)
    for i in range(numkeys):
        bytelist = b''.join([bytes([random.randint(0, 255)]) for x in range(keylenbytes)])
        keylist.append(bytelist)
    return keylist

def F(byteseq, k):
    h = hmac.new(k, byteseq, hashlib.sha1)
    return h.digest()[:8]

def xor(byteseq1, byteseq2):
    l1 = [b for b in byteseq1]
    l2 = [b for b in byteseq2]
    l1attachl2 = zip(l1,l2)

    l1xorl2 = [bytes([elem1^elem2]) for elem1,elem2 in l1attachl2]
    result = b''.join(l1xorl2)
    return result

def feistel_block(LE_inp, RE_inp, k):
    LE_out = RE_inp
    RE_out = xor(LE_inp, F(RE_inp, k))
    return LE_out, RE_out

def feistel_enc(plaintext, num_rounds, seed):
    keylist = gen_keylist(8, num_rounds, seed)
    ciphertext = ""
    plaintext += b'\x20' * (16-len(plaintext))
    L_block = plaintext[:8]
    R_block = plaintext[8:]

    for i in range(num_rounds):
        L_enc, R_enc = feistel_block(L_block, R_block, keylist[i])
        L_block = L_enc
        R_block = R_enc

    ciphertext = R_enc + L_enc
    return ciphertext

def feistel_dec(ciphertext, num_rounds,seed):
    keylist = gen_keylist(8, num_rounds, seed)[::-1]
    plaintext = ""
    L_block = ciphertext[:8]
    R_block = ciphertext[8:]

    for i in range(num_rounds):
        L_dec, R_dec = feistel_block(L_block, R_block, keylist[i])
        L_block = L_dec
        R_block = R_dec

    plaintext = R_dec + L_dec
    return plaintext

if __name__ == '__main__':
    num_rounds = 16
    seed = 50
    plaintext = b'isthis16bytes?'
    ciphertext = feistel_enc(plaintext, num_rounds, seed)
    print(ciphertext)
    decypted = feistel_dec(ciphertext, num_rounds, seed)
    print(decypted)