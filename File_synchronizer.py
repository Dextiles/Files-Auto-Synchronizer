from os import walk
from hashlib import sha256


class Synchronizer:
    def __init__(self, service, directory):
        self.__cloud_service = service
        self.__file_directory = directory

    def __get_files_on_system(self):
        data = dict()
        for path_directory, _, filenames in walk(self.__file_directory):
            for filename in filenames:
                filepath = path_directory + '/' + filename
                with open(filepath, 'rb') as file_object:
                    data.setdefault(f'{filename}', {'sha256': sha256(file_object.read()).hexdigest(),
                                                    'path': filepath})
        return data

    def synchronise(self):
        service_data = self.__cloud_service.get_info()
        local_data = self.__get_files_on_system()
        for local_file, local_elem in local_data.items():
            if local_file not in service_data.keys():
                self.__cloud_service.load(local_elem['path'], local_file)
            elif local_file in service_data.keys():
                if local_elem['sha256'] != service_data[local_file]['sha256']:
                    self.__cloud_service.reload(local_elem['path'], local_file)
        for service_file, service_elem in service_data.items():
            if service_file not in local_data.keys():
                self.__cloud_service.delete(service_file)
