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
    parser.add_argument('--load', action='store_true', default=False)
    args = parser.parse_args()

    if args.load:
        base_name = 'reglist_lwm'
    else:
        base_name = 'reglist_swm'

    flat_reglist = REGS + REGS[16:23]
    #print(flat_reglist)
    #print(len(flat_reglist))

    for i in range(len(flat_reglist) - 1, -1, -1):
        name = f'{base_name}_{i:02}'
        next_name = f'{base_name}_{i+1:02}'
        reg = f'{flat_reglist[i]}'

        if not args.load:
            #sp_write = f'*:$(REGSIZE) (sp - $(REGSIZE)*({i+1}-rt_raw)) = {reg};'
            sp_write = 'BAD BAD BAD'
        else:
            sp_write = f'{reg} = *:4 (lo_rs_soffset9 + $(REGSIZE)*({i}-rt_raw));'

        # this is last register
        print(f'{name}: {reg}\t\t\t\t\tis {reg} & (rt_raw ...) & (count3_mapped = {i+1} - rt ...) & lo_rs_soffset9\t{{{sp_write}}}')

        if i != len(flat_reglist) - 1:
            pattern = '(rt_raw ...) & lo_rs_soffset9'

            print(f'{name}: {reg},{next_name}\tis {reg} & {pattern} & {next_name}\t\t\t\t{{{sp_write}}}')

    # entry points to first register (fp or ra)
    for i in range(31, -1, -1):
        next_name = f'{base_name}_{i:02}'
        print(f'{base_name}: ,{next_name}\tis (rt_raw = {i} ...) & {next_name} {{}}')

    # pre-constructor to get mapped count3 value in constraints
    # reglist_lwm_pre: reglist_lwm is (rt_raw; count3 = 0) & reglist_lwm [count3_mapped = 8;] {}
    # reglist_lwm_pre: reglist_lwm is (rt_raw; count3) & reglist_lwm [count3_mapped = count3;] {}



if __name__ == '__main__':
    main()
