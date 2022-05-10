import yaml

class Settings:
    def __init__(self):
        self.number_network_failures = 0
        self.number_repair_teams = 0
        self.recovery_intensity = 0.00
        self.recovery_policy = 'LIFO'

    def read_settings(self, name_file):
        with open(name_file, 'r', encoding='utf-8') as file:
            read_data = yaml.load(file, Loader=yaml.FullLoader)
        self.number_network_failures = read_data['number of network failures']
        self.number_repair_teams = read_data['number of repair teams']
        self.recovery_intensity = read_data['recovery intensity']
        self.recovery_policy = read_data['recovery policy']

    @staticmethod
    def create_settings(name_file):
        data = {'number of network failures': 0, 'number of repair teams': 0, 'recovery intensity': 0.00,
                'recovery policy': 'LIFO'}
        with open(name_file, 'w', encoding='utf-8') as file:
            yaml.dump(data, file)


    def get_settings(self):
        return [self.number_network_failures, self.number_repair_teams, self.recovery_intensity, self.recovery_policy]

    def set_settings(self, name_file, settings):
        self.number_network_failures = settings[0]
        self.number_repair_teams = settings[1]
        self.recovery_intensity = settings[2]
        self.recovery_policy = settings[3]
        data = {'number of network failures': settings[0], 'number of repair teams': settings[1],
                'recovery intensity': settings[2], 'recovery policy': settings[3]}
        with open(name_file, 'w', encoding='utf-8') as file:
            yaml.dump(data, file)