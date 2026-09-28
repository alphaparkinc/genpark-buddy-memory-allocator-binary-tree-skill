import sys
import json
from client import BuddyAllocator

buddy = BuddyAllocator(total_size=1024, min_block_size=16)

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "buddy_allocator_op",
                        "description": "Allocate or free memory using binary buddy system",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["allocate", "free"]},
                                "size": {"type": "integer"},
                                "offset": {"type": "integer"}
                            },
                            "required": ["action"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "buddy_allocator_op":
            act = args["action"]
            if act == "allocate":
                off = buddy.allocate(args.get("size", 16))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"offset": off, "status": "ALLOCATED" if off is not None else "OOM"})}]}}
            elif act == "free":
                ok = buddy.free(args.get("offset", 0))
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"success": ok, "status": "FREED" if ok else "INVALID_OFFSET"})}]}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if line.strip():
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
