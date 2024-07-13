import json


def normalize_json_to_dicts(input_file):
    data = json.load(input_file)
    # print(data)
    n_rows = len(next(iter(data.values())))

    records = []
    for i in range(n_rows):
        record = {}
        for key, values in data.items():
            # if key == "class":
            #     record["class_field"] = values.get(str(i), None)
            # else:
            #     record[key] = values.get(str(i), None)  # handle nulls
            record[key] = values.get(str(i), None)
        records.append(record)

    return records
