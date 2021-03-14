# freedeck-tools
Nice tools for the Freedeck

## CAD-Files
For an nice enclosure for the Freedeck there are a couple pre made CAD files that you can print yourself on a 3D printer.
- https://www.thingiverse.com/thing:4511644 Through Hole 3x2 Case(By AdamWelch)
- https://www.thingiverse.com/thing:4566274 Through Hole 3x2 Case Screwless (By Thijseigenwijs)

# Tools that work with the FreeDeck

## Linux

### Page Switcher

This tool can automatically switch the active page of the FreeDeck depending on the active window in your X11 session.
Just add your desired pages to the `page_list.txt`. To get the name the script is looking for, just run the script and click a window. It will give you the name you need to put into the `page_list.txt` followed by a comma and the page number.

```
...
chromium,3
...
```
When you are using chrome it will switch to page 3.

#### Caveats
- This only works with the freedeck-ino develop branch right now.
- You have to add a blank line to `page_list.txt` or else the last line won't be read.

## Windows

### Page Switcher

This tool can automatically switch the active page of the FreeDeck depending on the active window. Just add your desired pages to the `page_list.txt`. To get the name the script is looking for, just run the script and click a window. It will give you the name you need to put into the `page_list.txt` followed by a comma and the page number. After you have changed the `page_list.txt` you need to restart the python script again


#### Caveats
- This only works with the freedeck-ino develop branch right now.
- You have to add a blank line to `page_list.txt` or else the last line won't be read.
- You need python3 in order to run this script. Install instructions can be found in `windows\installGuide.txt`