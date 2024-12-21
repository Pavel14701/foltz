from dataclasses import dataclass, field
from typing import List
from common.config_check import Configs


@dataclass
class FormData(Configs):
    name: str
    phone: str
    question: str
    send_to_email: List[str] = field(init=False)
    send_from_email: str = field(init=False)
    bot_token: str = field(init=False)
    chat_id: str = field(init=False)

    def __post_init__(self):
        self.send_to_email = self.get_param_list('SEND_TO_EMAIL')
        self.send_from_email = self.check_env_var('SEND_FROM_EMAIL')
        self.bot_token = self.check_env_var('BOT_TOKEN')
        self.chat_id = self.check_env_var('CHAT_ID')

@dataclass
class DtoBotConfigs(Configs):
    supergroup_id: str = field(init=False)
    admin_user_ids: List[str] = field(init=False)
    bot_token: str = field(init=False)
    site_api_url:str = field(init=False)
    use_webhook:bool = field(init=False)
    bot_webhook:str = field(init=False)
    user_name:str = field(init=False)
    password:str = field(init=False)

    def __post_init__(self):
        self.supergroup_id = self.check_env_var('SUPERGROUP_ID')
        self.admin_user_ids = self.get_param_list('ADMIN_IDS')
        self.bot_token = self.check_env_var('BOT_TOKEN')
        self.site_api_url = self.check_env_var("YOUR_SITE_API_URL")
        self.use_webhook = bool(int(self.check_env_var('USE_WEBHOOK')))
        self.bot_webhook = self.check_env_var('BOT_WEBHOOK')
        self.user_name = self.check_env_var('SITE_ADMIN_NAME')
        self.password = self.check_env_var('SITE_ADMIN_PASSWORD')