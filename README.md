# mifit-font
Miband2 font tool
===================

This tool is based on https://github.com/amazfitbip/tools bipfont.py and https://gist.github.com/joserebelo/b9be41b7b88774f712e2f864fdd39878. It uses the font character files generated from the first tool, as thtere are many fonts like that on Internet. Please note, that fonts which are exported from MiBand 2 lack the information encoded in last number of character file name - the offset, so I would adwise against using them the other way. 

The font may be flashed by GadgetBridge or some other tool which supports custom firmware (font) flashing, but it is not widely tested. 

Notice: I was not able to test the font in an application which would send characters directly and is known to work. Gadgetbridge's test call displayed utf-8 characters outside of standard 8-bit ASCII with an extra space after them, so I don't know if it is its issue or firmware issue. Most apps provide transliteration to 7-bit ASCII anyway or do not support text display at all.

mi2font-sep.py
---------------

Usage:
   python ./mi2font-sep.py unpack Mili_chaohu.ft

	unpack the font to bmp files in bmp subdirectory

   python ./mi2font-sep.py pack new_Mili_chaohu.ft

	repack the font using bmp files in bmp subdirectory, use Chinese font header

   python ./mi2font-sep.py pack new_Mili_chaohu.ft en

	repack the font using bmp files in bmp subdirectory, use English font header

Mili_pro.ft.cz
---------------

Minimal font containing Czech characters

Mili_pro_czsk.ft
----------------

Font based on https://www.miuios.cz/fonty-s-cz-sk-diakritikou-23145 - complete version

Mili_pro_czsk_nosymbol.ft
--------------------------

Previous font with extra symbols for borders and ASCII-art removed
