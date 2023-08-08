#!/usr/bin/env python3
# config.py - Handles config files & handles json load/save
import os.path
import json


class Config():
    """Handles config files & handles json load/save
    Config is accessible via <configObject>.config["KEY"]
    Params:
            config_path - name of the config file to use, default to home dir
            verbose - bool, verbosity
    Methods:
        load_config
        save_config
        save_default_config
        get_path
    """

    def __init__(self, config_path: str = None, verbose: bool = False):
        """
        Configure Config object
        Params:
            config_path - name of the config file to use, default to home dir
            verbose - bool, verbosity
        """
        self.verbose: bool = verbose
        self.default_config_path: str = "./mmp/res/sampleconfig.json"

        # If config_path is defined, use it, otherwise use default path
        self.default_path = os.path.expanduser(
            "~") + "/minimacropad-config.json"
        self.path: str = config_path if config_path else self.default_path

        # Load JSON config from path, write default if nothing is found
        self.full_config: dict = self.load_config()

        # Shortcuts for accessing
        self.config = self.full_config["CONFIG"]
        self.actions = self.full_config["ACTIONS"]
        self.data = self.full_config["DATA"]
        self.serial = self.config["SERIAL"]
        self.size = self.config["SIZE"]
    # __init__

    def load_config(self) -> dict:
        """Loads JSON config from self.path
        Returns:
            dict - JSON config as a dictionary
        """
        try:
            with open(self.path, "r") as f:
                try:
                    return json.loads(f.read())
                except Exception as e:
                    msg = f"Failed to parse JSON from {self.path} config file."
                    print(msg)
                    raise e
        except FileNotFoundError:
            if self.default_path == self.path:
                self.save_default_config()
                return self.load_config()
            else:
                msg = f"Failed to find {self.path} config file. Remove this param or create the file"
                print(msg)
                raise Exception(msg)
        except Exception as e:
            print(f"Failed to load {self.path} config file.")
            raise e
    # load_config

    def save_default_config(self) -> None:
        """Saves sampleconfig.json to default (home) directory"""
        _config = None
        try:
            with open(self.default_config_path, "r") as f:
                _config = f.read()
        except FileNotFoundError:
            msg = f"Failed to find {self.default_config_path}"
            print(msg)
            raise Exception(msg)
        except Exception as e:
            print("Failed to load config file")
            print(e)
            raise e

        try:
            with open(self.path, "w") as f:
                f.write(_config)
        except Exception as e:
            print("Failed to save config file")
            print(e)
            raise e
    # save_default_config

    def save_config(self, new_config: dict = None) -> None:
        """Save self.full_config to self.path.
        Params:
            new_config - dict, if present, save that config object to the default config path.
        """
        if new_config is not None:
            self.full_config = new_config
        try:
            with open(self.path, "w") as f:
                f.write(json.dumps(self.full_config))
        except Exception as e:
            print("Failed to save config file")
            print(e)
            raise e

    def get_path(self) -> str:
        """Gets the config path
        Returns:
            str, config path
        """
        return self.path
    # get_path

# Config class
