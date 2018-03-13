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
        self.subcmd = args.SUBCMD

    def run(self):
        """
        Method to call the appropriate method from api module
        :return: None
        """
        if self.subcmd == 'create':
            create(self.name, self.dcctype, self.path,
                   self.template_folder_path)
        elif self.subcmd == 'delete':
            delete(self.name, self.dcctype, self.path)
        elif self.subcmd == 'list':
            list_projects(self.dcctype, self.path)
        elif self.subcmd == 'types':
            list_types(self.template_folder_path)
        elif self.subcmd == 'describe':
            describe(self.name, self.path)
        else:
            print "Insufficient/Invalid arguments, please provide options " \
                  "to execute"
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

    parser.add_argument('-t', '--type', help='The type of the project created '
                                             'from a specific template')

    parser.add_argument('SUBCMD', help='list: List the project which have been '
                                       'created, optionally restricting the '
                                       'list to a specific type or types by '
                                       'passing specific type or comma '
                                       'separated type value.\n'
                                       'create: Create a new project at the '
                                       'provided path, use PROJMAN_LOCATION env'
                                       'variable to override else default '
                                       'projects path will be used.\n'
                                       'delete: Delete an existing project, '
                                       'optionally restrict to a particular'
                                       ' type within project tree.\n'
                                       'types: List the type of project which '
                                       'may be created.\n'
                                       'describe: Print the structure of a '
                                       'project template.',
                        choices=['list', 'create', 'delete', 'types',
                                 'describe'])

    parser.add_argument('name', help='The name of the project to create, delete'
                                     ' or run types on.', nargs='?')

    args = parser.parse_args()
    cli = CLI(args)
    cli.run()