#!/usr/bin/env python3

# Reverse all bits
bit_str = ''

for i in range(32):
    swap_i = 31 - i

    bit_str += f'((rs >> {swap_i} & 1) << {i})'

    if i < 31:
        bit_str += ' | '

    if i > 1 and i % 4 == 0:
        bit_str += '\n\t'

print(f'rt = {bit_str};')
