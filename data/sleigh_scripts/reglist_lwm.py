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
            pcode =      f'*:4 (lo_rs_soffset9 + $(REGSIZE)*({i}-rt_raw)) = {reg}:4;'
            pcode_zero = f'*:4 (lo_rs_soffset9 + $(REGSIZE)*({i}-rt_raw)) = 0:4;'

            if reg == 'zero':
                # read from $zero is 0
                pcode = pcode_zero
        else:
            if reg == 'zero':
                pcode = ''  # write to $zero is NOP
            else:
                pcode = f'{reg} = sext(*:4 (lo_rs_soffset9 + $(REGSIZE)*({i}-rt_raw)));'

        # For SWM, if rt=0 then all writes are zero
        if not args.load and i <= 7:
            print(f'{name}: is (rt_raw ...) & (rt_raw2 = 0 ...) & (count3_mapped = {i+1} - rt_raw2 ...) & lo_rs_soffset9\t{{{pcode_zero}}}')

        # rule when this is last register
        if not args.load:
            print(f'{name}: is (rt_raw ...) & (rt_raw2 != 0 ...) & (count3_mapped = {i+1} - rt_raw2 ...) & lo_rs_soffset9\t{{{pcode}}}')
        else:
            print(f'{name}: is (rt_raw ...) & (count3_mapped = {i+1} - rt_raw2 ...) & lo_rs_soffset9\t{{{pcode}}}')

        # rule when there are more registers
        if i != len(flat_reglist) - 1:
            pattern = '(rt_raw ...) & lo_rs_soffset9'

            if (not args.load) and i<= 7:
                print(f'{name}: is (rt_raw2 = 0 ...) & {pattern} & {next_name}\t\t\t\t{{{pcode_zero}}}')

            print(f'{name}: is {pattern} & {next_name}\t\t\t\t{{{pcode}}}')

    # entry points to first register (fp or ra)
    for i in range(31, -1, -1):
        next_name = f'{base_name}_{i:02}'
        print(f'{base_name}: is (rt_raw = {i} ...) & {next_name} {{}}')

    # pre-constructor to get mapped count3 value in constraints
    print(f'{base_name}_pre: {base_name} is (rt_raw; count3 = 0) & {base_name} [count3_mapped = 8;] {{}}')
    print(f'{base_name}_pre: {base_name} is (rt_raw; count3) & {base_name} [count3_mapped = count3;] {{}}')



if __name__ == '__main__':
    main()
