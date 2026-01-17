from pystickynote.paths import CONFIG_FILE, NOTES_FILE
from configparser import ConfigParser
import os

example_config = """\
[DEFAULT]
background_color = #f5f545
text_color = #0a0a0a
alpha = 0.8
border_width = 0
title_size = 24
font_size = 24
box_height = 15
box_width = 80
no_titlebar = False"""

class Config:
    def __init__(self, config_dir):
        self.config = ConfigParser()
        self.config_path = os.path.realpath(config_dir + '/' + CONFIG_FILE)
        self.notes_path = os.path.realpath(config_dir + '/' + NOTES_FILE)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as file:
                file.write(example_config)
        if not os.path.exists(self.notes_path):
            with open(self.notes_path, 'w') as file:
                file.write('{}')
        self.config.read(self.config_path)
        self.config_dict = self.config['DEFAULT']
        self.background_color = self.config_dict['background_color']
        self.text_color = self.config_dict['text_color']
        self.alpha = self.config_dict['alpha']
        self.border_width = self.config_dict['border_width']
        self.font_size = self.config_dict['font_size']
        self.title_size = self.config_dict['title_size']
        try:
            self.height = self.config_dict['box_height']
            self.width = self.config_dict['box_width']
            self.no_titlebar = self.config_dict['no_titlebar'] == "True"
        except KeyError:
            self.config['DEFAULT']['box_height'] = '5'
            self.config['DEFAULT']['box_width'] = '50'
            self.config['DEFAULT']['no_titlebar'] = "False"
            with open(self.config_path, 'w') as config_file:
                self.config.write(config_file)
            self.height = self.config_dict['box_height']
            self.width = self.config_dict['box_width']
            self.no_titlebar = self.config_dict['no_titlebar'] == "True"