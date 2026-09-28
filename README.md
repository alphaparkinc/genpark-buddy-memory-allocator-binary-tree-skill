# Buddy Memory Allocator Skill

High-efficiency, zero-dependency Python implementation of the **Binary Buddy System Memory Allocator**.

## Features
- **Power-of-Two Splitting**: Minimizes external fragmentation via recursive block halving.
- **Fast XOR Coalescing**: Instant \(O(1)\) buddy pairing via bitwise XOR offset identity.
- **Zero External Dependencies**: Pure Python standard library.
- **Native MCP Protocol**: JSON-RPC 2.0 stdio server compatible with Claude Desktop, Cursor, and Windsurf.

## Architecture
```mermaid
graph TD
    Block1024["1024 KB Block"] --> B512_0["512 KB (Allocated)"]
    Block1024 --> B512_1["512 KB"]
    B512_1 --> B256_0["256 KB (Free)"]
    B512_1 --> B256_1["256 KB (Free)"]
```
