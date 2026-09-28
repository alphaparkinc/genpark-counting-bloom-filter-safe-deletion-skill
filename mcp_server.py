import sys
import json
from client import CountingBloomFilter

cbf = CountingBloomFilter(size=128, num_hashes=3)

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
                        "name": "counting_bloom_filter",
                        "description": "Add, remove, or test membership with Counting Bloom Filter",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {"type": "string", "enum": ["add", "remove", "contains"]},
                                "item": {"type": "string"}
                            },
                            "required": ["action", "item"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "counting_bloom_filter":
            act = args["action"]
            item = args["item"]
            if act == "add":
                cbf.add(item)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"action": "add", "item": item, "status": "OK"})}]}}
            elif act == "remove":
                ok = cbf.remove(item)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"action": "remove", "item": item, "removed": ok})}]}}
            elif act == "contains":
                present = cbf.contains(item)
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"item": item, "contains": present})}]}}
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
