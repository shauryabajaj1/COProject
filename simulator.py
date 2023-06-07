binaryopcode = {'add': '00000', 'sub': '00001', 'mov1': '00010', 'mov2': '00011', 'ld': '00100', 'st': '00101', 'mul': '00110', 'div': '00111', 'rs': '01000', 'ls': '01001', 'xor': '01010', 'or': '01011', 'and': '01100', 'not': '01101', 'cmp': '01110',
           'jmp': '01111', 'jlt': '11100', 'jgt': '11101', 'je': '11111', 'hlt': '11010', 'mov': '0'}

instructiontype = {'add': '3reg', 'sub': '3reg', 'mov1': 'regimm', 'mov2': '2reg', 'ld': 'regmem', 'st': 'regmem', 'mul': '3reg', 'div': '2reg',
                'rs': 'regimm', 'ls': 'regimm', 'xor': '3reg', 'or': '3reg', 'and': '3reg', 'not': '2reg', 'cmp': '2reg',
                'jmp': 'memaddr', 'jlt': 'memaddr', 'jgt': 'memaddr', 'je': 'memaddr', 'hlt': 'end', 'mov': '2reg'}

extrabits = {'3reg': '00', 'regimm': '0', '2reg':'00000', 'regmem': '0', 'memaddress': '0000', 'end': '00000000000'}

regs = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6':'110', 'FLAGS': '111'}

registervalues = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0, 'FLAGS': 0}

regkeyslist = list(registervalues.keys())

regvalueslist = list(registervalues.values())

registers = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6']

binarystring = ''

binarycode = []

pc = 0

def binarytodecimal(binary):
    value = list(binary)
    a = 0
    for i in range(len(value)):
            digit = value.pop()
            if digit == '1':
                a += pow(2, i)
    return a

def getkey(val):
    for key, value in regs.items():
        if val == value:
            return key

def dump():
    for i in binarycode:
        print(i)

def writeregvalues():
    print(format(pc, '07b'), end = '        ')
    for i in range(len(regvalueslist)):
        if i != len(regvalueslist) - 1:
            print(format(regvalueslist[i], '016b'), end = ' ')
        else:
            print(format(regvalueslist[i], '016b'))

'''with open('stdin.txt') as f:
    content = f.readlines()

for line in content:
    if not line:
        break
    else:
        line = line.strip()
        binarycode.append(line)'''

while True:
    try:
        line = input()
        line = line.strip()
        binarystring = binarystring + line + '\n'
    except EOFError:
       break

binarycode = binarystring.split('\n')

for i in range(len(binarycode), 128):
    binarycode.append('0' * 16)

while True:
    if binarycode[pc] == '1101000000000000':
        registervalues['FLAGS'] = 0
        writeregvalues()
        break
    binaryline = binarycode[pc]
    if binaryline[:5] == '00000':
        reg1 = getkey(binaryline[7:10])
        reg2 = getkey(binaryline[10:13])
        reg3 = getkey(binaryline[13:])
        registervalues[reg1] = registervalues[reg2] + registervalues[reg3]
        if registervalues[reg1] > 65535:
            registervalues[reg1] = 0
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc += 1
            continue
        else:
            registervalues[reg1] = 0
            writeregvalues()
            pc += 1
            continue
    elif binaryline[:5] == '00001':
        reg1 = getkey(binaryline[7:10])
        reg2 = getkey(binaryline[10:13])
        reg3 = getkey(binaryline[13:])
        registervalues[reg1] = registervalues[reg2] - registervalues[reg3]
        if registervalues[reg1] < 0:
            registervalues[reg1] = 0
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc += 1
            continue
        else:
            writeregvalues()
            pc += 1
            continue
    elif binaryline[:5] == '00010':
        reg1 = getkey(binaryline[6:9])
        a = 0
        num = list(binaryline[10:])
        for i in range(len(num)):
            digit = num.pop()
            if digit == '1':
                a += pow(2, i)
        registervalues[reg1] = a
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '00011':
        reg1 = getkey(binaryline[10:13])
        reg2 = getkey(binaryline[13:])
        registervalues[reg1] = registervalues[reg2]
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '00110':
        reg1 = getkey[binaryline[7:10]]
        reg2 = getkey[binaryline[10:13]]
        reg3 = getkey[binaryline[13:]]
        registervalues[reg1] = registervalues[reg2] * registervalues[reg3]
        if registervalues[reg1] > 65535:
            registervalues[reg1] = 0
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc += 1
            continue
        else:
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc += 1
            continue
    elif binaryline[:5] == '00111':
        reg1 = getkey[binaryline[10:13]]
        reg2 = getkey[binaryline[13:]]
        if registervalues[reg2] == 0:
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc += 1
            continue
        else:
            registervalues['R0'] = registervalues[reg1] // registervalues[reg2]
            registervalues['R1'] = registervalues[reg1] % registervalues[reg2]
            writeregvalues()
            pc += 1
            continue
    elif binaryline[:5] == '01000': #check if working properly later
        reg1 = getkey(binaryline[6:9])
        immvalue = binarytodecimal(binaryline[9:])
        shiftedval = '0' * immvalue + format(int(bin(registervalues[reg1])[2:], 2), '016b')
        registervalues[reg1] = shiftedval
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '01001':
        reg1 = getkey(binaryline[6:9])
        immvalue = binarytodecimal(binaryline[9:])
        shiftedval = registervalues[reg1] << immvalue
        registervalues[reg1] = shiftedval
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '01010':
        reg1 = getkey(binaryline[7:10])
        reg2 = getkey(binaryline[10:13])
        reg3 = getkey(binaryline[13:])
        registervalues[reg1] = registervalues[reg2] ^ registervalues[reg3]
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '00100':
        reg1 = getkey(binaryline[6:9])
        registervalues[reg1] = int(binarycode[[int(binaryline[9:], 2)]], 2)
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '00101':
        reg1 = getkey(binaryline[6:9])
        binarycode[int(binaryline[9:], 2)] = format(registervalues[reg1], '016b')
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '01011':
        reg1 = getkey(binaryline[7:10])
        reg2 = getkey(binaryline[10:13])
        reg3 = getkey(binaryline[13:])
        registervalues[reg1] = registervalues[reg2] | registervalues[reg3]
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '01100':
        reg1 = getkey(binaryline[7:10])
        reg2 = getkey(binaryline[10:13])
        reg3 = getkey(binaryline[13:])
        registervalues[reg1] = registervalues[reg2] & registervalues[reg3]
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '01101':
        reg1 = getkey(binaryline[10:13])
        reg2 = getkey(binaryline[13:])
        registervalues[reg2] = 65535 - registervalues[reg1]
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '01110':
        reg1 = getkey(binaryline[10:13])
        reg2 = getkey(binaryline[13:])
        if registervalues[reg1] < registervalues[reg2]:
            registervalues['FLAGS'] = 4
        elif registervalues[reg1] == registervalues[reg2]:
            registervalues['FLAGS'] = 1
        else:
            registervalues['FLAGS'] = 2
        writeregvalues()
        pc += 1
        continue
    elif binaryline[:5] == '01111':
        memaddr = binaryline[9:]
        registervalues['FLAGS'] = 0
        writeregvalues()
        pc = int(memaddr, 2)
        continue
    elif binaryline[:5] == '11100':
        if registervalues['FLAGS'] == 4:
            memaddr = binaryline[9:]
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc = int(memaddr, 2)
            continue
        else:
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc += 1
            continue
    elif binaryline[:5] == '11101':
        if registervalues['FLAGS'] == 2:
            memaddr = binaryline[9:]
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc = int(memaddr, 2)
            continue
        else:
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc += 1
            continue
    elif binaryline[:5] == '11111':
        if registervalues['FLAGS'] == 1:
            memaddr = binaryline[9:]
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc = int(memaddr, 2)
            continue
        else:
            registervalues['FLAGS'] = 0
            writeregvalues()
            pc += 1
            continue

dump()









        



#while True:
 #   try:
  #      line = input()
   #     line = line.strip()
    #    binarystring = binarystring + line + '\n'
    #except EOFError:
     #   break

#data = binarystring.split('\n')