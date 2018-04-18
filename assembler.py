# Brice Vadnais Capstone II ECE 493

# Assembler for Custom Microprocessor Architechture

# One thing to note is all labels need to go in brackets
# Still cant do immediate with labels so that needs to get fixed

# THIS WILL BREAK ONCE THERE ARE TOO MANY INSTRUCTIONS

# 16 bits of memory space
mem = [0] * (2 ** 16)

# pc initialized to 0x0000
pc = 0x0000

# Encoding Table or ent
ent = {'nop': '0x00',
       'add': '0x01',
       'sub': '0x02',
       'inca': '0x03',
       'incb': '0x04',
       'deca': '0x05',
       'decb': '0x06',
       'inva': '0x07',
       'invb': '0x08',
       'cmp': '0x09',
       'hlt': '0xFF',
       'lda': {'imm': '0x10', 'dir': '0x20', 'indx': '0x40'},
       'ldb': {'imm': '0x11', 'dir': '0x21', 'indx': '0x41'},
       'adda': {'imm': '0x12', 'dir': '0x22', 'indx': '0x44'},
       'addb': {'imm': '0x13', 'dir': '0x23', 'indx': '0x45'},
       'suba': {'imm': '0x14', 'dir': '0x24', 'indx': '0x46'},
       'subb': {'imm': '0x15', 'dir': '0x25', 'indx': '0x47'},
       'ldx': {'imm': '0x16'},
       'lds': {'imm': '0x17'},
       # Direct encoding may change in future for this
       'anda': {'imm': '0x18', 'dir': '0x2A', 'indx': '0x48'},
       # Direct encoding may change in future for this
       'andb': {'imm': '0x19', 'dir': '0x2B', 'indx': '0x49'},
       # Direct encoding may change in future for this
       'ora': {'imm': '0x1A', 'dir': '0x2C', 'indx': '0x4A'},
       # Direct encoding may change in future for this
       'orb': {'imm': '0x1B', 'dir': '0x2D', 'indx': '0x4B'},
       'sta': {'imm': '0x26', 'dir': '0x26', 'indx': '0x42'},
       'stb': {'imm': '0x27', 'dir': '0x27', 'indx': '0x43'},
       'psha': '0x30',
       'pshb': '0x31',
       'popa': '0x32',
       'popb': '0x33',
       'psh': {'imm': '0x34', 'dir': '0x35', 'indx': '0x36'},
       'incx': '0x4C',
       'decx': '0x4D',
       'jmp': {'dir': '0x50'},
       'jsr': {'dir': '0x51'},
       'rfs': {'dir': '0x52'},
       'jeq': {'dir': '0x53'},
       'jneq': {'dir': '0x54'},
       'jgt': {'dir': '0x55'},
       'jlt': {'dir': '0x56'},
       'jgte': {'dir': '0x57'},
       'jlte': {'dir': '0x58'}
       }


# preparing the asm file
asm_file = open('asmtest.asm', 'r')
memory = []
for lines in asm_file:
    if lines.startswith("#") or lines.startswith("\n"):
        continue
    asm_code = lines.split()
    for op in asm_code:
        memory.append(op)

print("This is the memory: %s" % (memory))


final_encoded_mem = ""
temp_mem = []

if memory[0] == 'ORG:':
    temp_mem = list(memory)
    final_encoded_mem = final_encoded_mem + format(int(temp_mem[1], 16), '04X')
    psa_val = int(temp_mem[1], 16)
    memory.remove(memory[0])
    memory.remove(memory[0])
    # print(temp_mem)
for x in range(psa_val):
    memory.insert(x, '0')

# This line will print with all empty 0s
# print("This is the memory after ORG: %s" % (memory))

labels = []

len_memory = len(memory)
# print(len(memory))
i_items = 0
while i_items < len_memory:
    if memory[i_items].endswith(":"):
        labels.append(memory[i_items])
        labels.append(i_items)
        memory.remove(memory[i_items])
        len_memory = len_memory - 1
    i_items += 1
# print(labels)
newlabels = []
for stuff in labels:
    if isinstance(stuff, int):
        newlabels.append(stuff)
    else:
        newlabels.append(stuff[:-1])

label_dict = dict(newlabels[i:i + 2] for i in range(0, len(newlabels), 2))


# for items in memory:
# fix the address for jumps/ labels, currently counting org as part of the count
for i in range(len(memory)):
    if memory[i] in ent:
        mem[i] = {}
        mem[i]['opc'] = ent[memory[i]]
        if not isinstance(mem[i]['opc'], dict):
            final_encoded_mem = final_encoded_mem + format(int(mem[i]['opc'], 16), '02X')
        if memory[i] == 'hlt':
            mem[i]['opr'] = pc
            final_encoded_mem = final_encoded_mem + format(mem[i]['opr'], '04X')

    elif memory[i].startswith('0x'):
        if mem[i - 1]['opc']['imm'] == '0x16' or mem[i - 1]['opc']['imm'] == '0x17' \
                or mem[i - 1]['opc']['imm'] == '0x26' or mem[i - 1]['opc']['imm'] == '0x27':
            mem[i - 1].update({'opc': mem[i - 1]['opc']['imm'], 'opr': int(memory[i], 16)})
            final_encoded_mem = final_encoded_mem + format(int(mem[i - 1]['opc'], 16), '02X')
            final_encoded_mem = final_encoded_mem + format(mem[i - 1]['opr'], '04X')
        else:
            mem[i - 1].update({'opc': mem[i - 1]['opc']['imm'], 'opr': int(memory[i], 16)})
            final_encoded_mem = final_encoded_mem + format(int(mem[i - 1]['opc'], 16), '02X')
            final_encoded_mem = final_encoded_mem + format(mem[i - 1]['opr'], '02X')

    elif memory[i].startswith('['):
        memory[i] = memory[i].strip('[]')
        if memory[i].startswith('X') or memory[i].startswith('x'):
            tmpindx = memory[i].split('+')
            mem[i - 1].update({'opc': mem[i - 1]['opc']['indx'], 'opr': tmpindx[1]})
            final_encoded_mem = final_encoded_mem + format(int(mem[i - 1]['opc'], 16), '02X')
            final_encoded_mem = final_encoded_mem + format(int(mem[i - 1]['opr'], 16), '02X')
        elif memory[i].startswith('0x'):
            mem[i - 1].update({'opc': mem[i - 1]['opc']['dir'], 'opr': int(memory[i], 16)})
            final_encoded_mem = final_encoded_mem + format(int(mem[i - 1]['opc'], 16), '02X')
            final_encoded_mem = final_encoded_mem + format(int(mem[i - 1]['opr'], 16), '04X')
        elif isinstance(memory[i], str):
            mem[i - 1].update({'opc': mem[i - 1]['opc']['dir'], 'opr': label_dict[memory[i]]})
            final_encoded_mem = final_encoded_mem + format(int(mem[i - 1]['opc'], 16), '02X')
            final_encoded_mem = final_encoded_mem + format(mem[i - 1]['opr'], '04X')
        else:
            continue
    else:
        continue

n = 2

new_enc_mem = [int(final_encoded_mem[i:i + n], 16) for i in range(0, len(final_encoded_mem), n)]

# print(new_enc_mem)
new_enc_mem.insert(0, len(new_enc_mem) + 1)
# print(new_enc_mem)
tot = 0
for opc_opr in new_enc_mem:
    tot += opc_opr
checksum_val = format(int(hex(0xFFFFFF - int(hex(tot), 16)), 16), '02X')
# print(checksum_val)
new_enc_mem.append(int(checksum_val[-2:], 16))
# print(new_enc_mem)

s19file = open('tests19.s19', 'w')

with s19file:
    s19file.write('S1')
    for i in new_enc_mem:
        s19file.write(format(i, '02X'))
    s19file.write('\n')
    s19file.write('S105FFFEFC0001')
