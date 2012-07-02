"""Column-level statistics for small CSV inputs."""
import csv
import io
import re

NUMBER = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)")


def profile(text, delimiter=","):
    if not isinstance(text, str):
        raise ValueError("CSV input must be text")
    if len(delimiter) != 1 or delimiter in "\r\n\x00":
        raise ValueError("Delimiter must be one non-newline character")
    try:
        reader = csv.reader(io.StringIO(text, newline=""), delimiter=delimiter, strict=True)
        raw_headers = next(reader, None)
        if raw_headers is None:
            raise ValueError("CSV input needs a header row")
        headers = [name.strip() for name in raw_headers]
        if not headers or any(not name for name in headers) or len(set(headers)) != len(headers):
            raise ValueError("Headers must be nonempty and unique after trimming")
        values = [[] for _ in headers]
        count = 0
        for row in reader:
            if len(row) != len(headers):
                raise ValueError("Row {} has the wrong number of columns".format(reader.line_num))
            for column, cell in zip(values, row):
                column.append(cell.strip())
            count += 1
    except csv.Error as error:
        raise ValueError("Invalid CSV: " + str(error)) from error
    columns = []
    for name, cells in zip(headers, values):
        nonempty = [cell for cell in cells if cell]
        columns.append({"name": name, "nonempty": len(nonempty), "empty": count - len(nonempty),
                        "numeric": sum(NUMBER.fullmatch(cell) is not None for cell in nonempty),
                        "distinct": len(set(nonempty)), "max_length": max(map(len, cells), default=0)})
    return {"row_count": count, "columns": columns}
