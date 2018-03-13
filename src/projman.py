import yaml
import os
import sys
import shutil


def create(name, dcc_type, path, template_path):
    """
    Method for creation of project
    :param name: Name of the project
    :param dcc_type: Type of the project
    :param path: Path of the project folder
    :param template_path: Path for the template folder
    :return: None
    """
    if not name:
        print 'Please provide the name for the project'
        sys.exit(4)
    if not os.path.exists(path):
        print 'Path {} does not exist, creating it....'.format(path)
        os.mkdir(path)
    try:
        if dcc_type:
            dcc_type_first = dcc_type.split(',')[0]
            create_config = _load_config(template_path, dcc_type_first)
            if create_config:
                path = os.path.join(path, name)
                if not os.path.exists(path):
                    os.mkdir(path)
                else:
                    print 'Path {} already exists'.format(path)
                path = os.path.join(path, dcc_type_first)
                parent_mode = create_config[0]['permission']
                if not os.path.exists(path):
                    os.mkdir(path, int(parent_mode, 8))
                else:
                    print 'Path {} already exists'.format(path)
                _create(create_config[0]['value'][dcc_type_first], path,
                        parent_mode)
            else:
                print 'Type {} does not exist'.format(dcc_type_first)
        else:
            print 'Please provide dcctype'
            sys.exit(4)
    except IOError as ie:
        print ie
        sys.exit(4)
    except OSError as e:
        print e
        sys.exit(4)


def list_types(template_path):
    """
    Method to list the project types
    :param path: Path of the project folder
    :return: None
    """
    try:
        types = _load_config(template_path)
        if types:
            for project_types in list(set(types)):
                print project_types
        else:
            sys.exit(4)
    except OSError as e:
        print e
        sys.exit(4)


def list_projects(dcc_type, path):
    """
    Method to list the project, optionally on basis of types
    :param dcc_type: Type of the project, can be comma separated
    :param path: Path for the project folder
    :return: None
    """
    _no_path_exists(path)
    try:
        if not dcc_type:
            for dirs in os.listdir(path):
                print os.path.join(path, dirs)
        else:
            dcc_types = [dcc for dcc in dcc_type.split(',') if dcc]
            for dirs in os.listdir(path):
                full_path = os.path.join(path, dirs)
                for type_dirs in os.listdir(full_path):
                    if type_dirs in dcc_types:
                        print '{} is present in {}'.format(type_dirs, full_path)
    except OSError as e:
        print e
        sys.exit(4)


def delete(name, dcc_type, path):
    """
    Method for deletion of project, optionally deletes on basis of type
    :param name: Name of the project
    :param dcc_type: Type of the project
    :param path: Path for the project folder
    :return: None
    """
    if not name:
        print 'Please provide name of the project for delete operation'
        sys.exit(4)
    path = os.path.join(path, name)
    _no_path_exists(path)
    try:
        if not dcc_type:
            shutil.rmtree(path, ignore_errors=True)
        else:
            dcc_type_list = [dcc for dcc in dcc_type.split(',') if dcc]
            for dcc_types in dcc_type_list:
                type_path = os.path.join(path, dcc_types)
                if not os.path.exists(type_path):
                    print 'DCC type {} does not exist'.format(dcc_types)
                    sys.exit(4)
                else:
                    if len(os.listdir(path)) == 1:
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        shutil.rmtree(type_path, ignore_errors=True)
    except OSError as e:
        print e
        sys.exit(4)


def describe(name, path):
    """
    Method to describe the project structure
    :param name: Name of the project
    :param path: Path for the project folder
    :return: None
    """
    if not name:
        print 'Please provide name of the project for describe operation'
        sys.exit(4)
    path = os.path.join(path, name)
    _no_path_exists(path)
    try:
        for root,dirs,files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 4 * level
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))
    except OSError as e:
        print e
        sys.exit(4)


def _create(typdict, path, parent_mode):
    """
    Helper method for creation of project
    :param typdict: list of dict values containing value and permission
    :param path: Path for the project folder
    :param parent_mode: Permission for the directory
    :return: None
    """
    for sub in typdict:
        if type(sub['value']) == str:
            new_path = os.path.join(path, sub['value'])
            new_parent_mode = sub.get('permission', parent_mode)
            if not os.path.exists(new_path):
                if '.' in sub['value']:
                    open(new_path, 'w').close()
                else:
                    os.mkdir(new_path)
                os.chmod(new_path, int(new_parent_mode, 8))
            else:
                print 'Path {} already exists'.format(new_path)
        elif type(sub['value']) == dict:
            for key in sub['value']:
                modify_path = os.path.join(path, key)
                modify_parent_mode = sub.get('permission', parent_mode)
                if not os.path.exists(modify_path):
                    if '.' in key:
                        open(modify_path, 'w').close()
                    else:
                        os.mkdir(modify_path)
                    os.chmod(modify_path, int(modify_parent_mode, 8))
                else:
                    print 'Path {} already exists'.format(modify_path)
                if type(sub['value'][key]) == list:
                    _create(sub['value'][key], modify_path, modify_parent_mode)


def _no_path_exists(path):
    """
    Helper method for checking the existence of path
    :param path: Path for the project folder
    :return: None
    """
    if not os.path.exists(path):
        print 'Path does not exist'
        sys.exit(4)


def _load_config(template_path, dcc_type=None):
    types = []
    template_folder_paths = [template_paths for template_paths in
                             template_path.split(':') if template_paths]
    for paths in template_folder_paths:
        if os.path.exists(paths):
            for config_file in os.listdir(paths):
                config_path = os.path.join(paths, config_file)
                if os.path.isfile(config_path) and \
                        config_file.endswith('.yaml'):
                    with open(config_path) as stream:
                        config = yaml.safe_load(stream)
                    if config:
                        try:
                            if dcc_type:
                                create_config = [project_types for
                                                 project_types in config if
                                                 dcc_type in
                                                 project_types['value']]
                                if create_config:
                                    return create_config
                            else:
                                [types.extend(typekeys) for typekeys in [
                                    project_types['value'].keys() for
                                                 project_types in config]]
                        except:
                            print "Invalid yaml file"
                            sys.exit(4)
                    else:
                        print 'Empty yaml file'
                        sys.exit(4)
                else:
                    print 'File {} is not a yaml file'.format(config_path)
        else:
            print 'Folder path {} does not exist'.format(paths)
    if types:
        return types