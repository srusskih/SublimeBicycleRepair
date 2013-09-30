SublimeBicycleRepair
====================

http://bicyclerepair.sourceforge.net/ plugin


**Underconstruction!** Feel free join

Commands
--------

 - **Rename** - Rename method, function, class
 - **Undo** - Undo the last refactoring (works if files was not changes from last refctoring)

Settings
--------

By default the plugin will use default Python interpreter from the `PATH`.
Also you can set different interpreter for each Sublime Project.

To set project related Python interpreter you have to edit yours project config file.
By default project config name is `<project name>.sublime-project`

You can set Python interpreter, and additional python package directories, using following:

    # <project name>.sublime-project
    {
        // ...

        "settings": {
            // ...
            "python_interpreter_path": "/home/sr/.virtualenvs/django1.5/bin/python"
            "python_package_paths": [
                "/home/sr/python_packages1",
                "/home/sr/python_packages2",
                "/home/sr/python_packages3"
            ]
        }
    }



TODO
----
  
  - extract function
  - extract method
  - extract local variable
  - inline local variable
  - move class to module






License 
-------

[MIT](/LICENSE)

http://bicyclerepair.sourceforge.net/ is under BSD license
