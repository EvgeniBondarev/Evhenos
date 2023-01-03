import requests
import json


class Telegraph(object):
    """docstring for Telegraph"""
    def __init__(self):
        super(Telegraph, self).__init__()

        if self.__get_config()['ok'] == True:
            data = self.__get_config()['result']
            
            self.token = data["access_token"]
            self.author_name = data['author_name']
            self.author_url = data['author_url']

        else:
            self.__registr()

    def __str__(self) -> str:
        return f'Token: {self.token}\nAuthor name: {self.author_name}\nAuthor URL: {self.author_url}'
        
    def __registr(self):
        """Use this method to create a new Telegraph account"""
        self.short_name = input("Short name: ")
        self.author_name = input("Author Name: ")
        self.author_url = input("Author URL (not necessary): ")

        data={
            'short_name':self.short_name, 
            'author_name':self.author_name,
            'author_url':self.author_url
        }

        result=requests.get("https://api.telegra.ph/createAccount?", params=data).json()
        print(result)

        with open('config.json', 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file, ensure_ascii=False, indent=4)

    def __get_config(self) -> json:
        try:
            with open('config.json') as f:
                user_content = json.load(f)
            return(user_content)
        except FileNotFoundError:
            self.__registr()

   
    # main methods
    
    def create_page(self, title: str, data_page: json) -> str:
        data={
            'access_token': self.token,
            'title': title,
            'author_name': self.author_name,
            'content': data_page,
            'return_content':'false'
        }
        
        page=requests.get("https://api.telegra.ph/createPage?", params=data)
        print(page.json())
        #return page.json()
    
    
    




    
