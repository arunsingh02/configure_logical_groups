from uuid import uuid5, NAMESPACE_DNS


class Utility:
    @staticmethod
    def uuid5_converter(string: str) -> str:
        return str(uuid5(NAMESPACE_DNS, string))


if __name__ == '__main__':
    utility_obj = Utility()
