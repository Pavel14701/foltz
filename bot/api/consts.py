from common.config_check import Configs

class ApiUrls:
    base_url:str = Configs().check_env_var('SITE_BASE_URL')
    blog:str = 'blog/'
    service:str = 'service/'
    product:str = 'product/'
    token:str = 'api/token/'
    token_refresh:str = 'api/token/refresh/'

    # Работает с моделями Blog, Service, Product
    def get_objects_list(self, _object:str) -> dict[str, str]:
        return {'method': 'get', 'url': f'{self.base_url}{_object}api/list/'}

    def create_object(self, _object:str) -> dict[str, str]:
        return {'method': 'post', 'url':f'{self.base_url}{_object}api/create/'}

    def get_object_details(self, _object:str, pk:int) -> dict[str, str]:
        return {'method': 'get', 'url': f'{self.base_url}{_object}api/{pk}'}

    def update_object(self, _object:str, object_id:int) -> dict[str, str]:
        return {'method': 'put', 'url': f'{self.base_url}{_object}api/{object_id}/update/'}

    def parcial_object_update(self, _object:str, pk:int) -> dict[str, str]:
        return {'method': 'patch', 'url': f'{self.base_url}{_object}api/{pk}/partial_update/'}

    def del_object(self, _object:str, pk:int) -> dict[str, str]:
        return {'method': 'delete', 'url': f'{self.base_url}{_object}api/{pk}/delete'}


    # Работает с секциями постов, продуков, услуг
    def get_object_sections(self, _object:str, pk:int) -> dict[str, str]:
        return {'method': 'get', 'url': f'{self.base_url}{_object}api/{pk}/sections/'}

    def get_object_section_info(self, _object:str, pk:int, section_id:int) -> dict[str, str]:
        return {'method': 'get', 'url': f'{self.base_url}{_object}api/{pk}/sections/{section_id}/'}

    def update_object_section_info(self, _object:str, pk:int, section_id:int) -> dict[str, str]:
        return {'method': 'put', 'url': f'{self.base_url}{_object}api/{pk}/sections/{section_id}/update'}

    def par_update_object_section_info(self, _object:str, pk:int, section_id:int) -> dict[str, str]:
        return {'method': 'patch', 'url': f'{self.base_url}{_object}api/{pk}/sections/{section_id}/parcial_update'}

    def delete_object_section(self, _object:str, pk:int, section_id:int) -> dict[str, str]:
        return {'method': 'delete', 'url': f'{self.base_url}{_object}api/{pk}/sections/{section_id}/delete'}

    def move_object_section(self, _object:str, pk:int, section_id:int) -> dict[str, str]:
        return {'method': 'post', 'url': f'{self.base_url}{_object}api/{pk}/sections/{section_id}/move'}

    def create_object_section(self, _object:str, pk:int) -> dict[str, str]:
        return {'method': 'post', 'url': f'{self.base_url}{_object}api/{pk}/sections/create/'}