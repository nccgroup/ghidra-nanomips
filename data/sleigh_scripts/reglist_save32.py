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
        base_name = 'reglist_rs32'
    else:
        base_name = 'reglist_sv32'

    sv32_regs = REGS + REGS[16:30]
    #print(sv32_regs)
    #print(len(sv32_regs))

    for i in range(len(sv32_regs) - 1, -1, -1):
        name = f'{base_name}_{i:02}'
        next_name = f'{base_name}_{i+1:02}'
        reg = f'{sv32_regs[i]}'

        if not args.restore:
            sp_write = f'*:$(REGSIZE) (sp - $(REGSIZE)*({i+1}-rt_raw)) = {reg};'
            sp_write_gp = f'*:$(REGSIZE) (sp - $(REGSIZE)*({i+1}-rt_raw)) = gp;'
        else:
            sp_write = f'{reg} = *:$(REGSIZE) (sp + lo_uimm12_sl3 - $(REGSIZE)*({i+1}-rt_raw));'
            sp_write_gp = f'gp = *:$(REGSIZE) (sp + lo_uimm12_sl3 - $(REGSIZE)*({i+1}-rt_raw));'

        offs_pattern = ' & lo_uimm12_sl3' if args.restore else ''

        # this is last register and gp is set (always end with gp)
        print(f'{name}: gp\t\t\t\t\tis count = {i+1} - rt_raw & rt_raw & gp; gp_end = 1{offs_pattern}\t{{{sp_write_gp}}}')

        # this is last register
        print(f'{name}: {reg}\t\t\t\t\tis count = {i+1} - rt_raw & rt_raw & {reg}; gp_end = 0{offs_pattern}\t{{{sp_write}}}')

        if i != len(sv32_regs) - 1:
            if args.restore:
                pattern = '(rt_raw; lo_uimm12_sl3)'
            else:
                pattern = 'rt_raw ...'

            print(f'{name}: {reg},{next_name}\tis {pattern} & {next_name} & {reg}\t\t\t\t{{{sp_write}}}')

    # empty register list case for count = 0
    print(f'{base_name}: \t\t\tis count = 0 {{}}')

    # entry points to first register (fp or ra)
    for i in range(31, -1, -1):
        next_name = f'{base_name}_{i:02}'
        print(f'{base_name}: ,{next_name}\tis rt_raw = {i} ... & {next_name} {{}}')


if __name__ == '__main__':
    main()
