from dataclasses import dataclass, field
from typing import List
from functools import wraps
from common.config_check import Configs


def with_provider(provider_class):
    def decorator(cls):
        original_init = cls.__init__

        @wraps(cls.__init__)
        def new_init(self, *args, **kwargs):
            self.provider = provider_class()
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init
        return cls
    return decorator

@with_provider(Configs)
@dataclass
class FormData:
    name: str
    phone: str
    question: str
    send_to_email: List[str] = field(init=False)
    send_from_email: str = field(init=False)
    bot_token: str = field(init=False)
    chat_id: str = field(init=False)

    def __post_init__(self):
        self.send_to_email = self.provider.get_param_list('SEND_TO_EMAIL')
        self.send_from_email = self.provider.check_env_var('SEND_FROM_EMAIL')
        self.bot_token = self.provider.check_env_var('BOT_TOKEN')
        self.chat_id = self.provider.check_env_var('CHAT_ID')

@with_provider(Configs)
@dataclass
class DtoBotConfigs:
    supergroup_id: str = field(init=False)
    admin_user_ids: List[str] = field(init=False)
    bot_token: str = field(init=False)
    site_api_url:str = field(init=False)

    def __post_init__(self):
        self.supergroup_id = self.provider.check_env_var('SUPERGROUP_ID')
        self.admin_user_ids = self.provider.get_param_list('ADMIN_IDS')
        self.bot_token = self.provider.check_env_var('BOT_TOKEN')
        self.site_api_url = self.provider.check_env_var("YOUR_SITE_API_URL")