

def str_to_arr(string: str):
    str_to_arr = string.split(",")
    str_to_arr = [b.strip() for b in str_to_arr if b.strip()]  # removes spaces
    return str_to_arr