# -*- coding: utf-8 -*-
"""
Example usage of OpenClawGenParkZKOrigin
Demonstrates Merkle tree construction and cryptographic data provenance verification.
"""

from client import OpenClawGenParkZKOrigin

def main():
    zk = OpenClawGenParkZKOrigin()

    leaves = [
        "Audit Log #1: Agent initialized with policy constraints",
        "Audit Log #2: User approved budget cap $500",
        "Audit Log #3: Order executed at Walmart UCP endpoint",
        "Audit Log #4: AP2 settlement verified"
    ]

    tree = zk.build_merkle_tree(leaves)

    print("================================================================")
    print("OpenClaw GenPark ZK Origin - Data Provenance Verification")
    print("================================================================\n")
    print(f"Leaves Ingested       : {tree['leaves_count']} items")
    print(f"Tree Depth            : {tree['tree_depth']} levels")
    print(f"Cryptographic Root    : {tree['merkle_root_hex']}\n")
    print("Leaf Hashes:")
    for idx, h in enumerate(tree['leaf_hashes']):
        print(f"  Leaf #{idx + 1}: {h[:24]}... ({leaves[idx]})")

if __name__ == "__main__":
    main()
