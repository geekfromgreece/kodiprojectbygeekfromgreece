# -*- coding: utf-8 -*-
import sys
import json
import urllib.parse

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo("id")
ADDON_PATH = ADDON.getAddonInfo("path")
HANDLE = int(sys.argv[1])

FANART = f"{ADDON_PATH}/fanart.jpg"
ICON = f"{ADDON_PATH}/icon.png"

PROFILE_DIR = xbmcvfs.translatePath(f"special://profile/addon_data/{ADDON_ID}")
CHANNELS_FILE = xbmcvfs.translatePath(f"{PROFILE_DIR}/channels.json")

def ensure_profile():
    if not xbmcvfs.exists(PROFILE_DIR):
        xbmcvfs.mkdirs(PROFILE_DIR)

def load_user_urls():
    ensure_profile()
    if not xbmcvfs.exists(CHANNELS_FILE):
        return {}
    try:
        f = xbmcvfs.File(CHANNELS_FILE)
        data = f.read()
        f.close()
        return json.loads(data) if data else {}
    except Exception:
        return {}

def save_user_urls(data):
    ensure_profile()
    f = xbmcvfs.File(CHANNELS_FILE, "w")
    f.write(json.dumps(data, ensure_ascii=False, indent=2))
    f.close()

def build_url(q):
    return sys.argv[0] + "?" + urllib.parse.urlencode(q)

def add_dir(label, q):
    url = build_url(q)
    li = xbmcgui.ListItem(label=label)
    li.setArt({"icon": ICON, "thumb": ICON, "fanart": FANART})
    li.setProperty("Fanart_Image", FANART)
    xbmcplugin.addDirectoryItem(HANDLE, url, li, True)

def add_play(label, stream_url, channel_key):
    li = xbmcgui.ListItem(label=label)
    li.setArt({"icon": ICON, "thumb": ICON, "fanart": FANART})
    li.setProperty("Fanart_Image", FANART)
    li.setProperty("IsPlayable", "true")
    li.setPath(stream_url)
    xbmcplugin.addDirectoryItem(HANDLE, build_url({"mode":"play","u":stream_url,"k":channel_key}), li, False)

def end_dir():
    xbmcplugin.setContent(HANDLE, "videos")
    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)

# --- Channel catalog (names only). For private channels you must provide a legal stream URL (m3u8/mpd) yourself.
GREEK_CHANNELS = [
    ("ant1", "ANT1"),
    ("alpha", "ALPHA"),
    ("mega", "MEGA"),
    ("star", "STAR Channel"),
    ("skai", "SKAI"),
    ("open", "OPEN"),
    ("makedonia", "Makedonia TV"),
    ("ert1", "ERT1"),
    ("ert2", "ERT2"),
    ("ert3", "ERT3"),
    ("ertnews", "ERT NEWS"),
    ("ertworld", "ERT World"),
    ("vouli", "Βουλή (Hellenic Parliament TV)"),
    ("star_kentrikis_ellados", "STAR Κεντρικής Ελλάδας"),
    ("ena_kentrikis_ellados", "ENA Κεντρικής Ελλάδας"),
    ("action24", "Action 24"),
    ("attica", "Attica TV"),
    ("kontra", "Kontra Channel"),
    ("rise", "RISE TV"),
    ("blue_sky", "Blue Sky"),
    ("tilemax", "Tilemax"),
    ("4e", "4E"),
    ("alert", "Alert TV"),
    ("achaia", "Achaia TV"),
    ("aeolos", "Aeolos TV"),
    ("acheloos", "Acheloos TV"),
    ("epirus", "Epirus TV1"),
    ("kritis", "Kriti TV"),
    ("cretatv", "CRETA TV"),
    ("dion", "Dion TV"),
    ("thrakinet", "Thrakinet TV"),
    ("startv", "Start TV (Kozani)"),
    ("lefkadatv", "Lefkada TV"),
    ("ionian", "Ionian TV"),
    ("mesogeios", "Mesogeios TV"),
    ("smile", "Smile TV"),
    ("syros", "Syros TV1"),
    ("tv100", "TV100 Thessaloniki"),
]

RUSSIAN_CHANNELS = [
    ("channel_one", "Channel One Russia"),
    ("russia1", "Russia-1"),
    ("rtr_planeta", "RTR-Planeta"),
    ("ntv", "NTV"),
    ("ctc", "CTC"),
    ("zvezda", "Zvezda"),
    ("zvezda_plus", "Zvezda PLUS"),
]

def root_menu():
    xbmcplugin.setPluginFanart(HANDLE, FANART)
    add_dir("1. Greek TV", {"mode": "greek"})
    add_dir("2. Russian TV", {"mode": "russian"})
    end_dir()

def greek_menu():
    xbmcplugin.setPluginFanart(HANDLE, FANART)
    add_dir("📺 Όλα τα Ελληνικά Κανάλια", {"mode":"greek_all"})
    add_dir("⚙️ Διαχείριση Stream URLs (set/clear)", {"mode":"manage", "country":"gr"})
    end_dir()

def russian_menu():
    xbmcplugin.setPluginFanart(HANDLE, FANART)
    add_dir("📺 Βασικά Ρωσικά Κανάλια", {"mode":"russian_all"})
    add_dir("⚙️ Διαχείριση Stream URLs (set/clear)", {"mode":"manage", "country":"ru"})
    end_dir()

def list_channels(country):
    xbmcplugin.setPluginFanart(HANDLE, FANART)
    user_urls = load_user_urls()

    if country == "gr":
        channels = GREEK_CHANNELS
        title = "Όλα τα Ελληνικά Κανάλια"
    else:
        channels = RUSSIAN_CHANNELS
        title = "Ρωσικά Κανάλια"
    # Header item (non-playable)
    add_dir(f"✅ {title} (βάλε νόμιμα URLs ανά κανάλι)", {"mode":"noop"})

    for key, name in channels:
        url = user_urls.get(key, "").strip()
        if url:
            add_play(name, url, key)
        else:
            add_dir(f"{name}  —  [Set stream URL]", {"mode":"set_url", "k": key, "n": name})
    end_dir()

def set_url(channel_key, channel_name):
    user_urls = load_user_urls()
    current = user_urls.get(channel_key, "")
    dlg = xbmcgui.Dialog()
    note = "Βάλε νόμιμο stream URL (π.χ. m3u8/mpd) από δική σου πηγή/συνδρομή.\n(Δεν παρέχονται πειρατικά links.)"
    url = dlg.input(f"Set URL: {channel_name}", defaultt=current, type=xbmcgui.INPUT_ALPHANUM)
    if url is None:
        return
    url = url.strip()
    if not url:
        # Clear
        if channel_key in user_urls:
            user_urls.pop(channel_key, None)
            save_user_urls(user_urls)
        dlg.notification("geekfromgreece", f"Cleared: {channel_name}", xbmcgui.NOTIFICATION_INFO, 2500)
    else:
        user_urls[channel_key] = url
        save_user_urls(user_urls)
        dlg.notification("geekfromgreece", f"Saved: {channel_name}", xbmcgui.NOTIFICATION_INFO, 2500)

    # Return to list
    xbmc.executebuiltin("Container.Refresh")

def manage(country):
    xbmcplugin.setPluginFanart(HANDLE, FANART)
    if country == "gr":
        channels = GREEK_CHANNELS
        title = "Manage Greek URLs"
    else:
        channels = RUSSIAN_CHANNELS
        title = "Manage Russian URLs"

    add_dir(f"⚙️ {title}", {"mode":"noop"})
    for key, name in channels:
        add_dir(f"Set/Clear: {name}", {"mode":"set_url", "k": key, "n": name})
    end_dir()

def play(u):
    # Kodi plays listitem path directly when returning a playable item,
    # but we keep a 'play' route for clarity/logging.
    li = xbmcgui.ListItem(path=u)
    li.setProperty("IsPlayable", "true")
    xbmcplugin.setResolvedUrl(HANDLE, True, li)

def router():
    params = dict(urllib.parse.parse_qsl(sys.argv[2][1:])) if len(sys.argv) > 2 and sys.argv[2] else {}
    mode = params.get("mode", "root")

    if mode == "greek":
        greek_menu()
    elif mode == "russian":
        russian_menu()
    elif mode == "greek_all":
        list_channels("gr")
    elif mode == "russian_all":
        list_channels("ru")
    elif mode == "set_url":
        set_url(params.get("k",""), params.get("n",""))
    elif mode == "manage":
        manage(params.get("country","gr"))
    elif mode == "play":
        play(params.get("u",""))
    else:
        root_menu()

if __name__ == "__main__":
    router()
