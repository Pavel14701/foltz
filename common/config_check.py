import os
from dotenv import load_dotenv


class Configs:
    type_map = {
        'str': str,
        'int': int,
        'bool': lambda v: v.lower() in ('true', '1', 'yes'),
        'float': float
    }

    def __init__(self):
        load_dotenv()

    def check_env_var(self, key:str, _type:str='str') -> str|int|bool|float:
        value = os.getenv(key.upper())
        if value is None:
            raise ValueError(f"Environment variable '{key.upper()}' is not set")
        try:
            return self.type_map[_type](value)
        except KeyError:
            raise ValueError(f"Unsupported type for variable '{key.upper()}'")

    def get_param_list(self, key: str, _type: str = 'str') -> list[str|int|bool|float]|str|int|bool|float:
        if not (values:= os.getenv(f'{key.upper()}')):
            raise ValueError(f'Missing parameters for {key.upper()}')
        try:
            if ',' in values:
                return [self.type_map[_type](value) for value in values.split(',')]
            else:
                return self.type_map[_type](values)
        except KeyError:
            raise ValueError(f"Unsupported type for variable '{key.upper()}'")
