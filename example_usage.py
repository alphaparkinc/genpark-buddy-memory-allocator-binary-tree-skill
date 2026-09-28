from client import BuddyAllocator

buddy = BuddyAllocator(total_size=512, min_block_size=16)
off1 = buddy.allocate(32)
off2 = buddy.allocate(64)
print(f"Allocated block 1 at offset {off1}, block 2 at offset {off2}")

buddy.free(off1)
buddy.free(off2)
print("Blocks successfully freed and coalesced.")
