import yaml

def read_config(file_path):
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return config_data
