class Identifiers:
    r_init, r_end, ct_init, ct_end, pac_init, pac_end = 0, 0, 0, 0, None, None

    def __init__(self, r_init, r_end, ct_init, ct_end, pac_init=None, pac_end=None):
        self.r_init = r_init
        self.r_end = r_end
        self.ct_init = ct_init
        self.ct_end = ct_end
        self.pac_init = pac_init
        self.pac_end = pac_end

    def list(self):
        if not self.__compare_params(self.r_init, self.r_end):
            return []

        if not self.__compare_params(self.ct_init, self.ct_end):
            return []

        if self.__compare_params(self.pac_init, self.pac_end):
            return self.__resolve_tree(self.r_init, self.r_end, self.ct_init, self.ct_end, self.pac_init, self.pac_end)

        return self.__resolve_two(self.r_init, self.r_end, self.ct_init, self.ct_end)

    @staticmethod
    def __compare_params(p1, p2):
        return p1 is not None and p2 is not None and 0 < p1 <= p2

    @staticmethod
    def __make_name_str(r, ct, pac=None):
        r = str(r).rjust(2, '0')
        ct = str(ct).rjust(2, '0')

        if pac is None:
            return "R{}-CT{}".format(r, ct)

        pac = str(pac).rjust(2, '0')

        return "R{}-CT{}-PAC{}".format(r, ct, pac)

    @staticmethod
    def __make_numbers_list(init, end):
        num_list = list(range(init, end))

        num_list.append(end)

        return num_list

    def __resolve_two(self, r_init, r_end, ct_init, ct_end):
        r_list = self.__make_numbers_list(r_init, r_end)
        ct_list = self.__make_numbers_list(ct_init, ct_end)

        name_str_list = []

        for r in r_list:
            for ct in ct_list:
                name_str = self.__make_name_str(r, ct)
                name_str_list.append(name_str)

        return name_str_list

    def __resolve_tree(self, r_init, r_end, ct_init, ct_end, pac_init, pac_end):
        r_list = self.__make_numbers_list(r_init, r_end)
        ct_list = self.__make_numbers_list(ct_init, ct_end)
        pac_list = self.__make_numbers_list(pac_init, pac_end)

        name_str_list = []

        for r in r_list:
            for ct in ct_list:
                for pac in pac_list:
                    name_str = self.__make_name_str(r, ct, pac)
                    name_str_list.append(name_str)

        return name_str_list
