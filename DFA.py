from collections import OrderedDict
import itertools


ciphertext_1 = [0x31, 0x79, 0x82, 0xfa, 0x56, 0x66, 0x67, 0x7f, 0x86, 0xb0, 0x21, 0xf3, 0x13, 0xe2, 0x17, 0x25]
faultyone = [0x77, 0xf3, 0xda, 0xc6, 0x17, 0x58, 0xcd, 0xb2, 0xcd, 0x9a, 0xb5, 0xd5, 0x32, 0xd4, 0xec, 0x8d]

ciphertext_2 = [0xee ,0xad ,0xe7 ,0x6a ,0xe8 ,0x53 ,0xcc ,0xec ,0xa4 ,0x5d ,0xdd ,0xfe ,0x25 ,0x7c ,0x63 ,0xc0]
faultytwo = [0x0c ,0x15 ,0x31 ,0xc0 ,0x70 ,0xf9 ,0x30 ,0x3e ,0xf2 ,0x3f ,0xca ,0x1f ,0x5b ,0xab ,0x10 ,0x07]

#Correct Ciphertext1: 0x317982fa5666677f86b021f313e21725
#Correct Ciphertext2: 0xeeade76ae853cceca45dddfe257c63c0
#Faulty Ciphertext1:  0x77f3dac61758cdb2cd9ab5d532d4ec8d
#Faulty Ciphertext2:  0x0c1531c070f9303ef23fca1f5bab1007

#Answer: 0xade208dd 380df400 7b37a576 e918ed66


Si = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
      0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
      0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
      0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
      0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
      0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
      0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
      0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
      0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
      0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
      0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
      0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
      0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
      0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
      0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
      0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]

xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)
d = {}
key = ''
finalkey = {}

def fxtime(tf,i):
    if(tf == 'f'):
        return i
    if(tf == '2f'):
        return xtime(i)
    if(tf == '3f'):
        return xtime(i)^i

def dfa(i1, i2, i3, i4, f1, f2, f3, f4):
    for i in range(256):
        for j in range(256):
            temp = []
            if(fxtime(f1, i) == (Si[ciphertext_1[i1] ^ j] ^ Si[faultyone[i1] ^ j])):
                key = str(i)+' '+str(j)
                temp.append([j])
                
                tempk7 = []
                for k in range(256):  #k
                    if(fxtime(f2, i) == (Si[ciphertext_1[i2] ^ k] ^ Si[faultyone[i2] ^ k])):
                        tempk7.append(k)
                temp.append(tempk7)
                
                tempk10 = []
                for l in range(256):
                    if(fxtime(f3, i) == (Si[ciphertext_1[i3] ^ l] ^ Si[faultyone[i3] ^ l])):
                        tempk10.append(l)
                temp.append(tempk10)
                
                tempk13 = []
                for m in range(256):
                    if(fxtime(f4, i) == (Si[ciphertext_1[i4] ^ m] ^ Si[faultyone[i4] ^ m])):
                        tempk13.append(m)
                temp.append(tempk13)
           
                d[key] = temp

    d2 = {}
    key2 = ''
    for i in range(256):
        for j in range(256):
            temp = []
            if(fxtime(f1, i) == (Si[ciphertext_2[i1] ^ j] ^ Si[faultytwo[i1] ^ j])):
                key2 = str(i)+' '+str(j)
                temp.append([j])
                
                tempk7 = []
                for k in range(256):  #k
                    if(fxtime(f2, i) == (Si[ciphertext_2[i2] ^ k] ^ Si[faultytwo[i2] ^ k])):
                        tempk7.append(k)
                temp.append(tempk7)
                
                tempk10 = []
                for l in range(256):
                    if(fxtime(f3, i) == (Si[ciphertext_2[i3] ^ l] ^ Si[faultytwo[i3] ^ l])):
                        tempk10.append(l)
                temp.append(tempk10)
                
                tempk13 = []
                for m in range(256):
                    if(fxtime(f4, i) == (Si[ciphertext_2[i4] ^ m] ^ Si[faultytwo[i4] ^ m])):
                        tempk13.append(m)
                temp.append(tempk13)
           
                d2[key2] = temp

    guess1 = []
    guess2 = []

    for i in d.values():
        flag = 0
        for j in i:
            if(len(j) == 0):
                flag = 1
        if(flag == 0):
            guess1.extend(list(itertools.product(*i)))

    print("\n------------\n")

    for i in d2.values():
        flag = 0
        for j in i:
            if(len(j) == 0):
                flag = 1
        if(flag == 0):
            guess2.extend(list(itertools.product(*i)))


    tkey = (list(set(guess1) & set(guess2)))
    if(tkey):
        tk = list(tkey[0])
        print(tk)
        finalkey[i1] = hex(tk[0]) 
        finalkey[i2] = hex(tk[1])
        finalkey[i3] = hex(tk[2])
        finalkey[i4] = hex(tk[3])
        for i in tk:
            print(hex(i))
            


tindices = [[0, 13,10,7], [4, 1, 14, 11], [8,5,2,15], [12,9,6,3]]
findices = [['2f', 'f', 'f','3f'], ['f', 'f','3f','2f'], ['f','3f','2f','f'], ['3f','2f', 'f', 'f']]

dfa(tindices[0][0], tindices[0][1], tindices[0][2], tindices[0][3], findices[0][0], findices[0][1], findices[0][2], findices[0][3])
dfa(tindices[1][0], tindices[1][1], tindices[1][2], tindices[1][3], findices[1][0], findices[1][1], findices[1][2], findices[1][3])
dfa(tindices[2][0], tindices[2][1], tindices[2][2], tindices[2][3], findices[2][0], findices[2][1], findices[2][2], findices[2][3])
dfa(tindices[3][0], tindices[3][1], tindices[3][2], tindices[3][3], findices[3][0], findices[3][1], findices[3][2], findices[3][3])

print("----final key---\n", OrderedDict(sorted(finalkey.items())))