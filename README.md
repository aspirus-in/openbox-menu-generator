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
`git clone <repository>`

`menugen.py menu.conf > ~/.config/openbox/menu.xml`

`openbox --reconfigure`
