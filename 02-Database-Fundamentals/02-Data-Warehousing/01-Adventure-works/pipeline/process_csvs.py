import glob
import codecs
import shutil


def guess_encoding(file_path):
    encodings_to_try = ["utf-8", "utf-16-le", "utf-16-be"]

    for enc in encodings_to_try:
        try:
            with codecs.open(file_path, encoding=enc) as f:
                f.read(4)
            return enc
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Could not determine encoding for file {file_path}")


def process_file(csv_file):
    print("Processing file: ", csv_file)
    is_needed = csv_file.endswith("Address.csv")
    if is_needed:
        encoding = "windows-1252"
    else:
        encoding = guess_encoding(csv_file)

    with codecs.open(csv_file, "r", encoding=encoding) as f:
        output = []
        text = ""
        is_first = True
        is_pipes = False

        for line in f:
            if is_first:
                if "+|" in line:
                    is_pipes = True
                if line.startswith("\uFEFF"):
                    line = line[1:]
                    is_needed = True

            is_first = False

            if not is_needed:
                break

            if is_pipes:
                if line.strip().endswith("&|"):
                    text += line.replace('"', '""').strip()[:-2]
                    output.append(
                        "\t".join(
                            [
                                '"' + part + '"' if "\t" in part else part
                                for part in text.split("+|")
                            ]
                        )
                        + "\n"
                    )
                    text = ""
            else:
                line_modified = (
                    line.replace('"', '""')
                    .replace("&|\n", "\n")
                    .replace("&|\r\n", "\n")
                )
                output.append(line_modified.replace("\r\n", "\n"))

        if is_needed:
            with open(
                csv_file.replace("original", "processed"), "w", encoding="utf-8"
            ) as w:
                w.write("".join(output))
        else:
            shutil.copyfile(csv_file, csv_file.replace("original", "processed"))


for csv_file in glob.glob("data/original/*.csv"):
    process_file(csv_file)
