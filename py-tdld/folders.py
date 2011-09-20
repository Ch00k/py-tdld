from restclient import RESTClient
import os

class Folders():
    
    def add_folders(self, data):
        folders, method = RESTClient().httprequest(protocol = 'http',
                                                     hostname = 'api.toodledo.com',
                                                     resource = '/2/folders/add.php',
                                                     url_params = {
                                                                   'key': open(os.path.expanduser('~/.tdld/state')).read(),
                                                                   #'name': 'folder1'
                                                                   },
                                                     body = data)
        
        return folders, method
    
if __name__ == '__main__':

    add_folders, method = Folders().add_folders(data = ['key': '2ce76378dcdf3dfa3d34c589920cece5',
                                                        'folders': {'name': 'new test folder 1'}])
    print add_folders, method