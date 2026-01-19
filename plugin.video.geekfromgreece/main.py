# -*- coding: utf-8 -*-
import sys
import xbmcplugin
import xbmcgui
import xbmcaddon
from urllib.parse import parse_qs, urlencode

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])

# Simple routing
params = parse_qs(sys.argv[2][1:]) if len(sys.argv) > 2 else {}
mode = (params.get("mode", [""])[0] or "").strip()
country = (params.get("country", [""])[0] or "").strip()


def add_dir(name, query):
    url = sys.argv[0] + "?" + urlencode(query)
    li = xbmcgui.ListItem(label=name)
    li.setArt({"icon": "special://home/addons/plugin.video.geekfromgreece/icon.png"})
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=li, isFolder=True)


def add_playable(name, stream_url):
    li = xbmcgui.ListItem(label=name)
    li.setProperty("IsPlayable", "true")
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=stream_url, listitem=li, isFolder=False)


def list_root():
    add_dir("🇬🇷 Ελληνικά", {"mode": "list", "country": "gr"})
    add_dir("🇷🇺 Ρωσικά", {"mode": "list", "country": "ru"})
    xbmcplugin.endOfDirectory(HANDLE)


def list_channels(country_code):
    # Placeholder channels. Next step: we will replace with real working sources.
    if country_code == "gr":
        channels = [
            ("ERT1", ""),
            ("ERT2", ""),
            ("ERT3", ""),
            ("ERT World", ""),
            ("Βουλή", ""),
            ("STAR Κεντρικής Ελλάδας", ""),
            ("ENA", ""),
            ("ANT1 (DRM)", ""),
            ("MEGA (DRM)", ""),
            ("ALPHA (DRM)", ""),
            ("STAR (DRM)", ""),
        ]
    else:
        channels = [
            ("Channel One Russia", ""),
            ("Russia-1", ""),
            ("RTR-Planeta", ""),
            ("NTV", ""),
            ("CTC", ""),
            ("Zvezda", ""),
            ("Zvezda Plus", ""),
        ]

    for name, url in channels:
        if url:
            add_playable(name, url)
        else:
            # For now, show as non-playable folder item (we'll fix streams in next step)
            add_dir(name, {"mode": "noop"})

    xbmcplugin.endOfDirectory(HANDLE)


def noop():
    xbmcgui.Dialog().notification("GeekFromGreece", "Next step: add real stream URLs", xbmcgui.NOTIFICATION_INFO, 3000)


if mode == "list" and country:
    list_channels(country)
elif mode == "noop":
    noop()
else:
    list_root()
