
import sys

def caesar_str_enc(plaintext, k):               
  ciphertext= ""
  for c in plaintext:
    if c.isupper():
      uni_c = ord(c)
      ind_c = uni_c - ord("A")
      ind_enc_c = (ind_c + k) %26
      new_c = ind_enc_c + 65
      enc_c = chr (new_c)
      ciphertext = ciphertext + enc_c
      #print (ciphertext)
    else:
      ciphertext += c
  return ciphertext                             

def caesar_str_dec(ciphertext, k):                
  plaintext = ""
  for c in ciphertext:
    if c.isupper():
      ind_c = ord(c)-65
      ind_dec_c = (ind_c - k ) %26
      dec_c = chr(ind_dec_c + 65)
      plaintext = plaintext + dec_c
    else:
      plaintext += c
    #print (plaintext)
  return plaintext                              
if __name__ == "__main__":                        
    input_str = 'TEST STRING'            
    k = int(input("Enter K value: ")) #taking user input for shift value
    enc_st = caesar_str_enc (input_str, k)
    print(enc_st)
    dec_st = caesar_str_dec (enc_st, k)
    print(dec_st)
    #test_function()                               
 
# def test_function():                           
    
#     return None