import json
import os
import sys
import logging
import re
import pybase64
import yaml
import base64

from .secret_store import AbstractSecretStore, SecretsStoreException
from itertools import cycle
from ...misc import run_cmd

from .keystore import PasswordProtectedKeystoreWithHMAC

from base64 import urlsafe_b64encode


class LocalSecretStore(AbstractSecretStore):
    """
    A class representing a local secret store for managing secrets.

    Attributes:
        store_name (str): Name of the secret store.
        store_priority (int): Priority of the secret store.
        root_store_path (str): Root path where the local secret store is stored.
        application_settings (Settings): An instance of Settings providing application settings.
        app_short_name (str): Short name of the application.
        password (str): Password for the local secret store.

    Methods:
        __init__(store_name, store_priority, root_store_path, application_settings, app_short_name, password=None): Constructor to initialize the LocalSecretStore.
        __initialise_secrets_store(password): Initialize the secrets store if it doesn't exist.
        __guid(): Generate a unique identifier based on the machine and store path.
        get_secret(key, default_value=None): Retrieve a secret from the local secret store.
        set_secret(key, value): Set a secret in the local secret store.
        delete_secret(key): Delete a secret from the local secret store.
        __save(): Save the changes made to the local secret store.
    """

    def __init__(self, store_name, store_priority, root_store_path, application_settings, app_short_name,
                 password: str = os.getenv('SECRETS_STORE_PASSWORD', None)) -> None:
        """
        Initialize the LocalSecretStore.

        Args:
            store_name (str): Name of the secret store.
            store_priority (int): Priority of the secret store.
            root_store_path (str): Root path where the local secret store is stored.
            application_settings (Settings): An instance of Settings providing application settings.
            app_short_name (str): Short name of the application.
            password (str): Password for the local secret store (default: None).
        """
        super().__init__(store_name, 'local', store_priority, application_settings)
        if os.path.exists(os.path.join(root_store_path, f"{app_short_name}.keystore")):
            logging.warning(f'Old Keystore file "{os.path.join(root_store_path, f"{app_short_name}.keystore")}" is no longer supported.')
        self.store_path = os.path.join(root_store_path, f"{app_short_name}.v2keystore")

        # If password is not provided, generate a unique password
        if password is None:
            password = self.__guid()

        try:
            # Try to load the existing store
            self.store = PasswordProtectedKeystoreWithHMAC(self.store_path, password)
            self.store_available = True
            self.store_read_only = not self.__is_writeable()
            logging.info(f'Successfully opened Secrets Store: {self.store_path}')
            self.__check_auto_imports(root_store_path)
        except Exception as ex:
            raise SecretsStoreException(f'Failed to open Secrets Store: {self.store_path}. Error: {str(ex)}')

    def __check_auto_imports(self, root_store_path):
        auto_yaml = os.path.join(root_store_path, 'secrets.yaml')
        if os.path.exists(auto_yaml):
            print(f'Performing Auto-Import of Secrets from {auto_yaml}')
            with open(auto_yaml, 'r', encoding='UTF-8') as auto_yaml_file:
                secrets = yaml.safe_load(auto_yaml_file)
                for entry in secrets['secrets']:
                    name = entry.get('name')
                    value = entry.get('value')
                    secret_file = entry.get('file')
                    store_as = entry.get('store_as')

                    if secret_file is not None:
                        if os.path.exists(secret_file):
                            if store_as == 'raw':
                                with open(secret_file, 'r') as file:
                                    file_content = file.read()
                                value = file_content
                            elif store_as == 'base64':
                                with open(secret_file, 'rb') as file:
                                    file_content = file.read()
                                value = base64.b64encode(file_content).decode('utf-8')
                            else:
                                print(f'Unsupported "store_as" value of {store_as} for {name}', file=sys.stderr)
                        else:
                            print(f'The file "{secret_file}" specified for {name} does not exist', file=sys.stderr)

                    if value is not None:
                        self.set_secret(name, value)
                        print(f'Imported Secret: {name}')
                    else:
                        print(f'Missing "value" for {name}. Not imported.', file=sys.stderr)

            os.remove(auto_yaml)

    def __guid(self):
        """
        Generate a unique identifier based on the machine and store path.

        Returns:
            Unique identifier.
        """
        base = None
        # Determine machine ID based on the platform
        if sys.platform == 'darwin':
            base = run_cmd(
                "ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'")

        if sys.platform == 'win32' or sys.platform == 'cygwin' or sys.platform == 'msys':
            base = run_cmd('wmic csproduct get uuid').split('\n')[2] \
                .strip()

        if sys.platform.startswith('linux'):
            base = run_cmd('cat /var/lib/dbus/machine-id') or \
                   run_cmd('cat /etc/machine-id')

        if sys.platform.startswith('openbsd') or sys.platform.startswith('freebsd'):
            base = run_cmd('cat /etc/hostid') or \
                   run_cmd('kenv -q smbios.system.uuid')

        if not base:
            raise SecretsStoreException("Failed to determined unique machine ID")

        base += self.store_path
        key = re.sub("[^a-zA-Z]+", "", base)
        xored = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(base, cycle(key)))
        return urlsafe_b64encode(pybase64.b64encode_as_string(xored.encode())[:32].encode()).decode()

    def get_secret(self, key, default_value=None):
        """
        Retrieve a secret from the local secret store.

        Args:
            key (str): Key of the secret.
            default_value: Default value to return if the secret is not found.

        Returns:
            Secret value if found, else default_value.
        """
        entry = self.store.get(key=key)
        if not entry or entry == 'NONE':
            return default_value

        return entry

    def set_persistent_setting(self, key, value):
        if self.get_secret(key):
            self.delete_secret(key)

        self.store.set(key=key, value=value)


    def set_secret(self, key, value):
        """
        Set a secret in the local secret store.

        Args:
            key (str): Key of the secret.
            value: Value of the secret.
        """
        if self.get_secret(key):
            self.delete_secret(key)

        self.store.set(key=key, value=value)
        index = self.get_index()
        if key not in index:
            index.append(key)
        self.__set_index(index)

    def delete_secret(self, key):
        """
        Delete a secret from the local secret store.

        Args:
            key (str): Key of the secret.
        """
        self.store.delete(key=key)
        index = self.get_index()
        while key in index:
            index.remove(key)
        self.__set_index(index)

    def __set_index(self, index: list):
        self.store.set(key=f'{self.store_name}.INDEX', value=json.dumps(index))

    def get_index(self) -> list:
        index = self.get_secret(f'{self.store_name}.INDEX', None)
        if index is None:
            self.__set_index([])
            return []

        return json.loads(index)

    def __is_writeable(self):
        try:
            self.store.set('sstore_save', 'true')
            self.store.delete('sstore_save')
            return True
        except Exception as ex:
            logging.warning(str(ex))
            return False
