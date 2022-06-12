# 2 Pass assembler for 32-bit ISA
# Name: Tushar Suresh Adhatrao
# Roll: 21111049
# Class: MSc B21

import sys
import new_sym_tab
import data_lst

def Error_table(error_name = ""):
    error_table = {
        "no_file": "Please give asm file as argument"
    }
    return error_table[error_name]

def readFile(fileName):
    data_lst.get_list_table(fileName)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(Error_table("no_file"))
        sys.exit(0)
    readFile(sys.argv[1])
