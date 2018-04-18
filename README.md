# Assembler
Assembler built to be used for FPGA microprocessor.  

Lots of work left to do

Currently able to assemble an asm file(for custom microprocessor) if it has less than 255 bytes of code.

Need to implement ASCII support as well as areas to declare bytes, words, etc.

Labels currently can only be used within brackets so that needs to be fixed as well.

### To use
Write code in asmtest.asm 
Keep asmtest.asm, tests19.s19, and assembler.py in the same directory
Run assembler.py and it will generate the corresponding code for tests19.s19

#### Quick Note
This is to be used in conjunction with RomTools(coming soon), which will allow for the code to be translated into a LUT for VHDL and the custom microprocessor can run from that.
