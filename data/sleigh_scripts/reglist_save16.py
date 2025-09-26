#!/usr/bin/env python3
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument('--restore', action='store_true', default=False)
    args = parser.parse_args()

    if args.restore:
        base_name = 'reglist_rs16'
    else:
        base_name = 'reglist_sv16'

    sv16_regs = ['fp', 'ra'] + REGS[16:30]

    for i in range(len(sv16_regs) - 1, -1, -1):
        name = f'{base_name}_{i:02}'
        next_name = f'{base_name}_{i+1:02}'
        reg = f'{sv16_regs[i]}'

        if not args.restore:
            # SAVE
            sp_write = f'*:$(REGSIZE) (sp - $(REGSIZE)*({i+1}-rt1_raw)) = {reg};'
        else:
            # RESTORE
            sp_write = f'{reg} = *:$(REGSIZE) (load_multiple_base + hi_uoffset8_sl4 - $(REGSIZE)*({i+1}-rt1_raw));'

        offs_pattern = ' & hi_uoffset8_sl4' if args.restore else ''

        print(f'{name}: {reg}\t\t\tis count = {i+1} - rt1_raw & rt1_raw & {reg}{offs_pattern}\t{{{sp_write}}}')

        if i != len(sv16_regs) - 1:
            print(f'{name}: {reg},{next_name}\tis rt1_raw & {reg} & {next_name}{offs_pattern}\t{{{sp_write}}}')

    # empty register list case for count = 0
    print(f'{base_name}: \t\t\tis count = 0 {{}}')

    # entry points to first register (fp or ra)
    for i in range(1, -1, -1):
        next_name = f'{base_name}_{i:02}'
        print(f'{base_name}: ,{next_name}\tis rt1_raw = {i} & {next_name} {{}}')


if __name__ == '__main__':
    main()
