def _compare_params(p1, p2):
    return p1 is not None and p2 is not None and 0 < p1 <= p2


def _make_name_str(r, ct, pac=None):
    r = str(r).rjust(2, '0')
    ct = str(ct).rjust(2, '0')

    if pac is None:
        return "R{}-CT{}".format(r, ct)

    pac = str(pac).rjust(2, '0')

    return "R{}-CT{}-PAC{}".format(r, ct, pac)


def _make_numbers_list(init, end):
    num_list = list(range(init, end))

    num_list.append(end)

    return num_list


def _resolve_two(r_init, r_end, ct_init, ct_end):
    r_list = _make_numbers_list(r_init, r_end)
    ct_list = _make_numbers_list(ct_init, ct_end)

    name_str_list = []

    for r in r_list:
        for ct in ct_list:
            name_str = _make_name_str(r, ct)
            name_str_list.append(name_str)

    return name_str_list


def _resolve_tree(r_init, r_end, ct_init, ct_end, pac_init, pac_end):
    r_list = _make_numbers_list(r_init, r_end)
    ct_list = _make_numbers_list(ct_init, ct_end)
    pac_list = _make_numbers_list(pac_init, pac_end)

    name_str_list = []

    for r in r_list:
        for ct in ct_list:
            for pac in pac_list:
                name_str = _make_name_str(r, ct, pac)
                name_str_list.append(name_str)

    return name_str_list


def make_identifier_list(r_init, r_end, ct_init, ct_end, pac_init=None, pac_end=None):

    if not _compare_params(r_init, r_end):
        return []

    if not _compare_params(ct_init, ct_end):
        return []

    if _compare_params(pac_init, pac_end):
        return _resolve_tree(r_init, r_end, ct_init, ct_end, pac_init, pac_end)

    return _resolve_two(r_init, r_end, ct_init, ct_end)

