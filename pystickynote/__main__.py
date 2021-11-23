from .core import create_note, delete_note, open_note, list_notes
from .config import Config
from .paths import PATH_DIR
import json
from argparse import ArgumentParser
from uuid import uuid4

new_id = str(uuid4())

def main():
    parser = ArgumentParser(usage='pystickynote <open/create/list> <name/all>')
    parser.add_argument('action', choices=['open', 'create', 'delete', 'list'], help='Choose action to take.')
    parser.add_argument('name', help='Stickynote\'s name to save to', nargs='?', default=new_id)
    parser.add_argument('-c', '--config_dir', help='set path to config folder [%(default)s]', default=PATH_DIR)
    args = parser.parse_args()
    config = Config(args.config_dir)
    if args.action == 'create':
        if args.name == new_id:
            print('Please Provide A Name for Your Note.')
        else:
            with open(config.notes_path, 'r+') as json_file:
                obj = json.load(json_file)
                for k, v in obj.items():
                    if args.name == k:
                        print('Note with that name found, please use the open command to edit/delete.')
                        exit(1)
            create_note(args.name, config)
    elif args.action == 'delete':
        if args.name == new_id:
            print('Please Provide The Name of The Note.')
        else:
            delete_note(args.name)
    elif args.action == 'open':
        if args.name == new_id:
            print('Please Provide The Name of The Note.')
        else:
            open_note(args.name, config)
    elif args.action == 'list':
        list_notes()
    exit(0)

if __name__ == "__main__":
    main()