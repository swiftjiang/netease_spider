#!/usr/bin/env python
# -*- coding: utf-8 -*-

import public as uapi
import tools
from terminaltables import AsciiTable
import playlist_config


class Playlist:
    def __init__(self):
        self.__headers = uapi.header
        self.__url = uapi.music_url

    def curl_playlist(self, playlist_id):
        # playlist_api = "http://music.163.com/api/playlist/detail?id={}&upd" (playlist_id)
        url = uapi.playlist_api.format(playlist_id)
        try:
            data = tools.curl(url, self.__headers)
            playlist = data['result']
            return playlist
        except Exception as e:
            print("抓取歌单页面存在问题：{} 歌单ID：{}".format(e, playlist_id))

    def view_capture(self, link):
        # url = "http://music.163.com/api/playlist/detail?id="  +  link(int(playlist_id)
        url = self.__url + str(link)
        songs = []
        try:
            # 歌单信息
            playlist = self.curl_playlist(link)
            # 曲目信息
            musics = playlist['tracks']
            exist = 0
            for music in musics:
                sid = music['id']
                name = tools.encode(music['name'])
                author = tools.encode(music['artists'][0]['name'])
                album = tools.encode(music['album']['name'])
                if music["bMusic"] is None:
                    play_time = 0
                else:
                    play_time = music["bMusic"]["playTime"]
                # 修改添加
                song = [sid, name, author, play_time, album]
                songs.append(song)
                # 数据库检查
                # 如果不在数据库，存入数据库，并且exist++
                del song
            return playlist, songs, exist
        except Exception as e:
            print("抓取歌单页面存在问题：{} 歌单ID：{}".format(e, url))

    def get_playlist(self, playlist_id):
        playlist, songs, exist = self.view_capture(int(playlist_id))
        #  歌单名称
        playlist_name = tools.encode("<<" + str(playlist['name']) + ">>")
        # 歌单ID
        playlist_id = tools.encode(str(playlist_id))
        # 歌单曲目数量
        count = tools.encode(str(playlist['trackCount']))
        # 歌单作者
        author = tools.encode(str(playlist['creator']['nickname']))
        # 播放次数
        play = tools.encode(str(playlist['playCount']))
        # 歌单订阅量
        subscribed = tools.encode(str(playlist['subscribedCount']))
        # 歌单分享数量
        share = tools.encode(str(playlist['shareCount']))
        # 歌单评论数量
        comment = tools.encode(str(playlist['commentCount']))
        # 歌单描述
        description = tools.encode(str(playlist['description']))
        # 歌单更新数量
        news = tools.encode((str(exist)))
        # 歌单信息表格
        playlist_info = [["歌单名称"],
                         ["歌单  ID"],
                         ["曲目数量"],
                         ["  维护  "],
                         ["播放数量"],
                         ["关注人数"],
                         ["分享次数"],
                         ["评论数量"],
                         ["  描述  "],
                         ["更新数量"],
                         ]
        playlist_info[0].append(playlist_name)
        playlist_info[1].append(playlist_id)
        playlist_info[2].append(str(count))
        playlist_info[3].append(author)
        playlist_info[4].append(play)
        playlist_info[5].append(subscribed)
        playlist_info[6].append(share)
        playlist_info[7].append(comment)
        playlist_info[8].append(description)
        playlist_info[9].append(news)
        # 合并打印歌单信息表格
        log = playlist_info
        log.append([])
        log.append([])
        log.append(["歌曲ID", "歌曲名称", "艺术家", "时长", "唱片"])
        log.append([])
        log.append([])
        log.extend(songs)
        print(AsciiTable(log).table)
        # playlist = self.curl_playlist(playlist_id)
        return playlist_info


if __name__ == '__main__':
    id_up = playlist_config.Playlist_ID_json["云音乐飙升榜"]
    id_new = playlist_config.Playlist_ID_json["云音乐新歌榜"]
    id_ori = playlist_config.Playlist_ID_json["网易原创歌曲榜"]
    id_hot = playlist_config.Playlist_ID_json["云音乐热歌榜"]
    table = [
        ["榜单", "ID"],
        ["云音乐飙升榜", str(id_up)],
        ["云音乐新歌榜", str(id_new)],
        ["网易原创歌曲榜", str(id_ori)],
        ["云音乐热歌榜", str(id_hot)]
    ]
    print(AsciiTable(table).table)
    pl = Playlist()
    pl.get_playlist(id_up)

    """
                    测试单元 begin
                    """
    """""
    if exist == 0:
        exist = 1
        table = [["字段", "类型", "内容"]]
        for var in music:
            a = tools.encode(var)
            b = tools.encode(str(type(music[var])))
            if b == "<class 'dict'>" or b == "<class 'list'>" or b == "<class 'str'>":
                c = tools.encode(str(len(music[var])))
            else:
                c = tools.encode("NULL")
            d = tools.encode(music[var].__str__())
            table.append([a, b, c, d])
        print(AsciiTable(table).table)
    """""
    """
    测试单元 end
    """