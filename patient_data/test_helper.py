def get_optional_fields_test_data(optional_fields):
    optional_fields_data = []
    for model_data in optional_fields:
        incorrect_inp_lengths = [
            len(field_data["inputs"]) for field_data in model_data["incorrect_fields"]
        ]
        incorrect_inp_lengths.sort(reverse=True)
        longest_length = incorrect_inp_lengths[0]
        optional_data_collection = []
        for i in range(longest_length):
            optional_data = {k: v for k, v in model_data.items()}
            incorrect_data_collection = []
            for data in model_data["incorrect_fields"]:
                incorrect_data = {}
                inputs_len = len(data["inputs"])
                incorrect_data["field"] = data["field"]
                incorrect_data["input"] = data["inputs"][i % inputs_len]
                incorrect_data_collection.append(incorrect_data)
            optional_data["incorrect_fields"] = incorrect_data_collection
            optional_data_collection.append(optional_data)
        optional_fields_data.append(optional_data_collection)
    return [optional_fields_data]
