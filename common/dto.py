from dataclasses import dataclass, field
from .config_check import Configs


@dataclass
class FormData(Configs):
    name:str
    phone:str
    question:str
    send_to_email:list[str] = field(default_factory=lambda: FormData().get_param_list('SEND_TO_EMAIL'))
    send_from_email:str = field(default_factory=lambda: FormData().check_env_var('SEND_FROM_EMAIL'))
    bot_token:str = field(default_factory=lambda: FormData().check_env_var('BOT_TOKEN'))
    chat_id:str = field(default_factory=lambda: FormData().check_env_var('CHAT_ID'))