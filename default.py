# -*- coding: utf-8 -*-
import re,string
import urllib, urllib2
import xbmcgui, xbmcplugin

pluginUrl = sys.argv[0]
pluginHandle = int(sys.argv[1])
pluginQuery = sys.argv[2]

def get_stream_url(channel_id):
    xml = urllib2.urlopen('http://tvgry.pl/player/playlist_union.asp?ID=' + channel_id + '&QUALITY=2&SECTION=TV').read()
    match=re.compile(':file>([^<]+)').findall(xml)[0]
    return match

def add_video_item(gru):
    html = urllib2.urlopen('http://www.gry-online.pl/'+gru).read()
    match=re.compile('a href="([^"]+)">nast').findall(html)
    if len(match) > 0:
        next_page = xbmcgui.ListItem('>> strona ' + match[0][-1])
        xbmcplugin.addDirectoryItem(pluginHandle, pluginUrl+"?grupa="+urllib.quote_plus(match[0]), next_page, isFolder=True)
    for v in re.finditer('src="([^"]+)"><a href="[^0-9]+([0-9]+)"></a></div><h4>([^<]+)', html):
        img, filename, title = v.groups()
        listitem = xbmcgui.ListItem(title.decode('cp1250'), iconImage=img, thumbnailImage=img)
        listitem.setInfo('video', {'title': title.decode('cp1250') })
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(pluginHandle, pluginUrl+"?odtwarzaj="+filename, listitem, isFolder=False)

if pluginQuery.startswith('?odtwarzaj='):
    channel_id = pluginQuery[11:]
    stream_url = get_stream_url(channel_id)
    xbmcplugin.setResolvedUrl(pluginHandle, True, xbmcgui.ListItem(path=stream_url))
elif pluginQuery.startswith('?grupa='):
    GRU_id = urllib.unquote_plus(pluginQuery[7:])
    add_video_item(GRU_id)
else:
    html = urllib2.urlopen('http://www.gry-online.pl/telewizja-dla-graczy.asp').read()
    for v in re.finditer('a href="([^"]+)" class="pr [^>]+>([^<]+)', html):
        link, title = v.groups()
        listitem = xbmcgui.ListItem(title.decode('cp1250'))
        xbmcplugin.addDirectoryItem(pluginHandle, pluginUrl+"?grupa="+urllib.quote_plus(link), listitem, isFolder=True)
xbmcplugin.endOfDirectory(pluginHandle) 
