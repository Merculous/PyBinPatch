
import binascii
from itertools import zip_longest

from .file import readBinaryFromPath, writeJsonToPath


class Diff:
    def __init__(self, src1_path, src2_path, diff_path=None):
        self.src1_path = src1_path
        self.src2_path = src2_path
        self.diff_path = diff_path

        self.src1_data = readBinaryFromPath(self.src1_path)
        self.src2_data = readBinaryFromPath(self.src2_path)

        self.src1_len = len(self.src1_data)
        self.src2_len = len(self.src2_data)

        self.same_sizes = True if self.src1_len == self.src2_len else False

    def diff(self):
        data1 = iter(self.src1_data)
        data2 = iter(self.src2_data)

        differences = []

        for i, (v1, v2) in enumerate(zip_longest(data1, data2)):
            if not isinstance(v1, int):
                pass

            if not isinstance(v2, int):
                pass

            if v1 != v2:
                offset = hex(i)

                v1 = v1.to_bytes(1, 'little')
                v2 = v2.to_bytes(1, 'little')

                v1 = binascii.hexlify(v1).decode('utf-8')
                v2 = binascii.hexlify(v2).decode('utf-8')

                difference = (offset, v1, v2)

                differences.append(difference)

        iter_differences = iter(differences)

        differences_updated = {}

        start_offset = 0
        last_offset = 0

        old_buff = ''
        new_buff = ''

        for offset, v1, v2 in iter_differences:
            try:
                next_offset, next_v1, next_v2 = next(iter_differences)
            except StopIteration:
                break

            offset_int = int(offset, 16)
            next_offset_int = int(next_offset, 16)

            if start_offset == 0:
                old_buff = v1 + next_v1
                new_buff = v2 + next_v2

                start_offset = offset_int
                last_offset = next_offset_int

                continue

            if offset_int != last_offset + 1:
                if start_offset_hex not in differences_updated:
                    differences_updated[start_offset_hex] = {
                        'old': old_buff,
                        'new': new_buff
                    }

                old_buff = ''
                new_buff = ''

                start_offset = offset_int
                last_offset = start_offset - 1

            if offset_int == last_offset + 1:
                start_offset_hex = hex(start_offset)

                old_buff += v1
                new_buff += v2

                if start_offset_hex in differences_updated:
                    differences_updated[start_offset_hex]['old'] += old_buff
                    differences_updated[start_offset_hex]['new'] += new_buff

                    old_buff = ''
                    new_buff = ''

                last_offset = offset_int

                if next_offset_int == offset_int + 1:
                    old_buff += next_v1
                    new_buff += next_v2

                    if start_offset_hex in differences_updated:
                        differences_updated[start_offset_hex]['old'] += old_buff
                        differences_updated[start_offset_hex]['new'] += new_buff

                        old_buff = ''
                        new_buff = ''

                    last_offset = next_offset_int

                else:
                    differences_updated[next_offset] = {
                        'old': next_v1,
                        'new': next_v2
                    }

                    old_buff = ''
                    new_buff = ''

                    start_offset = next_offset_int
                    last_offset = start_offset

        return differences_updated

    def writeDiffToPath(self):
        if not self.diff_path:
            raise Exception('Please set a diff path!')

        differences = self.diff()

        writeJsonToPath(self.diff_path, differences)
