from restclient import BaseClient
from time import time
import os

class Notebooks():
    def __init__(self, useremail, userpassword):
        self.cl = BaseClient(useremail = useremail,
                             userpassword = userpassword)
        
    def get_notebooks(self, modbefore=None, moafter=None, id=None, start=None, num=None):
        notebooks, method = self.cl.get(baseurl = 'http://api.toodledo.com/2/notebooks/get.php',
                                        ssl = True)
        
        return notebooks, method
    
    def add_notebooks(self, data):
        notebooks, method = self.client.post(protocol = 'http',
                                             hostname = 'api.toodledo.com',
                                             resource = '/2/notebooks/add.php',
                                             body = data)
        
        return notebooks, method
        
if __name__ == '__main__':
    
    nb = Notebooks(useremail = 'me@ex.com',
                   userpassword = '123qwe')
    get_notebooks, method = nb.get_notebooks()
    print get_notebooks, method

    #add_notebooks, method = nb.add_notebooks(data = {'notebooks': [{"title":"My newIdeas"}],
                           #                                   'f': 'xml'})
    #print add_notebooks, method
    
    #add_notebooks, method = Notebooks().add_notebooks(data = 'notebooks=[{"title": "My newIdeas"}]&key=ccef29cffce17d21c24623eb0c77b22d')
    #print add_notebooks, method