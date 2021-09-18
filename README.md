# openbox-menu-generator
Generate Openbox Menus from a easy to write configuration file.

Example Configuration:
('#' indicate comments but not implemented yet, so remove them first!)
```
[Openbox]                           # Separator with label
Firefox:firefox                     # Menu item "Firefox" command `firefox`
Terminal:xterm
---                                 # Separator
Places {                            # Sub-menu with label
	Home:xdg-open ~
	Downloads:xdg-open ~/Downloads
}
All Applications {
	!dmenu                          # Template to generate application launchers
	                                # from .desktop files in `/usr/share/application`
	                                # with categories.
	Flatpaks {
		!flatpaks                   # Similar to !dmenu but for flatpaks
	}
}
```

## Usage
`git clone https://github.com/aspirus-in/openbox-menu-generator.git`

`menugen.py menu.conf > ~/.config/openbox/menu.xml`

`openbox --reconfigure`

## Documentation
`[Separator With Label]`

This creates a Separator with Label as the text inside the square brackets.

```
Menu {
	
}
```

This creates a sub-menu with the label as the text before the '{'.
'}' on a single line closes a sub-menu.
Menu items inside the `{}` will appear inside the sub-menu when expanded.

`Menu Item:command`

This creates a single Menu item with a command, the text before the ':' is the label and after is the command to be executed when the item is clicked.

`!dmenu`

This is a template, it will get replaced by Menu items for all the applications (From `.desktop` files inside `/usr/share/applications`) separated into Categories.

`!flatpaks`

This is a template, it will get replaced by Menu items for all the Flatpak applications (From `flatpak list -app` command).
Using this without flatpak installed will result in a broken menu.xml file.
