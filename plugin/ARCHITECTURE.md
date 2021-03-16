# Architecture

Plugin implements two things:

1. A plugin base class and loading system
2. An event engine

These parts are described below.

## Plugins

Plugins are defined as any class that is a subclass of `plugin.Plugin` and is decorated with `decorators.edmc_plugin`,
or a set of functions decorated as callbacks. While the second method of defining a plugin will work, it is discoraged.
TODO: second method does not work

Plugins are loaded as standard python packages. Meaning that the _only_ file that is directly executed (as in,
not executed via import from another file) is `__init__.py`. This file is required to make the plugin a package anyway.
If a developer does not want to store their plugin classes in `__init__.py`, all that is required within that file is
an import of their main plugin file.

### Decorators

There are two decorators that currently defined by plugin:

1. `edmc_plugin`
2. `hook`

`ecmc_plugin` is a class decorator that marks the given class as an edmc plugin to be instantiated later in loading

`hook` is a function decorator that marks the given function as an edmc callback for any number of events

### Loading

On a load call (as in `plugin.manager.PluginManager#load_plugin`), the plugin's module is loaded into the running
interpreter. Once the load is complete, the module is scanned for a decorated class that satisfies the above requirements.
Once a plugin class is found, it is instantiated and the below takes place.

If the load fails, an exception indicating the failure (likely subclass of PluginLoadingException) will be raised by the
loading machinery, this exception will be caught and logged at the top level of loading.

### Old style plugins

Searching for old style plugins is done as part of locating normal plugins. We attempt to load any plugin with an
`__init__.py` as normal, but if it does not contain a decorated plugin class, we then search for a `plugin_start3`.
If we find said file, we load the plugin in the wrapped plugin loading system.

!!UNIMPLEMENTED -- Planning

During the above loading steps to find the packages for new-style plugins, old style plugins are assumed to be
any python files in the root plugin directory, or any directory under the root that has no `__init__.py`. These will
be wrapped in a compatibility class and should continue to work as normal:

1. Load file as a module
2. Map any existing functions in the file to their new counterparts, start3 -> load, journal hooks -> event handlers
3. These will explicitly NOT support reloading. And any attempt to reload them will result in a very large and scary
   exception being thrown.

### Post instantiation of class

After a plugin class is instantiated, two things happen:

1. It is scanned for event callbacks
2. Its on load callback is called

Event callbacks are scanned for and stored as described in the decorator section.

The choice to load callbacks _before_ on_load is called is intentional -- To prevent `on_load` from modifying callbacks.
If a user wants dynamically generated callbacks, they must do so in `__init__`. This is a design choice that may be
changed, but was made to allow for assumptions that may or may not be made in implementation.

## Event Engine

Events are identified by a namespace, and are hooked using the decorator `@hook("namespace.event_name")`.
You can hook onto all events in a given namespace using `@hook("namespace")`, and all events fired with the special 
event name `*`.