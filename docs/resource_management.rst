
Resource Management in the Application
======================================

The dtPyAppFramework includes a robust Resource Manager, which is a singleton class named ResourceManager. This class streamlines the process of managing various resources such as images, text files, or any other file-based assets within your application.

Accessing the Resource Manager
------------------------------

To utilise the Resource Manager, follow these steps:

Access the singleton instance of the **\ ``ResourceManager``\ **\ :

.. code-block:: python

   from dtPyAppFramework.resources import ResourceManager

   resource_manager = ResourceManager()

Resource Directories
--------------------

The Resource Manager searches for resources in specific directories. By default, it looks for resources in the following directories:


* User-specific data root path: ``os.path.join(self.application_paths.usr_data_root_path, "resources")``
* All users' data root path: ``os.path.join(self.application_paths.app_data_root_path, "resources")``
* Current working directory: ``os.path.join(os.getcwd(), "resources")``

Retrieving Resources in the Application
---------------------------------------

The **\ ``ResourceManager``\ ** class provides a straightforward method to retrieve the full path to a resource within your application. Use the ``get_resource_path`` function, passing the name of the resource as an argument. The Resource Manager will search through predefined resource directories and return the full path to the resource if found.

Retrieving Resource Paths
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Assuming you have a ResourceManager instance named resource_manager

   # Retrieve the full path to an image resource
   image_path = resource_manager.get_resource_path("example_image.png")

   # Retrieve the full path to a text file resource
   text_file_path = resource_manager.get_resource_path("example_text.txt")

Function Definition
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   def get_resource_path(self, resource):
       """
       Get the full path to a resource.

       Args:
           resource (str): Name of the resource.

       Returns:
           str: Full path to the resource, or None if not found.
       """

The ``get_resource_path`` function iterates through the defined resource directories and checks for the existence of the specified resource. If found, it returns the full path to the resource; otherwise, it logs an error and returns ``None``.

Example
~~~~~~~

.. code-block:: python

   from dtPyAppFramework.resources import ResourceManager

   # Access the singleton instance of the ResourceManager
   resource_manager = ResourceManager()

   # Retrieve the full path to an image resource
   image_path = resource_manager.get_resource_path("example_image.png")

   # Retrieve the full path to a text file resource
   text_file_path = resource_manager.get_resource_path("example_text.txt")

   # Check if the resources were found
   if image_path:
       print(f"Full path to the image: {image_path}")
   else:
       print("Image resource not found.")

   if text_file_path:
       print(f"Full path to the text file: {text_file_path}")
   else:
       print("Text file resource not found.")

Use the ``get_resource_path`` function to dynamically obtain the full path to your application's resources, making it convenient for various resource management needs.

Retrieving Resources with Partial Paths
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``get_resource_path`` function in the ResourceManager class supports retrieving resources by providing a partial file path. This allows you to specify a partial path or filename, and the function will search through the predefined resource directories, attempting to find a match. If a match is found, it returns the full path to the resource; otherwise, it returns ``None``.

Retrieving Resources with Partial Paths
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Assuming you have a ResourceManager instance named resource_manager

   # Retrieve the full path to a JavaScript file with a partial path
   javascript_path = resource_manager.get_resource_path("/javascript/test.js")

   # Retrieve the full path to a CSS file with a partial path
   css_path = resource_manager.get_resource_path("/styles/main.css")

Example
~~~~~~~

.. code-block:: python

   from dtPyAppFramework.resources import ResourceManager

   # Access the singleton instance of the ResourceManager
   resource_manager = ResourceManager()

   # Retrieve the full path to a JavaScript file with a partial path
   javascript_path = resource_manager.get_resource_path("/javascript/test.js")

   # Retrieve the full path to a CSS file with a partial path
   css_path = resource_manager.get_resource_path("/styles/main.css")

   # Check if the resources were found
   if javascript_path:
       print(f"Full path to the JavaScript file: {javascript_path}")
   else:
       print("JavaScript file not found.")

   if css_path:
       print(f"Full path to the CSS file: {css_path}")
   else:
       print("CSS file not found.")

Use the ``get_resource_path`` function with partial paths to conveniently locate resources within your application based on specific directory structures or filenames.
