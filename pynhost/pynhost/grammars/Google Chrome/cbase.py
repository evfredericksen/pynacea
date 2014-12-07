import time
from pynhost import api
from pynhost.grammars import baseutils, extension

# H   :   Go back in history
# L   :   Go forward in history
# Manipulating tabs
# K, gt   :   Go one tab right
# J, gT   :   Go one tab left
# t   :   Create new tab
# x   :   Close current tab
# X   :   Restore closed tab
# Navigating the page
# ?   :   Show the help dialog
# j   :   Scroll down
# k   :   Scroll up
# h   :   Scroll left
# l   :   Scroll right
# gg  :   Scroll to the top of the page
# G   :   Scroll to the bottom of the page
    
# u, <c-u>    :   Scroll a half page up
# d, <c-d>    :   Scroll a half page down
# <c-f>   :   Scroll a full page down
# <c-b>   :   Scroll a full page up
# f   :   Open a link in the current tab
# F   :   Open a link in a new tab
# o   :   Open URL, bookmark, or history entry
# O   :   Open URL, bookmark, or history entry in a new tab
    
# r   :   Reload the page
# gs  :   View page source
# /   :   Enter find mode
# n   :   Cycle forward to the next find match
# N   :   Cycle backward to the previous find match
# yy  :   Copy the current URL to the clipboard
# gf  :   Cycle focus to the next frame
# i   :   Enter insert mode

class ChromeBaseGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
            'basic': '(back | forward | right | left | new tab | <hom_down> | up | bottom | top | talk | bar | close | refresh) [<num>]',
            'go_to_website': '(go to | goto ) {}',
            'open_in_new_tab': 'new',
            'rewind_ff': '(rewind | fast-forward) <num> [(minutes | this | minute) [and] [<num>]] [seconds]',
        }

        self.dictionary = {
            'bed': 'reddit.com',
            'read': 'reddit.com',
            'reddit': 'reddit.com',
            'awful': 'forums.somethingawful.com',
            'something awful': 'forums.somethingawful.com',
            'slashdot': 'slashdot.org',
            'you to': 'youtube.com',
            'youtube': 'youtube.com',
            'okcupid': 'okcupid.com',
            'news': 'news.google.com',
            'wikipedia': 'wikipedia.org',
        }

    def basic(self, words):
        api.send_string('{escape}')
        d = {
            'back': '{shift+h}',
            'forward': '{shift+l}',
            'right': '{shift+k}',
            'left': '{shift+j}',
            'new tab': 't',
            'down': 'dd',
            'up': 'uu',
            'top': 'gg',
            'talk': 'gg',
            'bottom': '{shift+g}',
            'bar': '{ctrl+l}',
            'close': '{ctrl+w}',
            'refresh': 'r',
        }
        if not words[-1].isdigit():
            words.append('1')
        words[0] = d[' '.join(words[:-1])]
        num = int(baseutils.set_number(words))
        for i in range(num):
            api.send_string(words[0])
            time.sleep(.1)

    def go_to_website(self, words):
        api.send_string('{ctrl+l}{backspace}' + words[-1] + '{enter}')

    def open_in_new_tab(self, words):
        api.send_string('{shift+f}')

    def rewind_ff(self, words):
        m = {'rewind': 'j', 'fast-forward': 'l'}
        key = m[words[0]]
        minutes = 0
        seconds = 0
        if 'minutes' in words or 'minute' in words:
            minutes = int(words[1])
        if words[-1].isdigit():
            seconds = int(words[-1])
        if 'seconds' in words:
            seconds = int(words[-2])
        num = minutes * 6 + seconds // 10
        if num:
            api.send_string('i')
        for i in range(num):
            api.send_string(key)
        if num:
            api.send_string('{escape}')      

    def close_tab(self, words):
        api.send_string('{ctrl+w}')

    def undo(self, words):
        api.send_string('{ctrl+z}')

    def redo(self, words):
        api.send_string('{ctrl+y}')

    def vertical_split(self, words): 
        api.send_string('{shift+alt+2}')

    def merge(self, words):
        api.send_string('{shift+alt+1}')
