# 2 Pass Assembler for IA-32

Python program to generate Hex translation of assembly code.

## Description

This program generates the listing of the assembly program.
Same as:
  ```
  $ nasm -felf32 sample.asm -l p.lst
  ```

## Getting Started

### Dependencies

* Python 3
* PrettyTable module (Python)

### Executing program

* Make sure you have python,pip installed
* Install the prettyTable module via pip
```
pip install prettyTable
```
* Run the myAssembler script and pass assembly file as argument.

```
python3 myAssembler.py sample.asm
```

## Features
  1) MOD RM Byte
  2) MOV,ADD,SUB,XOR instructions
  3) register + 32bit / 8bit immediate data
  4) Backward jump reference
  5) Data, ro-data, bss section data declaration
  6) register + data section

## Help

Any advise for common problems or issues would be appreciated.

## Author

 [@LinkedIn](https://www.linkedin.com/in/tushar-adhatrao/)


## Guide
* Prof. Nitin Patil (PUCSD)

## Acknowledgments

* [IA32 Mannual](https://www.intel.in/content/www/in/en/architecture-and-technology/64-ia-32-architectures-software-developer-instruction-set-reference-manual-325383.html)

## Screenshots
* Sample assembly code
![Alt text](/screenshots/1.png)
* Symbol Table
![Alt text](/screenshots/2.png)
* Listing
![Alt text](/screenshots/3.png)
