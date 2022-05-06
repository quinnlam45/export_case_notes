# Case note data functions

# returns list of sliced strings
def slice_str(string_data, slice_length):
    sliced_str_list = []
    notes_str = string_data
    char_count = len(notes_str)
    
    while char_count > 0:

        if char_count > slice_length + 1:
            # find next available space/char to slice
            slice_pos = return_slice_length(notes_str, slice_length)
            sliced_str = notes_str[:slice_pos]
            sliced_str_list.append(sliced_str)
            char_count -= slice_pos

            # slice out appended chars from string update notes_str
            notes_str = notes_str[slice_pos:]
            
            # update char counter
            char_count = len(notes_str)
        else:
            sliced_str_list.append(notes_str)
            break
    
    sliced_str_list = add_contd_to_sliced_str_list_items(sliced_str_list)

    return sliced_str_list

def add_contd_to_sliced_str_list_items(sliced_str_list):
    # append strings to sliced text
    for x, line in enumerate(sliced_str_list):
        if x == 0:
            sliced_str_list[x] = line + " ..."
        elif x == len(sliced_str_list)-1:
            sliced_str_list[x] = "[cont'd] " + line
        else:
            sliced_str_list[x] = "[cont'd] " + line + " ..."
    return sliced_str_list

# finds next available space or "." in string and returns character position
def return_slice_length(string_data, slice_len):
    slice_length = slice_len
    char = string_data[slice_length]
    string_length = len(string_data)-slice_length

    while char != " " and char != "." and slice_length < len(string_data)-1:
        slice_length += 1
        char = string_data[slice_length]
        string_length -= 1

    #print(slice_length)
    return slice_length

# copy current row for each sliced string
def return_copied_rows_for_sliced_str(current_row, sliced_str_list):
    transformed_rows_for_sliced_str = []

    for sliced_str in sliced_str_list:
        sliced_str_row = current_row.copy()
        sliced_str_row.append(sliced_str)
        transformed_rows_for_sliced_str.append(sliced_str_row)

    return transformed_rows_for_sliced_str

# slice and format case note rows
def transform_case_note_data(case_note_data, string_length_limit = 1000):
    transformed_rows = []

    for datarow in case_note_data:
        row = []
        for item in datarow[5:]:
            if isinstance(item, str) and len(item) > string_length_limit:
                current_row = row
                # returns list of sliced strings
                sliced_str_list = slice_str(item, string_length_limit)
                
                # copy current row and append sliced string from list                
                transformed_sliced_str_rows = return_copied_rows_for_sliced_str(current_row, sliced_str_list)
                for sliced_str_row in transformed_sliced_str_rows:
                    transformed_rows.append(sliced_str_row)
                
                # reset row
                row = []
            else:
                row.append(item)
        if row:
            transformed_rows.append(row)

    return transformed_rows