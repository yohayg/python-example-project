import logging

from faker import Faker

log = logging.getLogger("DataGenerator")


class DataGenerator:

    def __init__(self):
        pass

    @staticmethod
    def get_header():
        return ['Email', 'First Name', 'Last Name']

    @staticmethod
    def get_fake_data(fake):
        # We need to seed in multi processing/ threading otherwise it will generate the same data

        first = str(fake.first_name())
        last = str(fake.last_name())
        email = str(fake.email())
        line = [email, first, last]
        return line


def generate_data(bulk, index):
    log.debug('long time task begins')
    result = []
    fake = Faker()
    if index is not None:
        fake.seed_instance(index)
    for _ in range(bulk):
        line = DataGenerator.get_fake_data(fake)
        result.append(line)
    log.debug('long time task finished %s' % result)

    return result
