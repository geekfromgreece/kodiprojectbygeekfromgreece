# -*- coding: utf-8 -*-
import sys
import urllib.parse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_PATH = ADDON.getAddonInfo("path")
HANDLE = int(sys.argv[1])

FANART = f"{ADDON_PATH}/fanart.png"
ICON = f"{ADDON_PATH}/icon.png"

def build_url(query):
    return sys.argv[0] + "?" + urllib.parse.urlencode(query)

def add_item(label, query):
    url = build_url(query)
    li = xbmcgui.ListItem(label=label)
    li.setArt({"icon": ICON, "thumb": ICON, "fanart": FANART})
    li.setProperty("Fanart_Image", FANART)
    xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

def main_menu():
    xbmcplugin.setPluginFanart(HANDLE, FANART)
    add_item("1. Greek TV", {"mode": "greek"})
    add_item("2. Russian TV", {"mode": "russian"})
    xbmcplugin.endOfDirectory(HANDLE)

if __name__ == "__main__":
    main_menu()
