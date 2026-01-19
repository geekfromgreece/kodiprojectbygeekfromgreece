# -*- coding: utf-8 -*-
import sys
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
HANDLE = int(sys.argv[1])

FANART = f"{ADDON_PATH}/fanart.jpg"
ICON = f"{ADDON_PATH}/icon.png"

def build_url(q):
    return sys.argv[0] + "?" + urllib.parse.urlencode(q)

def add_dir(label, q):
    url = build_url(q)
    li = xbmcgui.ListItem(label=label)
    li.setArt({"icon": ICON, "thumb": ICON, "fanart": FANART})
    li.setProperty("Fanart_Image", FANART)
    xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

def root_menu():
    xbmcplugin.setPluginFanart(HANDLE, FANART)
    add_dir("1. Greek TV", {"mode": "gr"})
    add_dir("2. Russian TV", {"mode": "ru"})
    xbmcplugin.endOfDirectory(HANDLE)

if __name__ == "__main__":
    root_menu()
