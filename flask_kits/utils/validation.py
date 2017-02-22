import re

cell_phone_reg = re.compile("^1\\d{10}$")


def is_cell_phone(phone):
    return cell_phone_reg.match(phone) is not None
