from math import ceil
from prettytable import PrettyTable
import getMODrM
import sys

MODE = ""
ADDRESS = 0
new_ADDRESS = 0
declarative = ["extern","global"]
operations = ["add","sub","mov"]
register32 = ["eax","ecx","edx","ebx","esp","ebp","esi","edi"]
main_table = [
        ["89","01","29"],
        ["8B","03","2B"],
        ["B8","81","81"],
        ["C7","81","81"]
    ]
opcode_column = ["MOV","ADD","SUB"]
opcode_row = ["r32_r32","r32_m32","r32_imm32","m32_imm32"]

listing = []

class Row:
    def __init__(self,no,address,hexing,instruction):
	    self.no = no
	    self.address = address
	    self.hexing = hexing
	    self.instruction = instruction

def getOperand(tokens):
    flag = False
    for token in tokens:
        if "," in token:
            flag = True
            token = token.split(',')
    if flag == False:
        token = tokens[2]
    return token

def decimalBinaryToHex(num):
    return str(hex(num)).replace("x","")


def binaryToHex(ch):
    binary = ""
    binary = bin(ord(ch)).replace("b","")
    return binary

def appendPaddingForDD(res):
    i = 0
    while(i < (len(res)/2)%4):
        res += "00"
        i += 1
    return res

def appendPaddingForDW(res):
    i = 0
    while(i < (len(res)/2)%2):
        res += "00"
        i += 1
    return res

def getDWConversion(text):
    hexing = {
            "0000":"0",
            "0001":"1",
            "0010":"2",
            "0011":"3",
            "0100":"4",
            "0101":"5",
            "0110":"6",
            "0111":"7",
            "1000":"8",
            "1001":"9",
            "1010":"A",
            "1011":"B",
            "1100":"C",
            "1101":"D",
            "1110":"E",
            "1111":"F",
            }

    res = ""
    if "\"" in text:
        text = text.replace("\"","")
        for ch in text:
            binary = binaryToHex(ch)
            op1 = binary[0:4]
            op2 = binary[4:]
            res += hexing[op1]
            res += hexing[op2]
    else:
        text = int(text)
        if text > 255:
            print(f"error cannot store greater than 255")
        else:
            res += decimalBinaryToHex(text)
    res = appendPaddingForDW(res)
    return res

def getDDConversion(text):
    hexing = {
            "0000":"0",
            "0001":"1",
            "0010":"2",
            "0011":"3",
            "0100":"4",
            "0101":"5",
            "0110":"6",
            "0111":"7",
            "1000":"8",
            "1001":"9",
            "1010":"A",
            "1011":"B",
            "1100":"C",
            "1101":"D",
            "1110":"E",
            "1111":"F",
            }

    res = ""
    if "\"" in text:
        text = text.replace("\"","")
        for ch in text:
            binary = binaryToHex(ch)
            op1 = binary[0:4]
            op2 = binary[4:]
            res += hexing[op1]
            res += hexing[op2]
    else:
        text = int(text)
        if text > 255:
            print(f"error cannot store greater than 255")
        else:
            res += decimalBinaryToHex(text)
    res = appendPaddingForDD(res)
    return res


def getDBConversion(text):
    hexing = {
            "0000":"0",
            "0001":"1",
            "0010":"2",
            "0011":"3",
            "0100":"4",
            "0101":"5",
            "0110":"6",
            "0111":"7",
            "1000":"8",
            "1001":"9",
            "1010":"A",
            "1011":"B",
            "1100":"C",
            "1101":"D",
            "1110":"E",
            "1111":"F",
            }

    res = ""
    if "\"" in text:
        text = text.replace("\"","")
        for ch in text:
            binary = binaryToHex(ch)
            op1 = binary[0:4]
            op2 = binary[4:]
            res += hexing[op1]
            res += hexing[op2]
    else:
        text = int(text)
        if text > 255:
            print(f"error cannot store greater than 255")
        else:
            res += decimalBinaryToHex(text)
    return res

def dbConvert(tokens):
    token = getOperand(tokens)
    res = ""
    if isinstance(token,list):
        for t in token:
            res += getDBConversion(t)
    else:
        res += getDBConversion(t)
    return res

def dwConvert(tokens):
    token = getOperand(tokens)
    res = ""
    if isinstance(token,list):
        for t in token:
            res += getDWConversion(t)
    else:
        res += getDWConversion(token)
    return res

def ddConvert(tokens):
    token = getOperand(tokens)
    res = ""
    if isinstance(token,list):
        for t in token:
            res += getDDConversion(t)
    else:
        res += getDDConversion(token)
    return res

def convertData(tokens):
    if(tokens[1] == "db"):
        return dbConvert(tokens)
    if(tokens[1] == "dd"):
        return ddConvert(tokens)
    if(tokens[1] == "dw"):
        return dwConvert(tokens)

def convertBSS(tokens):
    global ADDRESS
    res = '<res '
    if(tokens[1] == "resb"):
        data = str(tokens[2])
    elif(tokens[1] == "resw"):
        data = str(2*int(tokens[2]))
    elif(tokens[1] == "resd"):
        data = str(4*int(tokens[2]))
    i = 0
    while(i < 8-len(data)):
        res += "0"
        i += 1
    res += data + ">"
    ADDRESS += int(data)
    return res

def getInstructedOpcode(tokens):
    global operations
    if(not tokens[0] in operations):
        pass

    return ""

def getInstructionName(inst):
    inst = inst.upper()
    if(inst in opcode_column):
        return inst
    return False

def get32bitHex(num):
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



def getOpcode(inst,op_type,tokens):
    if(not inst in opcode_column or not op_type in opcode_row):
        return ""
    col= opcode_column.index(inst)
    row = opcode_row.index(op_type)
    inst_op = main_table[row][col]
    x = ""
    y =""
    if(op_type == "r32_imm32"):
        x = int(inst_op,16)
        regs = tokens.split(",")
        reg = regs[0]
        n = register32.index(reg)
        x += n
        x = str(hex(x)).replace("0x","").upper()
        y = get32bitHex(int(regs[1]))
        return x+y
    return inst_op
        

def TypeOfOp(op):
    if("[" in op and "]" in op):
        return "mem"
    if(op in register32):
        return "reg"
    if(op.isnumeric()):
        if(int(op) > 127):
            return "imm32"
        else:
            return "imm8"
    return ""

def getOpType(OpType):
    if("," in OpType):
        tokens = OpType.split(",")
        op1 = tokens[0]
        op2 = tokens[1]
        res1 = TypeOfOp(op1)
        res2 = TypeOfOp(op2)
        if(res1 == "mem"):
                return "m32_imm32"
        elif(res1 == "reg"):
            if(res2 == "imm32" or res2 == "imm8"):
                return "r32_imm32"
            elif(res2 == "reg"):
                return "r32_r32"
            elif(res2 == "mem"):
                return "r32_m32"
        return ""

def convertText(tokens):
    global ADDRESS
    global register32
    ModValue = 0
    res = ""
    if(tokens[0] in declarative):
        return ""
    if(":" in tokens[0] and len(tokens) == 1):
        return ""
    if(tokens[0] in operations):
        if("," in tokens[1]):
             operands = tokens[1].split(",")
             if(not "]" in operands[1] and not operands[1] in register32):   
                #conversion time
                ModValue = getInstructedOpcode(tokens)
             else:
                 ModValue = getMODrM.generate(tokens[1])
        else:
            pass
    inst = getInstructionName(tokens[0])
    op_type = getOpType(tokens[1])
    res = getOpcode(inst,op_type,tokens[1]) 
    return res+str(ModValue)

def generate(line):
    global ADDRESS
    global new_ADDRESS
    global MODE
    global listing
    tokens = line.split(' ')
    if(";" in line):
        return
    if "section" in tokens:
        MODE = tokens[1]
        ADDRESS = 0
        new_ADDRESS = 0
        x = Row(len(listing)+1,"","",line)
        listing.append(x)
        return
    res = ""
    if(MODE == ".data" or MODE == ".rodata"):
        res = convertData(tokens)
        ADDRESS += len(res)//2
    elif(MODE == ".bss"):
        res = convertBSS(tokens)
    if(MODE == ".text"):
      res = convertText(tokens)
      ADDRESS += len(res)//2
    temp = str(hex(new_ADDRESS)).replace("0x","")
    temp = temp.zfill(8)
    x = Row(len(listing)+1,temp,res,line)
    listing.append(x)
    new_ADDRESS = ADDRESS

def printTable():
	global listing
	myTable = PrettyTable(['No','Address','Hexing','instruction'])
	for ele in listing:
		myTable.add_row([ele.no,ele.address,ele.hexing,ele.instruction])
	print(myTable)

def get_list_table(fileName):
    with open(fileName,"r") as f:
        for line in f:
            generate(line.strip())
        printTable()


if __name__ == "__main__":
    with open(sys.argv[1],"r") as f:
        for line in f:
            generate(line.strip())
        printTable()
