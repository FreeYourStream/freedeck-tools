# FreeDeck-Tools

Nice companion tools for the FreeDeck

## Page Switcher

This tool can automatically switch the active page of the FreeDeck depending on the active window.
You can pick between the python, powershell and bash version. The pythonscript is much faster, works on windows and linux (help for porting to MacOS needed), but requires you to install python.

### Installation

1. Install python3 (windows users click [here](https://www.microsoft.com/de-de/p/python-38/9mssztt1n39l) or [here](https://www.python.org/downloads/windows/))
2. Check if it's installed correctly by typing `python3 --version` in a console. It should show something like `Python 3.9.1`
3. Navigate a console to the folder containing the script and type `pip install -r requirements.txt --user`
4. Configure the page_list.txt as described below
5. Launch the `auto_page_switch.py` script. Either by double clicking on it or by navigating a console to the folder that contains the script. Then type `python auto_page_switch.py`

### Config File (page_list.txt)

Just add your desired pages to the `page_list.txt`. To get the name the script is looking for, just run the script and click a window. It will give you the name you need to put into the `page_list.txt` followed by a comma and the page number. After you have changed the `page_list.txt` you need to restart the script again
You can also pass a third parameter to declare a range of pages for an application, if you are already in this page range, the freedeck won't change the page and stay where it is right now.

```
...
chromium,3
fusion360,7,9
...
```

#### Caveats

- This only works with the freedeck-ino develop branch right now.
- You have to add a blank line to `page_list.txt` at the end or else the last line won't be read.
- (Python) You need python3 in order to run this script. Download [here](https://www.microsoft.com/de-de/p/python-38/9mssztt1n39l) or [here](https://www.python.org/downloads/windows/).
- (Powershell) Its not that fast, despite having no delays in the script
