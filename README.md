
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
### Caveats
- This only works with the freedeck-ino develop branch right now.
- You have to add a blank line to `page_list.txt` or else the last line won't be read.