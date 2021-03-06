import os


class FileSystemError(Exception):
    ''' Class for errors in filesystem module '''
    pass


class FSItem(object):
    ''' Common class for OS items OS: Files and Directories '''

    def __init__(self, path):
        ''' Creates new FSItem instance by given path to file '''
        self.path = path
        self.name = os.path.split(path)[1]
        
    def rename(self, newname):
        ''' Renames current item
                raise FileSystemError if item does not exist
                raise FileSystemError if item "newname" already exists '''
        if os.path.exists(self.path) and self.name != newname:
            if os.path.exists(os.path.join(self.path, newname)) == False:
                new_path = os.path.join(os.path.split(self.path)[0], newname)
                os.rename(self.path, new_path)
                self.path = new_path
                self.name = os.path.split(new_path)[1]
            else:
                raise FileSystemError(
                "Can't rename file: {0} already exist".format(os.path.join(self.path, newname)))
        else:
            raise FileSystemError(
                "Can't rename file: {0} already exist".format(newname))

    def getname(self):
        ''' Returns name of current item '''
        return self.name

    def get_path_name(self):
        return self.path

    def isfile(self):
        ''' Returns True if current item exists and current item is file, False otherwise '''
        return os.path.isfile(self.path)

    def isdirectory(self):
        ''' Returns True if current item exists and current item is directory, False otherwise '''
        return os.path.isdir(self.path)


class File(FSItem):
    ''' Class for working with files '''

    def __init__(self, path):
        ''' Creates new File instance by given path to file
                raise FileSystemError if there exists directory with the same path '''
        if os.path.isdir(path):
            raise FileSystemError(
                "Can't create file: {0} already exist".format(self.getname()))
        else:
            self.path = path
            self.name = os.path.split(path)[1]

    def __len__(self):
        ''' Returns size of file in bytes
                raise FileSystemError if file does not exist '''
        if os.path.isfile(self.path) and os.path.exists(self.path):
            return os.stat(self.path).st_size
        else:
            raise FileSystemError(
                "Can't show size: file {0} does not exist".format(self.get_path_name()))
    def create(self):
        ''' Creates new item in OS
            raise FileSystemError if item with such path already exists '''
        if os.path.exists(self.path):
            raise FileSystemError("{0} already exists".
                                  format(self.path))
        else:
            with open(self.path, 'a'):
                pass

    def getcontent(self):
        ''' Returns list of lines in file (without trailing end-of-line)
                raise FileSystemError if file does not exist '''
        if os.path.isfile(self.path) and os.path.exists(self.path):
            with open(self.path, 'r') as file:
                return ([line.rstrip() for line in file])
        else:
            raise FileSystemError(
                "Can't show content: file {0} does not exist".format(self.get_path_name()))

    def __iter__(self):
        ''' Returns iterator for lines of this file
                raise FileSystemError if file does not exist '''
        with open(self.path, 'r') as file:
            return iter(list(map(lambda line: line.rstrip(), file)))


class Directory(FSItem):
    ''' Class for working with directories '''

    def __init__(self, path):
        ''' Creates new Directory instance by given path
                raise FileSystemError if there exists file with the same path '''
        if os.path.isfile(path):
            raise FileSystemError(
                "Can't create directory: {0} is file".format(self.get_path_name()))
        else:
            self.path = path
            self.name = os.path.split(path)[1]

    def items(self):
        ''' Yields FSItem instances of items inside of current directory
                raise FileSystemError if current directory does not exists '''
        if os.path.exists(self.path) == False:
            raise FileSystemError(
                "Can't show instances inside of directory: {0} do not exist".format(self.get_path_name()))
        else:
            for file in os.listdir(self.path):
                if os.path.isfile(os.path.join(self.path, file)):
                    yield File(os.path.join(self.path, file))
                else:
                    if os.path.isdir(os.path.join(self.path, file)):
                        yield Directory(os.path.join(self.path, file))



    def files(self):
        ''' Yields File instances of files inside of current directory
                raise FileSystemError if current directory does not exists '''
        if os.path.exists(self.path) == False and isdirectory(self.path) == False:
            raise FileSystemError()
        else:
            for file in filter(lambda file: os.path.isfile(os.path.join(self.path, file)), list(os.listdir(self.path))):
                yield File(os.path.join(self.path, file))

    def subdirectories(self):
        ''' Yields Directory instances of directories inside of current directory
                raise FileSystemError if current directory does not exists '''
        if os.path.exists(self.path) == False:
            raise FileSystemError()
        else:
            for directory in filter(lambda file: os.path.isdir(os.path.join(self.path, file)), list(os.listdir(self.path))):
                yield Directory(os.path.join(self.path, directory))

    def filesrecursive(self):
        ''' Yields File instances of files inside of this directory,
                inside of subdirectories of this directory and so on...
                raise FileSystemError if directory does not exist '''
        try:
            for file in os.listdir(self.path):
                if os.path.isfile(os.path.join(self.path, file)):
                    yield File(os.path.join(self.path, file))
                else:
                    for subitem in Directory(os.path.join(self.path, file)).filesrecursive():
                        yield subitem
        except FileNotFoundError:
            raise FileSystemError('Path {} not found'.format({self.path}))

    def create(self):
        ''' Creates new item in OS
            raise FileSystemError if item with such path already exists '''
        if os.path.exists(self.path):
            raise FileSystemError("{0} already exists".
                                  format(self.path))
        else:
            os.makedirs(self.path)

    def getsubdirectory(self, name):
        ''' Returns Directory instance with subdirectory of current directory with name "name"
                raise FileSystemError if item "name" already exists and item "name" is not directory '''
        if os.path.exists(os.path.join(self.path, name)) and \
                not os.path.isdir(os.path.join(self.path, name)):
            raise FileSystemError("{0} Item exists and is not directory".
                                  format(os.path.join(self.path, name)))
        else:
            return Directory(os.path.join(self.path, name))
