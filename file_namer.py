
import os
import time
import abc

class AbstractFileNamer(abc.ABC):
    @abc.abstractmethod
    def __init__(self, recipe_name: str):
        pass
    
    def file_path(self, dir: str, extension: str):
        extension=extension.lstrip('.')
        file_name = '%s-%s.%s'%(self.recipe_name, self.time, extension)
        return os.path.join(dir, file_name) 


class FileNamer(AbstractFileNamer):
    def __init__(self, recipe_name: str):
        if not recipe_name:
            recipe_name = "unnamed"
        self.recipe_name = recipe_name
        self.time = '%i'%time.time()

class FakeFileNamer(AbstractFileNamer):
    def __init__(self):
        self.recipe_name = 'Fake recipe'
        self.time = ''
