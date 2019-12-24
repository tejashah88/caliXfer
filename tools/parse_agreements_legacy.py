import re
from pprint import PrettyPrinter
ezprint = PrettyPrinter(indent=4).pprint

from scrape_content import scrape_articulation_by_major

def count_chars_for_lines(raw_txt):
    return [len(line) for line in raw_txt.splitlines()]

def split_agreement_by_blocks(raw_txt):
    lines = raw_txt.splitlines()
    num_dashes = [line.count('-') for line in lines]
    mean_dashes = sum(num_dashes) / len(num_dashes)

    blocks = []
    buffer = ''
    for line in lines:
        if line.count('-') >= mean_dashes:
            blocks += [buffer]
            buffer = ''
        else:
            buffer += line + '\n'

    return blocks

# since each valid block has an equal number of bars and newlines, we can split the block with both delimiters
# and pair the even-indexed parts together as well as the odd-indexed parts
def split_block_by_side(block):
    block_parts = re.split('[|\n]', block)
    print(block_parts)
    origin_block = '\n'.join(block_parts[::2])
    dest_block = '\n'.join(block_parts[1::2])
    print('>>> ORIGIN BLOCK')
    print(origin_block)
    print('>>> END ORIGIN BLOCK')
    print()
    print('>>> DEST BLOCK')
    print(dest_block)
    print('>>> END DEST BLOCK')
    print()
    return [origin_block, dest_block]

def split_all_course_blocks_by_side(blocks):
    finished_blocks = []
    for block in blocks:
        count_newlines = sum(ch == '\n' for ch in block)
        count_bars = sum(ch == '|' for ch in block)
        finished_blocks += [split_block_by_side(block) if count_bars == count_newlines else block]

    return finished_blocks

def append_missing_spaces(raw_txt):
    lines = raw_txt.splitlines()
    max_len = max([len(line) for line in lines])
    fixed_lines = [line.ljust(max_len) for line in lines]
    return '\n'.join(fixed_lines)


def parse_major_agreement(agreement_text):
    space_filled = append_missing_spaces(agreement_text)
    blocks = split_agreement_by_blocks(space_filled)
    finalized_blocks = split_all_course_blocks_by_side(blocks)
    # print(count_chars_for_lines(space_filled))
    # [ezprint(block) for block in split_all_course_blocks_by_side(blocks)]
    # split_all_course_blocks_by_side(blocks)
    return finalized_blocks

if __name__ == '__main__':
    # txt = scrape_articulation_by_major('DIABLO', '16-17', 'UCB', 'EECS')
    # txt = scrape_articulation_by_major('DIABLO', '16-17', 'CSUC', 'ENGMT')
    # txt = scrape_articulation_by_major('SDSU', '16-17', 'CSULA', 'CE')

    with open('./data/dump-dvc-info/agreements/UCB/EECS.txt', 'r') as file:
        from time import time
        start = time()

        content = file.read()
        parse_major_agreement(content)

        end = time()
        print((end - start) * 1000, 'ms')