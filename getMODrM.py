#from shutil import RegistryError
import sys

#from data_lst import binaryToHex


offset = ""
offset_flag = False
register32 = {
    "EAX":"000",
    "ECX":"001",
    "EDX":"010",
    "EBX":"011",
    "ESP":"100",
    "EBP":"101",
    "ESI":"110",
    "EDI":"111",
}
def getBinaryFromRegister(op1,op2):
    binary = "11"
    binary += register32[op2]
    binary += register32[op1]
    return binary

def setModByDigit(digit):
    return "01" if int(digit) <= 127 else "10"

def get32bitOffset(num):
    binary = format(num,'032b')
    dec1 = int(binary[24:28],2)
    dec2 = int(binary[28:32],2)
    dec3 = int(binary[16:20],2)
    dec4 = int(binary[20:24],2)
    dec5 = int(binary[8:12],2)
    dec6 = int(binary[12:16],2)
    dec7 = int(binary[0:4],2)
    dec8 = int(binary[4:8],2)
    hex1 = str(hex(dec1)).replace("0x","")
    hex2 = str(hex(dec2)).replace("0x","")
    hex3 = str(hex(dec3)).replace("0x","")
    hex4 = str(hex(dec4)).replace("0x","")
    hex5 = str(hex(dec5)).replace("0x","")
    hex6 = str(hex(dec6)).replace("0x","")
    hex7 = str(hex(dec7)).replace("0x","")
    hex8 = str(hex(dec8)).replace("0x","")
    return hex1+hex2+hex3+hex4+hex5+hex6+hex7+hex8


def get8bitOffset(num):
    binary = format(num,'08b')
    dec1 = int(binary[:4],2)
    dec2 = int(binary[4:8],2)
    hex1 = str(hex(dec1)).replace("0x","")
    hex2 = str(hex(dec2)).replace("0x","")
    return hex1+hex2

def getBinaryFromMemory(op1,op2):
    global offset_flag
    global offset
    if(not "[" in op2 and not "]" in op2):
        print(f"error {op2}")
        sys.exit(0)
    reg = ""
    binary = ""
    insideBracket = op2[op2.find("[")+1:op2.find("]")]
    if("+" in insideBracket):
        tokens = insideBracket.split("+")
        reg = tokens[0]
        binary = setModByDigit(tokens[1])
        if(int(tokens[1]) > 127):
            offset = get32bitOffset(int(tokens[1]))
        else:
            offset = get8bitOffset(int(tokens[1]))
    else:
        reg = insideBracket
        binary = "00"
    binary += register32[op1]
    binary += register32[reg]
    return binary

def getModVal(binary):
    global offset
    modVal = hex(int(binary[:4],2)).replace("0x","") + hex(int(binary[4:],2)).replace("0x","") + offset
    offset = ""
    return modVal

def generate(line):
    global register32
    tokens = line.split(",")
    for i in range(len(tokens)):
        tokens[i] = tokens[i].upper()
    if(not tokens[0] in register32):
        print(f"register not available {tokens[0]}")
        print(f"register not available {tokens}")
        sys.exit(0)
    binary = ""
    if(tokens[0] in register32 and tokens[1] in register32):
        binary = getBinaryFromRegister(tokens[0],tokens[1])
    elif("[" in tokens[1] and "]" in tokens[1]):
        binary = getBinaryFromMemory(tokens[0],tokens[1])
    #print(f"{tokens[0]} + {tokens[1]} = {getModVal(binary)}")
    return getModVal(binary)

#if __name__ == "__main__":
 #   with open(sys.argv[1],"r") as f:
  #      for line in f:
   #         generate(line.strip())
