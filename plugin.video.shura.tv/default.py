# -*- coding: utf-8 -*
# -*- coding: utf-8 -*
# /*
# *      Copyright (C) 2010-2012 AKGDRG <akgdrg@gmail.com>
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# */

#import xbmcaddon, string, xbmc, xbmcgui, xbmcplugin, os
import time
import datetime
import threading
import urllib.request
import urllib.error
import urllib.parse
import re
import string
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import os
import urllib.request
import urllib.parse
import urllib.error
import http.cookiejar
import xbmcaddon

from resources.lib.iptv import shura

#import web_pdb;

#web_pdb.set_trace()

addon = xbmcaddon.Addon(id='plugin.video.shura.tv')
sys.path.append(os.path.join(addon.getAddonInfo('path'), 'resources', 'lib'))

PLUGIN_ID = 'plugin.video.SHURA.TV'

__settings__ = xbmcaddon.Addon()

__language__ = __settings__.getLocalizedString
OTT = __settings__.getSetting('OTT')
handle = int(sys.argv[1])

PLUGIN_NAME = 'SHURA.TV'
PLUGIN_CORE = None
TRANSSID = ''
thumb = os.path.join(addon.getAddonInfo('path'), "icon2.png")
CHANNELMAPPING_ORIG = os.path.join(
    addon.getAddonInfo('path'), 'channelmapping_orig.txt')
CHANNELMAPPING_USER = os.path.join(
    addon.getAddonInfo('path'), 'channelmapping_user.txt')

def ru(x): return x
def xt(x): return xbmcvfs.translatePath(x)


def get_params():
    param = []
    paramstring = sys.argv[2]
    xbmc.log('[SHURA.TV] [%s] parsing params from %s' %
             (PLUGIN_NAME, paramstring))
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


INFOTIMER_SHOW = None
INFOTIMER_HIDE = None


def gettbn(Title):
    thumb2 = xbmcvfs.translatePath(os.path.join(
        ImgPath, dc.get(xt(Title), ' ')+'.png'))
    return thumb2


def formating(str):
    str = str.strip()
    str = str.replace('\n', '').replace('\r', '')
    str = str.replace(' +1', '').replace(' +2', '').replace(' +3', '').replace(' +4', '').replace(' +5', '').replace(' +6', '').replace(' +7',
                                                                                                                                        '').replace(' -1', '').replace(' -2', '').replace(' -3', '').replace(' -4', '').replace(' -5', '').replace(' -6', '').replace(' -7', '')
    str = str.replace('-', ' ').replace('  ', ' ')
    str = xt(str).lower()
    str = str.replace('Й', 'й')
    str = str.replace('Ц', 'ц')
    str = str.replace('У', 'у')
    str = str.replace('К', 'к')
    str = str.replace('Е', 'е')
    str = str.replace('Н', 'н')
    str = str.replace('Г', 'г')
    str = str.replace('Ш', 'ш')
    str = str.replace('Щ', 'щ')
    str = str.replace('З', 'з')
    str = str.replace('Х', 'х')
    str = str.replace('Ъ', 'ъ')
    str = str.replace('Ф', 'ф')
    str = str.replace('Ы', 'ы')
    str = str.replace('В', 'в')
    str = str.replace('А', 'а')
    str = str.replace('П', 'п')
    str = str.replace('Р', 'р')
    str = str.replace('О', 'о')
    str = str.replace('Л', 'л')
    str = str.replace('Д', 'д')
    str = str.replace('Ж', 'ж')
    str = str.replace('Э', 'э')
    str = str.replace('Я', 'я')
    str = str.replace('Ч', 'ч')
    str = str.replace('С', 'с')
    str = str.replace('М', 'м')
    str = str.replace('И', 'и')
    str = str.replace('Т', 'т')
    str = str.replace('Ь', 'ь')
    str = str.replace('Б', 'б')
    str = str.replace('Ю', 'ю')
    return str


def resetAlarms(plugin, mode):
    refreshAlarmId = '%s_refresh_list' % PLUGIN_ID
    xbmc.executebuiltin("XBMC.CancelAlarm(%s,True)" % refreshAlarmId)
    resetInfoTimers()


def resetInfoTimers():
    if INFOTIMER_SHOW:
        if INFOTIMER_SHOW.isAlive():
            INFOTIMER_SHOW.cancel()
    if INFOTIMER_HIDE:
        if INFOTIMER_HIDE.isAlive():
            INFOTIMER_HIDE.cancel()


def ShowRoot(plugin):
    uri = sys.argv[0] + '?mode=%s'

    tv_title = ' [  %s  ] ' % __language__(30012)
    tv = xbmcgui.ListItem(tv_title)
    tv.setLabel(tv_title)
    tv.setProperty('IsPlayable', 'false')
    tv.setInfo(type='video', infoLabels={
               'title': tv_title, 'plot': __language__(30012)})
    xbmcplugin.addDirectoryItem(handle, uri % 'TV', tv, True)

    favs = __settings__.getSetting('favourites').split(',')
    if len(favs) > 1:
        fv_title = ' [  %s  ] ' % __language__(30041)
        fv = xbmcgui.ListItem(fv_title)
        fv.setLabel(fv_title)
        fv.setProperty('IsPlayable', 'false')
        fv.setInfo(type='video', infoLabels={
                   'title': fv_title, 'plot': __language__(30041)})
        xbmcplugin.addDirectoryItem(handle, uri % 'FAV', fv, True)

    #set_title = ' [  %s  ] ' % __language__(30004)
    #set = xbmcgui.ListItem(set_title)
    # set.setLabel(set_title)
    #set.setProperty('IsPlayable', 'false')
    #set.setInfo( type='video', infoLabels={'title': set_title, 'plot': __language__(30004)})
    #xbmcplugin.addDirectoryItem(handle,uri % 'Settings',set,True)

    set_title = ' [  %s  ] ' % __language__(30005)
    set = xbmcgui.ListItem(set_title)
    set.setLabel(set_title)
    set.setProperty('IsPlayable', 'false')
    set.setInfo(type='video', infoLabels={
                'title': set_title, 'plot': __language__(30005)})
    xbmcplugin.addDirectoryItem(handle, uri % 'openSettings', set, True)

    xbmcplugin.endOfDirectory(handle, True, False)


def ProcessSettings(plugin, params):
    #web_pdb.set_trace()
    if 'name' in params:
        value, options = plugin.getSettingCurrent(params['name'])
        dialog = xbmcgui.Dialog()
        selection = []
        for opval, opname in options:
            selection.append(opname)
        ret = dialog.select(params['title'], selection)
        counter = 0
        for opval, opname in options:
            if counter == ret:
                plugin.setSettingCurrent(params['name'], opval)
            counter = counter + 1
        xbmc.executebuiltin('Container.Refresh')

    else:
        settings = plugin.getSettingsList()

        uri = sys.argv[0] + '?mode=Settings&name=%s&title=%s'

        for setting in settings:
            sName = __language__(setting['language_key'])

            label = setting['value']
            if 'options' in setting:
                for k, v in setting['options']:
                    if k == label:
                        label = v

            sName = sName + ' (%s)' % label

            sItem = xbmcgui.ListItem(sName)
            sItem.setLabel(sName)
            sItem.setProperty('IsPlayable', 'false')
            sItem.setInfo(type='video', infoLabels={
                          'title': sName, 'plot': sName})
            xbmcplugin.addDirectoryItem(handle, uri % (
                setting['name'], __language__(setting['language_key'])), sItem, True)

        xbmcplugin.endOfDirectory(handle, True, False)


def Archive(plugin, feed, host, ArchiveOnly):
    # web_pdb.set_trace()

    item = xbmcgui.ListItem('')
    weekepg = PLUGIN_CORE.getWeekEPG(host, feed)
    arch = PLUGIN_CORE.getArchive(host, feed)
    if weekepg != None and ArchiveOnly != 1:
        for i in range(len(weekepg)-1, -1, -1):
            #xbmc.log('[SHURA.TV] first archive2=' +weekepg[i]['name'])
            CurrentEPG = weekepg[i]['name']
            Description = weekepg[i]['text']
            epg_start = 0
            epg_end = 0
            timerange = '-'
            if "start_time" in weekepg[i]:
                epg_start = datetime.datetime.fromtimestamp(
                    weekepg[i]['start_time']).strftime('%d.%m %H:%M')
                if "duration" in weekepg[i]:
                    epg_end = datetime.datetime.fromtimestamp(
                        weekepg[i]['start_time'] + weekepg[i]['duration']).strftime('%H:%M')
                timerange = '%s - %s ' % (epg_start, epg_end)

            label = '%s[B] %s[/B] %s %s' % ('',
                                            '', timerange + '-'+CurrentEPG, '')

            item.setLabel(label)
            item.setIconImage(os.path.join(addon.getAddonInfo(
                'path'), 'resources', 'icons', 'play-stop.png'))
            item.setInfo(type='video', infoLabels={'title': CurrentEPG, 'plotoutline': '', 'plot': Description, 'genre': '',
                         'duration': weekepg[i]['duration'],  'StartTime': weekepg[i]['start_time'], 'EndTime': weekepg[i]['start_time'] + weekepg[i]['duration']})

            item.setProperty('IsPlayable', 'false')
            urlArchive = '%s~%s/%s/?archive=%s' % (host.split(
                '~')[0], PLUGIN_CORE.OTT,  feed, weekepg[i]['start_time'])
            xbmcplugin.addDirectoryItem(handle, '', item, False, 0)

    if arch != None:
        for archItems in arch:
            #xbmc.log('[SHURA.TV] first archive2=' +archItems['name'])
            CurrentEPG = archItems['name']
            Description = archItems['text']
            #xbmc.log('[SHURA.TV] Description='+Description)
            epg_start = 0
            epg_end = 0
            timerange = '-'
            if "start_time" in archItems:
                epg_start = datetime.datetime.fromtimestamp(
                    archItems['start_time']).strftime('%d.%m %H:%M')
                if "duration" in archItems:
                    epg_end = datetime.datetime.fromtimestamp(
                        archItems['start_time'] + archItems['duration']).strftime('%H:%M')
                timerange = '%s - %s ' % (epg_start, epg_end)

            label = '[COLOR green]%s[B] %s[/B] %s %s[/COLOR]' % (
                '', '', timerange + '-'+CurrentEPG, '')

            item.setLabel(label)
            iconImage = os.path.join(addon.getAddonInfo('path'), 'resources', 'icons', 'play.png')
            item.setArt({'icon': iconImage})
            item.setInfo(type='video', infoLabels={'title': CurrentEPG, 'plotoutline': '', 'plot': Description, 'genre': '',
                         'duration': archItems['duration'],  'StartTime': archItems['start_time'], 'EndTime': archItems['start_time'] + archItems['duration']})
            item.setProperty('IsPlayable', 'true')
            urlArchive = '%s~%s/%s/?archive=%s' % (host.split(
                '~')[0], PLUGIN_CORE.OTT,  feed, archItems['start_time'])
            xbmcplugin.addDirectoryItem(handle, urlArchive, item, False, 0)

    xbmcplugin.setContent(handle, 'Movies')
    xbmcplugin.endOfDirectory(handle, cacheToDisc=False)


def OpenPage(plugin, num):
    # web_pdb.set_trace()

    Lgl = plugin.getLast()

    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()

    counter = 0

    AddOnlyOneFile = __settings__.getSetting('AddOnlyOneChannelToPlaylist') == 'true'
    UseEpg = __settings__.getSetting('UseEpgInChannelsList') == 'true'

    if AddOnlyOneFile:
        i = num
        thumb2 = gettbn(formating(Lgl[i]['name']))
        item = xbmcgui.ListItem(Lgl[i]['name'])
        item.setArt({'icon': thumb2, 'thumb': thumb2})

        epg = None
        if UseEpg:
            epg = PLUGIN_CORE.getLastEPG(Lgl[i]['url'], Lgl[i]['id'])
            #if epg == None or len(epg) <= 0:
            #    epg = PLUGIN_CORE.getCurrentEPG(Lgl[i]['url'], Lgl[i]['id'])
            epg_start = 0
            epg_end = 0
            timerange = '-'
            CurrentEPG = ''
            played = 0
            try:
                #epg = epg[0]

                if float(epg[0]['start_time']) + float(epg[0]['duration']) < float(time.time()):
                    xbmc.log('[SHURA.TV] current epg of channel ' + channel['id']+ ' must be refreshed')
                    epg = PLUGIN_CORE.getCurrentEPG(Lgl[i]['url'], Lgl[i]['id'])

                CurrentEPG = epg[0]['name']

                if "start_time" in epg[0]:
                    epg_start = datetime.datetime.fromtimestamp(
                        epg[0]['start_time']).strftime('%H:%M')
                    if "duration" in epg[0]:
                        epg_end = datetime.datetime.fromtimestamp(
                            epg[0]['start_time'] + epg[0]['duration']).strftime('%H:%M')
                    timerange = '%s - %s ' % (epg_start, epg_end)

            except Exception as e:
                xbmc.log('[SHURA.TV] exception i prepare EPG' + str(e))
        label = '%s[B] %s[/B] %s %s' % ('', Lgl[i]['name'] +
                                        ':', timerange + '-'+CurrentEPG, '')
        if epg != None:
            item.setInfo(type='video', infoLabels={
                         'title': epg[0]['name']})
            item.setInfo(type='video', infoLabels={
                         'plot': epg[0]['name']})
            item.setInfo(type='video', infoLabels={'StartTime': epg_start})
            item.setInfo(type='video', infoLabels={'EndTime': epg_end})
            item.setInfo(type='video', infoLabels={
                         'duration': str(epg[0]['duration']/60)})
            if len(epg) > 1:
                item.setInfo(type='video', infoLabels={'Studio': str(datetime.datetime.fromtimestamp(epg[1]['start_time']).strftime(
                    '%H:%M'))+'-'+str(datetime.datetime.fromtimestamp(epg[1]['start_time']+epg[1]['duration']).strftime('%H:%M'))+':'+epg[1]['name']})
        else:
            item.setInfo(type="Video", infoLabels={"Title": Lgl[i]['name']})

        playlist.add(url=Lgl[i]['url'], listitem=item)
    else:
        for i in range(num, len(Lgl)):
            thumb2 = gettbn(formating(Lgl[i]['name']))
            item = xbmcgui.ListItem(Lgl[i]['name'])
            item.setArt({'icon': thumb2, 'thumb': thumb2})
            epg = None
            if UseEpg:
                epg = PLUGIN_CORE.getLastEPG(Lgl[i]['url'], Lgl[i]['id'])
                #if epg == None or len(epg) <= 0:
                #    epg = PLUGIN_CORE.getCurrentEPG(Lgl[i]['url'], Lgl[i]['id'])
                epg_start = 0
                epg_end = 0
                timerange = '-'
                CurrentEPG = ''
                played = 0
                try:
                    #epg = epg[0]

                    if float(epg[0]['start_time']) + float(epg[0]['duration']) < float(time.time()):
                        #xbmc.log('[SHURA.TV] current epg of channel ' + channel['id']+ ' must be refreshed')
                        epg = PLUGIN_CORE.getCurrentEPG(Lgl[i]['url'], Lgl[i]['id'])

                    CurrentEPG = epg[0]['name']

                    if "start_time" in epg[0]:
                        epg_start = datetime.datetime.fromtimestamp(
                            epg[0]['start_time']).strftime('%H:%M')
                        if "duration" in epg[0]:
                            epg_end = datetime.datetime.fromtimestamp(
                                epg[0]['start_time'] + epg[0]['duration']).strftime('%H:%M')
                        timerange = '%s - %s ' % (epg_start, epg_end)

                except Exception as e:
                    xbmc.log('[SHURA.TV] exception i prepare EPG' + str(e))
                label = '%s[B] %s[/B] %s %s' % ('', Lgl[i]['name'] +
                                                ':', timerange + '-'+CurrentEPG, '')
            if epg != None:
                item.setInfo(type='video', infoLabels={
                             'title': epg[0]['name']})
                item.setInfo(type='video', infoLabels={
                             'plot': epg[0]['name']})
                item.setInfo(type='video', infoLabels={'StartTime': epg_start})
                item.setInfo(type='video', infoLabels={'EndTime': epg_end})
                item.setInfo(type='video', infoLabels={
                             'duration': str(epg[0]['duration']/60)})
                if len(epg) > 1:
                    item.setInfo(type='video', infoLabels={'Studio': str(datetime.datetime.fromtimestamp(epg[1]['start_time']).strftime(
                        '%H:%M'))+'-'+str(datetime.datetime.fromtimestamp(epg[1]['start_time']+epg[1]['duration']).strftime('%H:%M'))+':'+epg[1]['name']})
            else:
                item.setInfo(type="Video", infoLabels={
                             "Title": Lgl[i]['name']})

            playlist.add(url=Lgl[i]['url'], listitem=item)

        for i in range(num):

            thumb2 = gettbn(formating(Lgl[i]['name']))
            item = xbmcgui.ListItem(Lgl[i]['name'])
            item.setArt({'icon': thumb2, 'thumb': thumb2})
            epg = None
            if UseEpg:
                epg = PLUGIN_CORE.getLastEPG(Lgl[i]['url'], Lgl[i]['id'])
                #if epg == None or len(epg) <= 0:
                #    epg = PLUGIN_CORE.getCurrentEPG(Lgl[i]['url'], Lgl[i]['id'])
                epg_start = 0
                epg_end = 0
                timerange = '-'
                CurrentEPG = ''
                played = 0
                try:
                    #epg = epg[0]

                    if float(epg[0]['start_time']) + float(epg[0]['duration']) < float(time.time()):
                        epg = PLUGIN_CORE.getCurrentEPG(Lgl[i]['url'], Lgl[i]['id'])
                    CurrentEPG = epg[0]['name']

                    if "start_time" in epg[0]:
                        epg_start = datetime.datetime.fromtimestamp(
                            epg[0]['start_time']).strftime('%H:%M')
                        if "duration" in epg[0]:
                            epg_end = datetime.datetime.fromtimestamp(
                                epg[0]['start_time'] + epg[0]['duration']).strftime('%H:%M')
                        timerange = '%s - %s ' % (epg_start, epg_end)

                except Exception as e:
                    xbmc.log('[SHURA.TV] exception i prepare EPG' + str(e))
                label = '%s[B] %s[/B] %s %s' % ('', Lgl[i]['name'] +
                                                ':', timerange + '-'+CurrentEPG, '')
            if epg != None:
                item.setInfo(type='video', infoLabels={
                             'title': epg[0]['name']})
                item.setInfo(type='video', infoLabels={
                             'plot': epg[0]['name']})
                item.setInfo(type='video', infoLabels={'StartTime': epg_start})
                item.setInfo(type='video', infoLabels={'EndTime': epg_end})
                item.setInfo(type='video', infoLabels={
                             'duration': str(epg[0]['duration']/60)})
                if len(epg) > 1:
                    item.setInfo(type='video', infoLabels={'Studio': str(datetime.datetime.fromtimestamp(epg[1]['start_time']).strftime(
                        '%H:%M'))+'-'+str(datetime.datetime.fromtimestamp(epg[1]['start_time']+epg[1]['duration']).strftime('%H:%M'))+':'+epg[1]['name']})
            else:
                item.setInfo(type="Video", infoLabels={
                             "Title": Lgl[i]['name']})
            playlist.add(url=Lgl[i]['url'], listitem=item)

    xbmc.Player().play(playlist)  # (url, item)


def ShowChannelsList(plugin, mode='TV'):
    #web_pdb.set_trace()

    refreshAlarmId = '%s_refresh_list' % PLUGIN_ID
    xbmc.log('[SHURA.TV] before GetChannels')
    channels = plugin.getLast()
    if len(channels) <= 0:
        xbmc.log('[SHURA.TV] getNewPlayList')
        channels = PLUGIN_CORE.getChannelsList()
    total_items = len(channels)
    xbmc.log('[SHURA.TV] ChannelCount='+str(total_items))

    xbmc.PlayList(xbmc.PLAYLIST_VIDEO).clear()

    UseEpg = __settings__.getSetting('UseEpgInChannelsList') == 'true'
    UseChannelsMapping = __settings__.getSetting('UseChannelsMapping') == 'true'
    PrefixChannelName = __settings__.getSetting('PrefixChannelName') == 'true'

    CHANNELMAPPING = ''
    channelsCountInFile = 0
    if os.path.isfile(CHANNELMAPPING_USER):
        CHANNELMAPPING = CHANNELMAPPING_USER
    else:
        xbmc.log('[SHURA.TV] No personal channel list mapping found')
        if os.path.isfile(CHANNELMAPPING_ORIG):
            CHANNELMAPPING = CHANNELMAPPING_ORIG
        else:
            xbmc.log('[SHURA.TV] No orig channel list mapping found')
    try:
        if os.path.isfile(CHANNELMAPPING):
            xbmc.log('[SHURA.TV] The %s channel mapping list is used' %
                     CHANNELMAPPING)
            l = open(CHANNELMAPPING, 'r', encoding='utf-8', errors='ignore')
            while 1:
                #web_pdb.set_trace()
                line = l.readline()
                if not line and UseChannelsMapping:
                    break
                pass  # do something
                ch_id = line.split(':')[0]
                #xbmc.log('[SHURA.TV] Current channel map %s' %ch_id)
                channelsCountInFile = channelsCountInFile + 1
                for channel in channels:
                    #xbmc.log('[SHURA.TV] Comparing with channel %s' %channel['id'])
                    if channel['id'] == ch_id or not UseChannelsMapping:
                        #web_pdb.set_trace()
                        #xbmc.log('[SHURA.TV] Match found for %s' %channel['id'])
                        epg = ''
                        try:
                            if UseEpg:
                                epg = PLUGIN_CORE.getLastEPG(channel['url'], channel['id'])
                                #if epg == None or len(epg) <= 0:
                                #    epg = PLUGIN_CORE.getCurrentEPG(channel['url'], channel['id'])
                        except Exception as e:
                            xbmc.log(
                                '[SHURA.TV] Error loading epg for channel%s. Ignore the current epg' % e)
                        epg_start = 0
                        epg_end = 0
                        timerange = '-'
                        CurrentEPG = ''
                        played = 0
                        Description = ''
                        index = channels.index(channel)
                        #xbmc.log('[SHURA.TV] 1')
                        if epg != None and len(epg) != 0:
                            try:
                                epg = epg[0]
                                if float(epg['start_time']) + float(epg['duration']) < float(time.time()):
                                    #xbmc.log('[SHURA.TV] current epg of channel ' + channel['id']+ ' must be refreshed')
                                    epg = PLUGIN_CORE.getCurrentEPG(channel['url'], channel['id'])
                                    epg = epg[0]

                                CurrentEPG = epg['name']
                                Description = epg['text']
                                if "start_time" in epg:
                                    epg_start = datetime.datetime.fromtimestamp(
                                        epg['start_time']).strftime('%H:%M')
                                    if "duration" in epg:
                                        epg_end = datetime.datetime.fromtimestamp(
                                            epg['start_time'] + epg['duration']).strftime('%H:%M')
                                    timerange = '%s - %s ' % (epg_start,
                                                              epg_end)
                                try:
                                    epg_start = float(epg_start)
                                except ValueError:
                                    epg_start = epg_start

                                try:
                                    duration = float(epg['duration'])
                                except ValueError:
                                    duration = epg['duration']

                                played = (
                                    (float(time.time()) - float(epg['start_time'])) / duration)*100
                            except Exception as e:
                                xbmc.log(
                                    '[SHURA.TV] exception in prepare EPG' + str(e))
                            archive_days = ' Архив='
                            archive_days = archive_days + str(int(int(channel['archive'])/24)) + ' дней' 
                            channelName = channel['name']
                            if PrefixChannelName:
                                channelName = ' %d - %s' % (index+1,
                                                            channelName)
                            label = '%s[B] %s[/B] %s %s' % ('', channelName+':', timerange + '-'+ CurrentEPG + ', '+str(int(played)), '%,' + archive_days)
                        else:
                            channelName = channel['name']
                            if PrefixChannelName:
                                channelName = ' %d - %s' % (index+1,
                                                            channelName)
                            label = '%s[B] %s[/B]' % ('', channelName)
                        iconimage = gettbn(formating(channel['name']))
                        item = xbmcgui.ListItem(channel['name'])
                        item.setArt({'icon': iconimage, 'thumb': iconimage})
                        item.setLabel(label)
                        # item.setIconImage(iconimage)

                        item.setInfo(type='video', infoLabels={
                                     'title': channel['name'], 'plotoutline': '', 'plot': Description})
                        #xbmc.log('[SHURA.TV] 2')
                        item.setProperty('IsPlayable', 'false')

                        popup = []

                        archive_text = __language__(30006)
                        uri2 = sys.argv[0] + '?mode=Archive&channel=%s&host=%s' % (
                            channel['id'], channel['url'])
                        popup.append((archive_text, 'Container.Update(%s)' % uri2))

                        epg_text = __language__(30011)

                        uri2 = sys.argv[0] + '?mode=EPG_Archive&channel=%s&host=%s' % (
                            channel['id'], channel['url'])
                        popup.append((epg_text, 'Container.Update(%s)' % uri2))
                        popup.append((__language__(30021), 'Container.Refresh',))

                        item.addContextMenuItems(popup, True)
                        purl = sys.argv[0] + '?mode=OpenPage' + '&num=' + urllib.parse.quote_plus(str(index))

                        xbmcplugin.addDirectoryItem(handle, purl, item, False, total_items)
                        #xbmc.log('[SHURA.TV] 3')
                        refresh_rate = int(__settings__.getSetting('autorefresh_rate'))
                        #xbmcplugin.setContent(handle, 'LiveTV')
                        if UseChannelsMapping:
                            break
                if not UseChannelsMapping:
                    break  # go out at the first loop as we add all channels at once
            l.close()
            xbmcplugin.setContent(handle, 'Movies')
            xbmcplugin.endOfDirectory(handle, cacheToDisc=False)
            if refresh_rate > 0:
                xbmc.executebuiltin("XBMC.AlarmClock(%s,XBMC.Container.Refresh,%s,True)" % (
                    refreshAlarmId, refresh_rate))
            #xbmc.log('[SHURA.TV] 4')
    except Exception as e:
        xbmc.log('[SHURA.TV] Error loading channel mapping %s' % e)
    if UseChannelsMapping and channelsCountInFile < len(channels):
        if os.path.isfile(CHANNELMAPPING):
            xbmc.log(
                '[SHURA.TV] Some channels are missing in mapping file, appending...')
            for channel in channels:
                found = 0
                ch_id = channel['id']
                file = open(CHANNELMAPPING, 'r')
                while 1:
                    line = file.readline()
                    if not line:
                        break
                    pass  # do something
                    if line.split(':')[0] == ch_id:
                        found = 1
                        xbmc.log('[SHURA.TV] match found')
                        break
                file.close()
                if found == 0:
                    xbmc.log(
                        '[SHURA.TV] No match found. Try to append %s' % ch_id)
                    try:
                        file = open(CHANNELMAPPING, 'a+')
                        file.write('\n'+ch_id+': ')
                        xbmc.log('[SHURA.TV] Channel %s added' % ch_id)
                        file.close()
                    except Exception as e:
                        xbmc.log(
                            '[SHURA.TV] Error during append channel to channel mapping file. Error=%s' % e)


def SetupInfoTimer():
    resetInfoTimers()
    INFOTIMER_SHOW = threading.Timer(10.0, ShowNowPlayingInfo)
    xbmc.log('[SHURA.TV] [%s] Info timer is set' % (PLUGIN_NAME))
    INFOTIMER_SHOW.start()


xbmc.log('[SHURA.TV] [%s] Loaded' % (PLUGIN_NAME))

params = get_params()

num = 0

if '_s' in params and '_sn' in params:
    SID = params['_s']
    SID_NAME = params['_sn']
else:
    SID = None
    SID_NAME = None

PLUGIN_CORE = shura(OTT, __settings__.getSetting(
    'stream_type'), __settings__.getSetting('server'))

dc = {"1 канал": "001", "1+1": "002"}
try:
    from canal_list import*
except:
    pass


ImgPath = os.path.join(addon.getAddonInfo('path'), 'resources', 'logo')

if 'mode' in params:
    mode = params['mode']
    #xbmc.log('mode in parms')
else:
    mode = 'TV'


if 'channel' in params:
    channel = params['channel']
else:
    channel = None

if 'host' in params:
    host = params['host']
else:
    host = ''

try:
    num = int(urllib.parse.unquote_plus(params["num"]))
except:
    pass

xbmc.log('[SHURA.TV] [%s] mode: %s' % (PLUGIN_NAME, mode))

resetAlarms(PLUGIN_CORE, mode)

if mode == 'archive' or mode == 'Archive':
    Archive(PLUGIN_CORE, channel, host, 1)

elif mode == 'epg_archive' or mode == 'EPG_Archive':
    Archive(PLUGIN_CORE, channel, host, 0)

elif mode == 'OpenPage':
    OpenPage(PLUGIN_CORE, num)

elif mode == 'PlayNext':
    PlayNext(PLUGIN_CORE, channel)

elif mode == 'ShowNowNextHint':
    ShowNowNextHint(PLUGIN_CORE, channel)

elif mode in ('TV', 'FAV'):
    ShowChannelsList(PLUGIN_CORE, mode)

elif mode == 'Favourite':
    Favourite(PLUGIN_CORE, channel)

elif mode == 'Settings' or mode == 'settings':
    ProcessSettings(PLUGIN_CORE, params)

elif mode == 'openSettings':
    __settings__.openSettings()

elif mode == 'ExecURL':
    Get(url)
    xbmc.sleep(50)
    xbmc.executebuiltin('Container.Refresh')
else:
    ShowRoot(PLUGIN_CORE)
