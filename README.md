# i3stuff
This project provides Python replacements for i3bar and i3status, used in the i3 window manager.

You can either only use the status line generator **cstatus** with the original i3bar or replace the i3bar with **cbar**.

## Screenshot
![cbar](screenshot.png?raw=true "CBar")

## Use cstatus with i3bar
Modify your i3 configuration file to include
```
bar {
        status_command python3 -u /path/to/cstatus/cstatus.py
        position top
        font pango:Terminus 15
        separator_symbol "    "
}
```

## Replace i3bar with cbar
Remove the bar configuration and append

```
exec --no-startup-id /path/to/cbar/cbar.py
```
to your i3 configuration file.
It might be necessary to extend your **PYTHONPATH** variable to include the cstatus directory
