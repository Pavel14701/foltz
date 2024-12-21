import requests

class Api:
    def __init__(self, url):
        self.base_url = url
        # Сессия для сохранения куки и CSRF токена
        self.session = requests.Session()
        self.csrf_token = self.__get_csrf_token()
        self.token_url = 'http://127.0.0.1:8000/api/token/'
        self.token_refresh_url = 'http://127.0.0.1:8000/api/token/refresh/'
        self.user_name = 'admin'
        self.password = '1234'

    def __get_csrf_token(self):
        response = self.session.get(self.base_url)
        if 'csrftoken' in response.cookies:
            return response.cookies['csrftoken']
        else:
            raise Exception("CSRF token not found")

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
            return {'access_token': access_token, 'refresh_token': refresh_token}
        else:
            print("Error:", response.status_code)
            print(response.json())
            raise Exception("Unable to get access token")

    def __refresh(self, token_dict:dict[str, str]) -> dict[str, str]:
        data = {
            "refresh": token_dict['refresh_token']
        }
        response = requests.post(self.token_refresh_url, data=data)
        if response.status_code == 200:
            new_access_token = response.json()['access']
            print("New Access Token:", new_access_token)
            token_dict['access_token'] = new_access_token
        else:
            print("Error:", response.status_code)
            print(response.json())
            return self.__get_access_token()
        return token_dict

    def request(self, query:str) -> any:
        jwt_token = self.__get_access_token()
        try:
            return self.__send_request(self.base_url, jwt_token['access_token'], query)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403 and "CSRF" in e.response.text:
                print("CSRF token expired, renewing token")
                self.csrf_token = self.__get_csrf_token()
                return self.__send_request(self.base_url, jwt_token['access_token'], query)
            elif e.response.status_code == 401:
                print("Access token expired, refreshing token")
                jwt_token = self.__refresh(jwt_token)
                return self.__send_request(self.base_url, jwt_token['access_token'], query)
            else:
                raise

    def __send_request(self, url:str, jwt_token:str, query:str):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}',  # Добавляем Bearer перед токеном
            'X-CSRFToken': self.csrf_token,
        }
        payload = {
            'query': query,
        }
        response = self.session.post(url, json=payload, headers=headers)
        # Проверка и вывод результата
        if response.status_code == 200:
            print("Response:", response.json())
            return response.json()
        else:
            print("Error:", response.status_code, response.text)
        



url = 'http://127.0.0.1:8000/api/'
query = """
    mutation {
        createBlogPost(title: "My New Post", content: "This is the content of my new post") {
        blogPost {
            id
            title
            content
        }
    }
    }
"""


graphql = Api(url)
graphql.request(query)