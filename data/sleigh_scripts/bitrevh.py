#!/usr/bin/env python3

# Reverse all bits
bit_str = ''

width = 16

for i in range(width):
    swap_i = (width - 1) - i

    bit_str += f'((rs >> {swap_i} & 1) << {i})'

    if i < (width - 1):
        bit_str += ' | '

    if i > 1 and i % 4 == 0:
        bit_str += '\n\t'

print(f'replaceme = {bit_str};')
