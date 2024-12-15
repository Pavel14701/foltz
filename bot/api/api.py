import requests
from bot.api.consts import ApiUrls
from bot.bot_instance import configs

class Api:
    def __init__(self):
        api = ApiUrls()
        self.token_url = f'{api.base_url}{api.token}'
        self.token_refresh_url = f'{api.base_url}{api.token_refresh}'
        self.user_name = configs.user_name
        self.password = configs.password

    def __get_access_token(self) -> dict[str, str]:
        data = {
            "username": self.user_name,
            "password": self.password
        }
        response = requests.post(self.token_url, data=data)
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            refresh_token = tokens['refresh']
            print("Access Token: OK")
        else:
            print("Error:", response.status_code)
            print(response.json())
        return {'access_token': access_token, 'refresh_token': refresh_token}

    def __refresh(self, token_dict:dict[str, str]) -> dict[str, str]:
        data = {
            "refresh": token_dict['refrefh_token']
        }
        response = requests.post(self.token_refresh_url, data=data)
        if response.status_code == 200:
            new_access_token = response.json()['access']
            print("New Access Token:", new_access_token)
        else:
            print("Error:", response.status_code)
            print(response.json())
            self.__get_access_token()
        return token_dict.update('access_token', new_access_token)

    def request(self, url:dict, data:dict) -> any:
        jwt_token = self.__get_access_token()
        try:
            return self.__send_request(url, jwt_token['access_token'], data)
        except Exception:
            jwt_token = self.__refresh(jwt_token)
            return self.__send_request(url, jwt_token['access_token'], data)

    def __send_request(self, url:dict, access_token:str, data:dict) -> any:
        headers = {"Authorization": f"Bearer {access_token}"}
        endpoint = url['url']
        match url['method']:
            case  'get':
                response = requests.get(endpoint, data=data, headers=headers)
            case 'post':
                response = requests.post(endpoint, data=data, headers=headers)
            case 'put':
                response = requests.put(endpoint, data=data, headers=headers)
            case 'patch':
                response = requests.patch(endpoint, data=data, headers=headers)
            case 'delete':
                response = requests.delete(endpoint, data=data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("Protected Data:", data)
            return data
        else:
            print("Error:", response.status_code)
            return response.json()