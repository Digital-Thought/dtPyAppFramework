import logging
from ...paths import ApplicationPaths
from ...decorators import singleton
from .local_secret_store import LocalSecretStore
from .aws_secret_store import AWSSecretsStore
from .azure_secret_store import AzureSecretsStore


@singleton()
class SecretsManager(object):
    """
    A singleton class responsible for managing secrets across different secret stores.

    Attributes:
        application_paths (ApplicationPaths): An instance of ApplicationPaths providing paths for secret stores.
        application_settings (Settings): An instance of Settings providing application settings.
        stores (list): A list to hold different secret stores.
    """

    def __init__(self, application_paths=None, application_settings=None, cloud_session_manager=None) -> None:
        """
        Initialize the SecretsManager.

        Args:
            application_paths (ApplicationPaths): An instance of ApplicationPaths providing paths for secret stores.
            application_settings (Settings): An instance of Settings providing application settings.
        """
        super().__init__()
        self.application_paths = application_paths
        self.application_settings = application_settings
        self.cloud_session_manager = cloud_session_manager
        self.stores = []
        self.store_names = []

        if not self.application_paths:
            self.application_paths = ApplicationPaths()

        # Add local user secret store
        self.stores.append(LocalSecretStore(store_name="User_Local_Store",
                                            store_priority=-0,
                                            root_store_path=self.application_paths.usr_data_root_path,
                                            application_settings=self.application_settings,
                                            app_short_name=self.application_paths.app_short_name))

        try:
            # Add local app secret store (if it exists)
            self.stores.append(LocalSecretStore(store_name="App_Local_Store",
                                                store_priority=1,
                                                root_store_path=self.application_paths.app_data_root_path,
                                                application_settings=self.application_settings,
                                                app_short_name=self.application_paths.app_short_name))
        except Exception as ex:
            print(f'Skipping APP Local Secret Store. {ex}')

        # Sort stores based on priority
        self._sort_stores()

    def get_local_stores_index(self):
        _index = {"User_Local_Store": {}, "App_Local_Store": {}}
        for key in _index:
            store: LocalSecretStore = self.get_store(key)
            try:
                _index[key]['available'] = store.store_available
                _index[key]['index'] = store.get_index()
                _index[key]['read_only'] = store.store_read_only
            except Exception as ex:
                logging.error(str(ex))
                _index[key]['available'] = False

        return _index

    def _sort_stores(self):
        self.stores.sort(key=lambda x: x.store_priority)
        for store in self.stores:
            self.store_names.append(store.store_name)

    def load_cloud_stores(self):
        """
        Load cloud secret stores based on settings.
        """
        if self.application_settings.get('secrets_manager', None) and self.application_settings.get(
                'secrets_manager.cloud_stores', None):
            for store_name in self.application_settings.get('secrets_manager.cloud_stores'):
                # Add AWS secret store
                if self.application_settings.get(f'secrets_manager.cloud_stores.{store_name}.store_type') == 'aws':
                    self.stores.append(AWSSecretsStore(store_priority=self.application_settings.get(
                        f'secrets_manager.cloud_stores.{store_name}.priority'),
                                                       store_name=store_name,
                        cloud_session_manager=self.cloud_session_manager,
                                                       application_settings=self.application_settings,
                    ))

                # Add Azure secret store
                if self.application_settings.get(f'secrets_manager.cloud_stores.{store_name}.store_type') == 'azure':
                    self.stores.append(AzureSecretsStore(store_priority=self.application_settings.get(
                        f'secrets_manager.cloud_stores.{store_name}.priority'),
                                                         store_name=store_name,
                        cloud_session_manager=self.cloud_session_manager,
                                                         application_settings=self.application_settings))

        # Sort stores based on priority
        self._sort_stores()

    def get_store(self, store_name):
        """
        Get a secret store by name.

        Args:
            store_name (str): Name of the secret store.

        Returns:
            Secret store instance if found, else None.
        """
        for store in self.stores:
            if store_name == store.store_name:
                return store
        return None

    def get_secret(self, key, default_value=None, store_name=None):
        """
        Get a secret from the secret stores.

        Args:
            key (str): Key of the secret.
            default_value: Default value to return if the secret is not found.
            store_name (str): Name of the secret store.

        Returns:
            Secret value if found, else default_value.
        """
        value = None
        if len(key.split(".")) == 2 and key.split(".")[0] in self.store_names:
            elements = key.split(".")
            store_name = elements[0]
            key = elements[1]

        for store in self.stores:
            if store_name and store_name == store.store_name:
                if store.store_available:
                    value = store.get_secret(key, None)
                else:
                    logging.error(f'Store {store.store_name} is not available to retrieve secret.')
                break
            elif not store_name:
                if store.store_available:
                    value = store.get_secret(key, None)
                    if value:
                        break

        if not value:
            logging.debug(f'The Secret {key} was not found. Returning default value.')
            value = default_value

        return value

    def set_secret(self, key, value, store_name='User_Local_Store'):
        """
        Set a secret in the specified secret store.

        Args:
            key (str): Key of the secret.
            value: Value of the secret.
            store_name (str): Name of the secret store (default is 'User_Local_Store').
        """
        if not store_name:
            store_name = 'User_Local_Store'
        for store in self.stores:
            if store_name == store.store_name:
                if store.store_available and not store.store_read_only:
                    store.set_secret(key, value)
                else:
                    logging.warning(f'Secrets Store {store.store_name} is either not available or is read only.')
                break

    def delete_secret(self, key, store_name='User_Local_Store'):
        """
        Delete a secret from the specified secret store.

        Args:
            key (str): Key of the secret.
            store_name (str): Name of the secret store (default is 'User_Local_Store').

        Returns:
            True if the secret is deleted, else False.
        """
        for store in self.stores:
            if store_name and store_name == store.name():
                value = store.delete_secret(key)
                break
