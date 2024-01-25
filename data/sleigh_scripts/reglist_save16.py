#!/usr/bin/env python3

REGS = """zero
	at
	t4 t5
	a0 a1 a2 a3
	a4 a5 a6 a7
	t0 t1 t2 t3
	s0 s1 s2 s3
	s4 s5 s6 s7
	t8 t9
	k0 k1
	gp sp fp ra""".split()


def main():
    sv16_regs = ['fp', 'ra'] + REGS[16:30]
    #print(sv16_regs)
    #print(len(sv16_regs))

    for i in range(15, -1, -1):
        name = f'reglist_sv16_{i:02}'
        next_name = f'reglist_sv16_{i+1:02}'
        reg = f'{sv16_regs[i]}'

        if i == 0:
            print(f'{name}:\t\t\t\tis count = 0 {{}}')
            # skip for rt=1
            print(f'{name}:\t, {next_name}\tis rt1 = 1 & {next_name} {{}}')
            print(f'{name}:\t, fp\t\t\tis rt1 = 0 & count = 1 & fp {{}}')
            print(f'{name}:\t, fp,{next_name}\tis rt1 = 0 & fp & {next_name} {{}}')
            continue

        print(f'{name}:\t{reg}\t\t\tis count = {i+1} - rt1 & {reg} {{}}')

        if i != 15:
            print(f'{name}:\t{reg},{next_name}\tis {reg} & {next_name} {{}}')


if __name__ == '__main__':
    main()
