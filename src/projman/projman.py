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
        with open(template_path) as stream:
            config = yaml.safe_load(stream)
        if config:
            if dcc_type:
                dcc_type_list = [dcc for dcc in dcc_type.split(',') if dcc]
                for dcc_types in dcc_type_list:
                    create_config = [project_types for project_types in config if
                                     dcc_types in project_types['value']]
                    if create_config:
                        path = os.path.join(path, name)
                        if not os.path.exists(path):
                            os.mkdir(path)
                        path = os.path.join(path, dcc_types)
                        parent_mode = create_config[0]['permission']
                        if not os.path.exists(path):
                            os.mkdir(path, int(parent_mode, 8))
                        # subprocess.call(['chmod', parent_mode, path])
                        _create(create_config[0]['value'][dcc_types], path,
                                parent_mode)
                    else:
                        print 'Type {} does not exist in template'.format(
                            dcc_type)
                        sys.exit(4)
            else:
                print 'Please provide dcctype'
                sys.exit(4)
    except IOError as ie:
        print ie
        sys.exit(4)
    except OSError as e:
        print e
        sys.exit(4)


def listing_project(path):
    """
    Method to list the project types
    :param path: Path of the project folder
    :return: None
    """
    _no_path_exists(path)
    try:
        for dirs in os.listdir(path):
            for type_dirs in os.listdir(os.path.join(path, dirs)):
                print type_dirs
    except OSError as e:
        print e
        sys.exit(4)


def listing_types(dcc_type, path):
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
                print dirs
        else:
            dcc_types = [dcc for dcc in dcc_type.split(',') if dcc]
            for dirs in os.listdir(path):
                for type_dirs in os.listdir(os.path.join(path, dirs)):
                    if type_dirs in dcc_types:
                        print dirs
    except OSError as e:
        print e
        sys.exit(4)


def delete(name, dcc_type, path, force):
    """
    Method for deletion of project, optionally deletes on basis of type
    :param name: Name of the project
    :param dcc_type: Type of the project
    :param path: Path for the project folder
    :param force: forceful deletion
    :return: None
    """
    if not name:
        print 'Please provide name of the project for delete operation'
        sys.exit(4)
    path = os.path.join(path, name)
    _no_path_exists(path)
    try:
        if not dcc_type:
            if force:
                shutil.rmtree(path, ignore_errors=True)
            else:
                os.rmdir(path)
        else:
            dcc_type_list = [dcc for dcc in dcc_type.split(',') if dcc]
            for dcc_types in dcc_type_list:
                path = os.path.join(path, dcc_types)
                if not os.path.exists(path):
                    print 'DCC type {} does not exist'.format(dcc_types)
                    sys.exit(4)
                else:
                    if force:
                        shutil.rmtree(path, ignore_errors=True)
                    else:
                        os.rmdir(path)
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
                os.mkdir(new_path, int(new_parent_mode, 8))
        elif type(sub['value']) == dict:
            for key in sub['value']:
                modify_path = os.path.join(path, key)
                modify_parent_mode = sub.get('permission', parent_mode)
                if not os.path.exists(modify_path):
                    os.mkdir(modify_path, int(modify_parent_mode, 8))
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