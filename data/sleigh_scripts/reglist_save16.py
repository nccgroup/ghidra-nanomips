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
    base_name = 'reglist_sv16'
    sv16_regs = ['fp', 'ra'] + REGS[16:30]

    for i in range(len(sv16_regs) - 1, -1, -1):
        name = f'{base_name}_{i:02}'
        next_name = f'{base_name}_{i+1:02}'
        reg = f'{sv16_regs[i]}'

        sp_write = f'*:$(REGSIZE) (sp - $(REGSIZE)*({i+1}-rt1_raw)) = {reg};'

        print(f'{name}: {reg}\t\t\tis count = {i+1} - rt1_raw & rt1_raw & {reg}\t{{{sp_write}}}')

        if i != len(sv16_regs) - 1:
            print(f'{name}: {reg},{next_name}\tis rt1_raw & {reg} & {next_name}\t{{{sp_write}}}')

    # empty register list case for count = 0
    print(f'{base_name}: \t\t\tis count = 0 {{}}')

    # entry points to first register (fp or ra)
    for i in range(1, -1, -1):
        next_name = f'{base_name}_{i:02}'
        print(f'{base_name}: ,{next_name}\tis rt1_raw = {i} & {next_name} {{}}')


if __name__ == '__main__':
    main()
