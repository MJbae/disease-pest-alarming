def _convert_text_to_data_structure(text):
    """
    Convert text to python data structure

    Parameters:
    text(str): text from OPEN API response

    Returns:
    result(list): list of dictionary elements
    """

    key_idx_start = 0
    key_idx_end = 0
    value_idx_start = 0
    value_idx_end = 0
    result = []
    temp_dict = {}

    for idx, char in enumerate(text):
        if char == "{":
            key_idx_start = idx + 1
        if char == ",":
            value_idx_end = idx
            key = text[key_idx_start:key_idx_end]
            value = text[value_idx_start:value_idx_end]
            temp_dict[key] = value
        if char == " ":
            key_idx_start = idx + 1
        if char == "=":
            key_idx_end = idx
            value_idx_start = idx + 1
        if char == "}":
            idx += 2
            key = text[key_idx_start:key_idx_end]
            value = text[value_idx_start:value_idx_end]
            temp_dict[key] = value
            result.append(temp_dict)
            temp_dict = {}

    return result
