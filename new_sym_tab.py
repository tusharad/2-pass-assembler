import sys
from prettytable import PrettyTable

class Row:
	def __init__(self,no,name,address,value,section,symbol_type):
		self.no = no
		self.name = name
		self.address = address
		self.value = value
		self.section = section
		self.symbol_type = symbol_type

cnt = 0
sections = ['.bss','.data','.rodata','.text']
data_types = ['db','dw','dd','dt']
bss_types = ['resb','resw','resd']
bss_vals = {'resb':1,'resw':2,'resd':4}
current_section = None
prev_address = "00000000"
new_address = 0
sym_table = []
valid_undefined = ['global','extern']
undefined_vals = {'global':'T','extern':'U'}

def setSection(line):
    global sections
    global new_address
    global prev_address
    global current_section
    tokens = line.split(" ")
    if(tokens[1] in sections):
        current_section = tokens[1]
        new_address = 0
        prev_address = 0
    return


def appendZero(num,data_type):
    if(data_type == "dd"):
        while(num%4 != 0):
            num += 1
    elif(data_type == "dw"):
        while(num%2 != 0):
            num += 1
    return num

def calculateAddress(value,data_type):
    global new_address
    global prev_address
    values = []
    addr = ""
    num = 0
    if("," in value):
        values = value.split(",")
        for ele in values:
            if("\"" in ele):
                 ele = ele.replace("\"","")
                 num += len(ele)
                 num = appendZero(num,data_type)
            elif(ele.isnumeric()):
                num += 1
                num = appendZero(num,data_type)
    else:
        if("\"" in value):
            value = value.replace("\"","")
            num += len(value)
            num = appendZero(num,data_type)
        elif(value.isnumeric()):
                num += 1
                num = appendZero(num,data_type)
    return num

def getDataSymbols(line):
    tokens = line.split(" ")
    global new_address
    global sym_table
    global current_section
    global prev_address
    num = 0
    try:
        variable_name = tokens[0]
        data_type = tokens[1]
        value = tokens[2]
        num = calculateAddress(value,data_type)
        new_address += num
        temp = str(hex(new_address)).replace("0x","")
        temp = temp.zfill(8)
        temp = str(hex(prev_address)).replace("0x","")
        temp = temp.zfill(8)
        x = Row(len(sym_table)+1,variable_name,temp,value,current_section,"D" if current_section == ".data" else "r")
        sym_table.append(x)
        prev_address = new_address
        return temp
    except:
        print(f"error occured {line}")

def getBSSsymbols(line):
    tokens = line.split(" ")
    global new_address
    global sym_table
    global current_section
    global prev_address
    num = 0
    try:
        variable_name = tokens[0]
        data_type = tokens[1]
        value = tokens[2]
        if(data_type == "resb"):
            num = int(value)
        elif(data_type == "resw"):
            num= int(value)*2
        elif(data_type == "resd"):
            num = int(value)*4
        new_address += num
        temp = str(hex(new_address)).replace("0x","")
        temp = temp.zfill(8)
        temp = str(hex(prev_address)).replace("0x","")
        temp = temp.zfill(8)
        x = Row(len(sym_table)+1,variable_name,temp,"None",current_section,"b")
        sym_table.append(x)
        prev_address = new_address
        return temp
    except:
        print(f"error occured {line}")

def getTextSymbols(line):
    global new_address
    global sym_table
    global current_section
    global prev_address
    
    tokens = line.split(" ")
    if(len(tokens) == 2 and ("global" in tokens or "extern" in tokens)):
        symbol = tokens[1]
        x = Row(len(sym_table)+1,symbol,"None","None",current_section,"U")
        sym_table.append(x)
        prev_address = new_address
        return
    if(len(tokens) == 1 and ":" in tokens[0]):
        label = tokens[0][:-1]
        x = Row(len(sym_table)+1,label,"None","None",current_section,"t")
        sym_table.append(x)
        prev_address = new_address
        return
    return

def generate(line):
    global current_section
    global new_address
    global prev_address
    if("section" in line):
        setSection(line)
        return
    res = ""
    if(current_section == ".data" or current_section == ".rodata"):
        res = getDataSymbols(line)
    elif(current_section == ".bss"):
        res = getBSSsymbols(line)
    elif(current_section == ".text"):
        res = getTextSymbols(line)
    return res

def printTable():
	global sym_table
	myTable = PrettyTable(['No','Name','Address','Value','Section','Symbol Type'])
	for ele in sym_table:
		myTable.add_row([ele.no,ele.name,ele.address,ele.value,ele.section,ele.symbol_type])
	print(myTable)
	return sym_table

def get_symbol_table(fileName):
    with open(fileName,"r") as f:
        for line in f:
            generate(line.strip())
    return printTable()

if __name__ == "__main__":
    with open(sys.argv[1],"r") as f:
        for line in f:
            generate(line.strip())
        printTable()
