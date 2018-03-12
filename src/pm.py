#!/usr/bin/env python

import argparse
import os
import sys
from projman import create, delete, list_projects, list_types, describe


class CLI:
    """
    CLI class
    """
    def __init__(self, args):
        """
        Initialisation of instance variables
        :param args: arguments passed through command
        """
        self.dcctype = args.type
        # Getting relative level from the project root 'projman'
        level = os.getcwd().split('/projman')[1].count(os.sep)
        if args.path:
            self.path = args.path
        elif os.getenv('PROJMAN_LOCATION'):
            self.path = os.getenv('PROJMAN_LOCATION')
        else:
            self.path = os.path.join('../' * level, 'projects')
        self.name = args.name
        self.template_folder_path = os.getenv('PROJMAN_TEMPLATES')
        if not self.template_folder_path:
            self.template_folder_path = os.path.join('../' * level, 'templates')
        self.create = args.create
        self.delete = args.delete
        self.list = args.list
        self.types = args.types
        self.describe = args.describe
        self.force = args.forceful

    def run(self):
        """
        Method to call the appropriate method from api module
        :return: None
        """
        if self.create:
            create(self.name, self.dcctype, self.path,
                   self.template_folder_path)
        elif self.delete:
            delete(self.name, self.dcctype, self.path, self.force)
        elif self.list:
            list_projects(self.dcctype, self.path)
        elif self.types:
            list_types(self.template_folder_path)
        elif self.describe:
            describe(self.name, self.path)
        else:
            print "Insufficient arguments, please provide options to execute"
            sys.exit(4)

if __name__ == '__main__':
    HELP_STR = """
        Tool for artists to do various operations for the project, starting 
        from creation to deletion
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, description=HELP_STR)

    parser.add_argument('-p', '--path', help='The base path in which to create '
                                             'the project. If not supplied, '
                                             'it uses a default project path '
                                             'from PROJMAN_LOCATION')

    parser.add_argument('-name', '--name', help='The name of the project to'
                                                ' create, delete or run types'
                                                ' on.')

    parser.add_argument('-t', '--type', help='The type of the project created '
                                             'from a specific template')

    parser.add_argument('--list', help='List the project which have been '
                                       'created, optionally restricting the '
                                       'list to a specific type or types by '
                                       'passing spcific type or comma '
                                       'separated type value',
                        action='store_true')

    parser.add_argument('--create', help='Create a new project at the '
                                         'provided path, use PROJMAN_LOCATION'
                                         ' env variable to override else '
                                         'default projects path will be used',
                        action='store_true')

    parser.add_argument('--delete', help='Delete an existing project, '
                                         'optionally restrict to a particular'
                                         ' type within project tree',
                        action='store_true')

    parser.add_argument('-f', '--forceful', help='To be used for force delete ',
                        action='store_true')

    parser.add_argument('--types', help='List the type of project which may be '
                                        'created', action='store_true')

    parser.add_argument('--describe', help='Print the structure of a project '
                                           'template', action='store_true')

    args = parser.parse_args()
    cli = CLI(args)
    cli.run()