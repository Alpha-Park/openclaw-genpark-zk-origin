# -*- coding: utf-8 -*-
"""
OpenClaw GenPark ZK Origin MCP Server
Exposes Merkle tree data provenance and inclusion verification tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import OpenClawGenParkZKOrigin

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "openclaw-genpark-zk-origin", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "build_merkle_tree",
                        "description": "Constructs binary Merkle trees over telemetry checkpoints and generates Merkle root.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "data_leaves": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": ["data_leaves"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "build_merkle_tree":
            zk = OpenClawGenParkZKOrigin()
            res = zk.build_merkle_tree(args.get("data_leaves", []))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        z = OpenClawGenParkZKOrigin()
        test_res = z.build_merkle_tree(["block-1", "block-2"])
        print(f"Test Root: {test_res['merkle_root_hex'][:16]}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
