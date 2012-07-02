"""Construct synthetic CSV documents and independently specified expected statistics."""
import argparse
import csv
import io
import json


def make_case(index):
    label = "synthetic-csv-{:04d}".format(index)
    kind = index % 9
    if kind == 0:
        return {"id": label, "input": "item,item\na,b\n", "expected_error": True}
    if kind == 1:
        return {"id": label, "input": "item,amount\na,2,extra\n", "expected_error": True}
    if kind == 2:
        return {"id": label, "input": 'item,amount\n"unfinished,2', "expected_error": True}
    count = 1 + index % 4
    items = ["item_{}_{}".format(index, row) for row in range(count)]
    amounts = ["{}.25".format(index % 100 + row) if row % 2 == 0 else ("" if index % 3 == 0 else "n/a") for row in range(count)]
    notes = ['synthetic, "quoted"' if row % 2 == 0 else "" for row in range(count)]
    handle = io.StringIO(newline="")
    writer = csv.writer(handle)
    writer.writerow(["item", "amount", "notes"])
    writer.writerows(zip(items, amounts, notes))
    columns = []
    for name, cells, numeric_count in (("item", items, 0), ("amount", amounts, (count + 1) // 2), ("notes", notes, 0)):
        present = [cell for cell in cells if cell]
        columns.append({"name": name, "nonempty": len(present), "empty": count - len(present),
                        "numeric": numeric_count, "distinct": len(set(present)), "max_length": max(map(len, cells))})
    return {"id": label, "input": handle.getvalue(), "expected": {"row_count": count, "columns": columns}}


def main():
    parser = argparse.ArgumentParser(description="Print generated CSV cases as JSONL.")
    parser.add_argument("--count", type=int, default=20)
    args = parser.parse_args()
    if not 1 <= args.count <= 10000:
        parser.error("Count must be between 1 and 10000")
    for index in range(args.count):
        print(json.dumps(make_case(index), ensure_ascii=True, sort_keys=True))


if __name__ == "__main__":
    main()
