#!/usr/bin/env python3
"""
Analyze RabbitMQ DLQ messages exported from the Management API.

Usage:
  python3 analyze_messages.py /tmp/dlq_messages.json
  python3 analyze_messages.py /tmp/dlq_messages.json --fields clientId,family,category
  python3 analyze_messages.py /tmp/dlq_messages.json --detail 10
"""

import json
import sys
import argparse
from collections import Counter


def load_messages(path):
    with open(path) as f:
        return json.load(f)


def analyze_headers(msgs):
    print("=" * 60)
    print("HEADER ANALYSIS")
    print("=" * 60)

    nack_count = 0
    xdeath_counts = []

    for m in msgs:
        headers = m.get("properties", {}).get("headers", {})
        if headers.get("rascal.immediateNack", False):
            nack_count += 1
        xdeath = headers.get("x-death", [])
        if xdeath:
            xdeath_counts.append(xdeath[0].get("count", 0))

    print(f"  Total messages: {len(msgs)}")
    print(f"  With immediateNack: {nack_count}")
    print(f"  Without immediateNack: {len(msgs) - nack_count}")

    if xdeath_counts:
        print(f"  x-death count range: {min(xdeath_counts)} - {max(xdeath_counts)}")
        print(f"  x-death count avg: {sum(xdeath_counts) / len(xdeath_counts):.1f}")

    rkeys = set(m.get("routing_key", "") for m in msgs)
    print(f"  Unique routing keys: {rkeys}")
    print()


def analyze_schemas(msgs):
    print("=" * 60)
    print("SCHEMA VARIATIONS")
    print("=" * 60)

    key_combos = {}
    for m in msgs:
        p = json.loads(m.get("payload", "{}"))
        combo = tuple(sorted(p.keys()))
        key_combos[combo] = key_combos.get(combo, 0) + 1

    print(f"  {len(key_combos)} schema variation(s):\n")
    for combo, cnt in sorted(key_combos.items(), key=lambda x: -x[1]):
        print(f"  [{cnt} msgs] {list(combo)}")

    # Show diff between schemas if there are exactly 2
    if len(key_combos) == 2:
        schemas = list(key_combos.keys())
        s1, s2 = set(schemas[0]), set(schemas[1])
        only_in_first = s1 - s2
        only_in_second = s2 - s1
        if only_in_first:
            print(f"\n  Only in schema 1 ({key_combos[schemas[0]]} msgs): {only_in_first}")
        if only_in_second:
            print(f"  Only in schema 2 ({key_combos[schemas[1]]} msgs): {only_in_second}")
    print()


def analyze_fields(msgs, fields):
    print("=" * 60)
    print("FIELD DISTRIBUTIONS")
    print("=" * 60)

    for field in fields:
        values = Counter()
        missing = 0
        for m in msgs:
            p = json.loads(m.get("payload", "{}"))
            if field in p:
                val = str(p[field])
                # Truncate long values
                if len(val) > 50:
                    val = val[:50] + "..."
                values[val] += 1
            else:
                missing += 1

        if not values and missing == len(msgs):
            continue

        print(f"\n  {field}: {len(values)} unique values", end="")
        if missing > 0:
            print(f" ({missing} missing)", end="")
        print()

        for val, cnt in values.most_common(10):
            print(f"    {val}: {cnt}")
    print()


def show_detail(msgs, n):
    print("=" * 60)
    print(f"MESSAGE DETAIL (first {n})")
    print("=" * 60)

    for i, m in enumerate(msgs[:n]):
        headers = m.get("properties", {}).get("headers", {})
        xdeath = headers.get("x-death", [])
        count = xdeath[0].get("count", 0) if xdeath else "N/A"
        nack = headers.get("rascal.immediateNack", False)
        payload = json.loads(m.get("payload", "{}"))
        routing_key = m.get("routing_key", "N/A")

        print(f"\n  --- Message {i + 1} ---")
        print(f"  routing_key: {routing_key}")
        print(f"  immediateNack: {nack}")
        print(f"  x-death count: {count}")
        print(f"  payload keys: {list(payload.keys())}")

        # Show a few key fields
        for key in ["id", "clientId", "family", "category", "type"]:
            if key in payload:
                val = str(payload[key])
                if len(val) > 60:
                    val = val[:60] + "..."
                print(f"  {key}: {val}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Analyze RabbitMQ DLQ messages")
    parser.add_argument("file", help="Path to DLQ messages JSON file")
    parser.add_argument(
        "--fields",
        default="clientId,family,category,type,status",
        help="Comma-separated fields to analyze distribution (default: clientId,family,category,type,status)",
    )
    parser.add_argument(
        "--detail",
        type=int,
        default=5,
        help="Number of messages to show in detail (default: 5)",
    )
    args = parser.parse_args()

    msgs = load_messages(args.file)
    fields = [f.strip() for f in args.fields.split(",")]

    print(f"\nAnalyzing {len(msgs)} messages from {args.file}\n")

    analyze_headers(msgs)
    analyze_schemas(msgs)
    analyze_fields(msgs, fields)
    show_detail(msgs, args.detail)


if __name__ == "__main__":
    main()
