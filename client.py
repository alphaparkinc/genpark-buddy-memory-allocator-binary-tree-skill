"""Binary Buddy System Memory Allocator.
100% Python Standard Library.
"""

import collections

class BuddyAllocator:
    """Binary buddy system memory allocator over power-of-two blocks."""
    def __init__(self, total_size=1024, min_block_size=16):
        self.total_size = total_size
        self.min_block = min_block_size
        self.max_order = (total_size // min_block_size).bit_length() - 1
        self.free_lists = collections.defaultdict(list)
        self.free_lists[self.max_order].append(0)
        self.allocated = {}

    def allocate(self, size):
        needed = max(size, self.min_block)
        blocks_needed = (needed + self.min_block - 1) // self.min_block
        order = (blocks_needed - 1).bit_length()
        current_order = order
        while current_order <= self.max_order and not self.free_lists[current_order]:
            current_order += 1
        if current_order > self.max_order:
            return None

        offset = self.free_lists[current_order].pop(0)
        while current_order > order:
            current_order -= 1
            buddy_offset = offset + (1 << current_order) * self.min_block
            self.free_lists[current_order].append(buddy_offset)

        self.allocated[offset] = order
        return offset

    def free(self, offset):
        if offset not in self.allocated:
            return False
        order = self.allocated.pop(offset)
        while order < self.max_order:
            buddy_offset = offset ^ ((1 << order) * self.min_block)
            if buddy_offset in self.free_lists[order]:
                self.free_lists[order].remove(buddy_offset)
                offset = min(offset, buddy_offset)
                order += 1
            else:
                break
        self.free_lists[order].append(offset)
        return True
