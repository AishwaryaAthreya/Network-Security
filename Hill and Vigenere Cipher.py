

# Inverse of a number in mod(26) arithmatic:
# in regular arithmetic, inverse of a number is another number so that the product of the two is 1
# inv(2) = 1/2,   inv(4) = 1/4
# In mod(26) arithmetic,all numbers are in the space of 0-25 so the inverse should reside in the same space
# and the product operation is defined as the product in mod(26) sense example:  2 * 15 = 30mod(26) = 4
# for example the inverse of 3 is a number n in range 0:25 such that 3*n mod(26)=1
# But not all of numbers in the 0:25 range have inverses. For example 2 doesn't have any inverse in mod(26) arithmetic.
# Practice: find the mod(26) inverses of the numbers 0:25
# for example to find the mod(26) inverse for 5, we need to search in numbers 0:25 and see which one satisifes 5*n mod(26)=1
# Mod26invTable = {}
# for m in range(26):
#   for minv in range(26):
#     if (m*minv)%26==1:
#       Mod26invTable[m] = minv
#       print(m, minv)

# Mod26invTable[17]

# Matrix multiplication and inverses in Mod26 world
# Notation:
# M: original matrix with elements in the rnage of 0:25   (3x3 matrix)
#
# Minv: real inverse of M in regular arithmetic i.e., M*Minv = I
# Mdet: Determinant of matrix M  i.e., a real number 
# Madj: real adjoint matrix of M (3x3 matrix with real number values)
#
# Minv26: inverse of M in the mod(26) arithmetic (elements of Minv26 are all in range of 0:25) i.e,  M*Minv26 mod(26) = I
# Mdet26: Determinant of M in mod(26) arithmetic (a number between 0:25)
# Mdet26inv: inverse of Mdet26 in mod(26) arithemtic
# Madj26: mod(26) adjoint matrix of M (3x3 matrix with values in range 0:25)

# For real matrices, if we want to find Minv, it is:
# Minv = (1/Mdet)* Madj  (1)

# For mod-26 matrices:
# Minv26 = (Mdet26inv * Madj26)%26  (2)

# For Hill cipher, M is given (3x3 matrix with elements in 0:25) but we need to find Minv26 (3x3 matrix with elements in 0:25)
# The numpy module in Python can be used for calculation of Minv and Minv26

import numpy as np
from pprint import pprint

# M = np.array([[17,17,5],[21,18,21],[2,2,19]])
# print("M:")
# print(M)

# Minv = np.linalg.inv(M)
# Mdet = np.linalg.det(M)
# print(Minv)
# print(Mdet)

# np.matrix.round(np.matmul(M, Minv))

# Madj = Mdet*Minv
# Madj26 = Madj%26

def matrixmodinv(M):
  Minv = np.linalg.inv(M)
  Mdet = np.linalg.det(M)

  Mod26invTable = {}
  for m in range(26):
    for minv in range(26):
      if (m*minv)%26==1:
        Mod26invTable[m] = minv
        #print(m, minv)

  
  Mdet26 = Mdet%26

  if Mdet26 in Mod26invTable:
    Mdet26inv = Mod26invTable[Mdet26]
  else:
    Mdet26inv = -1
    print('Non-inversible')
    exit()

  Madj = Mdet*Minv
  Madj26 = Madj%26

  Minv26=(Mdet26inv*Madj26)%26
  Minv26 = np.matrix.round(Minv26,0)%26

  return Minv26



#np.matrix.round(np.matmul(M,Minv26))%26

# How to work with text strings to break them into substrings or merge substrings
def convert(S):
    
  # I can convert it to uppercase by the upper() function
  S_upper = S.upper()
  #print(S_upper)
  # I can remove spaces by using the generic replace() function that allows me to replace any character with any other character
  S_upper = S_upper.replace(' ','')
  #print(S_upper_nospace)
  # I can extract certain section of a string same as lists
  # S_0 = S_upper_nospace[0:3]
  # S_1 = S_upper_nospace[3:6]
  # S_2 = S_upper_nospace[6:9]
  # S_3 = S_upper_nospace[9:12]
  # S_4 = S_upper_nospace[12:15]
  # print(S_0,S_1,S_2,S_3,S_4)

  # # How can I attachmultiple strings together?
  # # use the + sign
  # S_recover = S_0+S_1+S_2+S_3+S_4
  # print(S_recover)

  if len(S_upper) % 3 != 0:
    S_upper += 'X'*(3 - (len(S_upper)%3))

  return S_upper

def hill_enc(key,test_string):
  cipher=''

  temp_list = []
  test_string = convert(test_string)
  #print(test_string)
  PT_list = [ord(p)-65 for p in test_string]

  M=np.array(key)

  for i in range(0, len(test_string), 3):
    pt_sublist = np.array(PT_list[i:i+3])
    sub_enc= np.matrix.round(np.matmul(pt_sublist,M)%26,0)%26
    sub_enc=sub_enc.tolist()

    temp_list.extend(sub_enc)

  cipher=cipher.join(chr(p+65) for p in temp_list)

  return cipher

#hill_enc([[17,17,5],[21,18,21],[2,2,19]], 'Test String')

def hill_dec(key,test_string):
  plaintext= '' 
  temp_plain=[]
  cipher_list = [ord(c) - 65 for c in test_string]
  M=np.array(key)
  M_inverse = matrixmodinv(M)

  for i in range(0, len(test_string), 3):
    sub_cipherlist = np.array(cipher_list[i:i+3])

    sub_cipherlist_dec= np.matrix.round(np.matmul(sub_cipherlist,M_inverse)%26,0)%26

    sub_cipherlist_dec = sub_cipherlist_dec.tolist()

    temp_plain.extend(sub_cipherlist_dec)

  plaintext = plaintext.join(chr(int(c)+65) for c in temp_plain)

  return plaintext

# hill_dec([[17,17,5],[21,18,21],[2,2,19]],'BPBLJCPRGHQO')

def char_enc(ch,key_v):
  value = ord(ch)
  key = ord(key_v) - 65
  encryption_ch = chr((value + key - 65)%26 + 65)
  return encryption_ch

def char_dec(ch,key_v):
  value = ord(ch)
  key = ord(key_v) - 65
  decryption_ch = chr((value - key - 65)%26 + 65)
  return decryption_ch

def vigenere_enc(key, PT):
  cipher = '' 
  PT=PT.upper()
  PT=PT.replace(' ', '')
  for i in range(0,len(PT)):
    cipher += char_enc(PT[i],key[i%len(key)])
   # print(cipher)

  return cipher

# vigenere_enc('KEY', 'Test String')

def vigenere_dec(key,CT):
  plain = '' 
  for i in range(0,len(CT)):
    plain += char_dec(CT[i], key[i%len(key)])
  
  return plain

#print(vigenere_dec('KEY','DIQDWRBMLQ'))



