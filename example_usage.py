from client import CountingBloomFilter

cbf = CountingBloomFilter(size=128, num_hashes=3)
cbf.add("file_chunk_001")
cbf.add("file_chunk_002")

print("Contains chunk 001?", cbf.contains("file_chunk_001"))
print("Contains chunk 999?", cbf.contains("file_chunk_999"))

cbf.remove("file_chunk_001")
print("Contains chunk 001 after removal?", cbf.contains("file_chunk_001"))
