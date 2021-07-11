# File Name		: consumers.py
# Version	    : V2.0
# Designer		: 和合雅輝
# Date			: 2021.06.08
# Purpose      	: チャット機能に関する処理の記述
#
# # Revision :
# V1.0 : 和合雅輝, 2021.06.08
# V1.1 : 平澤巧望, 2021.06.20 投票機能の実装
# V2.0 : 松岡修平, 2021.06.20 司会者決定機能の実装

import json, os, sys
from re import S
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync  # async_to_sync() : 非同期関数を同期的に実行する際に使用する。
import datetime
#司会者決定するために参加車情報を取得するために使う
from .models import JoinChatRoom
import random
from asgiref.sync import sync_to_async
#非同期関数で同期関数を使用するために制限を解除
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

USERNAME_SYSTEM = '*system*'

# ChatConsumerクラス: WebSocketからの受け取ったものを処理するクラス
class ChatConsumer(AsyncWebsocketConsumer):

    # ルーム管理（インスタンス変数ではなく、インスタンス間で使用可能なクラス変数）
    rooms = None

    # コンストラクタ
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # クラス変数の初期化（最初のインスタンスが生成されたときのみ実施する）
        if ChatConsumer.rooms is None:
            ChatConsumer.rooms = {}  # 空の連想配列
        self.strGroupName = ''
        self.strUserName = ''

    # WebSocket接続時の処理
    async def connect(self):
        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        await self.accept()

    # WebSocket切断時の処理
    async def disconnect(self, close_code):
        # チャットからの離脱
        await self.leave_chat()

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    async def receive(self, text_data):
        # 受信データをJSONデータに復元
        text_data_json = json.loads(text_data)

        # チャットへの参加時の処理
        if ('join' == text_data_json.get('data_type')):
            # ユーザー名をクラスメンバー変数に設定
            self.strUserName = text_data_json['username']
            # ルーム名の取得
            strRoomName = text_data_json['roomname'];
            # チャットへの参加
            await self.join_chat(strRoomName)

        # チャットからの離脱時の処理
        elif ('leave' == text_data_json.get('data_type')):
            # チャットからの離脱
            await self.leave_chat()
        
        # 投票機能開始 or 終了時の処理
        elif ('vote' == text_data_json.get('data_type')):
            if (ChatConsumer.rooms[self.strGroupName]['vote_state'] == True):
                await self.end_vote() # 終了
            else:
                await self.start_vote() # 開始
        
        # 「〇」ボタンが押された時の処理
        elif ('vote_ok' == text_data_json.get('data_type')):
            await self.ok_vote()
        
        # 「×」ボタンが押された時の処理
        elif ('vote_ng' == text_data_json.get('data_type')):
            await self.ng_vote()
        
        # 「△」ボタンが押された時の処理
        elif ('vote_cd' == text_data_json.get('data_type')):
            await self.cd_vote()
        
        # 「司会決定」ボタンが押された時の処理
        elif ('sikai' == text_data_json.get('data_type')):
            await self.sikai_kettei()

        # メッセージ受信時の処理
        else:
            # メッセージの取り出し
            strMessage = text_data_json['message']
            # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
            data = {
                'type': 'chat_message',  # 受信処理関数名
                'message': strMessage,  # メッセージ
                'username': self.strUserName,  # ユーザー名
                'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
            }
            await self.channel_layer.group_send(self.strGroupName, data)

    # 投票開始処理
    async def start_vote(self):
        ChatConsumer.rooms[self.strGroupName]['vote_state'] = True
        ChatConsumer.rooms[self.strGroupName]['ok'] = 0
        ChatConsumer.rooms[self.strGroupName]['ng'] = 0
        ChatConsumer.rooms[self.strGroupName]['cd'] = 0
        data = {
            'type': 'chat_message',  # 受信処理関数名
            'message': '投票を開始しました（〇×△ボタンで回答してください）',  # メッセージ
            'username': USERNAME_SYSTEM,  # ユーザー名
            'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
        }
        await self.channel_layer.group_send(self.strGroupName, data)

    # 「〇」ボタンが押された時の処理
    async def ok_vote(self):
        if (ChatConsumer.rooms[self.strGroupName]['vote_state'] == True):
            # 投票時間中なら「〇」の数をカウントアップ
            ChatConsumer.rooms[self.strGroupName]['ok'] += 1
        else: # 投票時間中でなければメッセージとして「〇」を送信
            data = {
                'type': 'chat_message',  # 受信処理関数名
                'message': '〇',  # メッセージ
                'username': self.strUserName,  # ユーザー名
                'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
            }
            await self.channel_layer.group_send(self.strGroupName, data)

    # 「×」ボタンが押された時の処理
    async def ng_vote(self):
        if (ChatConsumer.rooms[self.strGroupName]['vote_state'] == True):
            # 投票時間中なら「×」の数をカウントアップ
            ChatConsumer.rooms[self.strGroupName]['ng'] += 1
        else: # 投票時間中でなければメッセージとして「×」を送信
            data = {
                'type': 'chat_message',  # 受信処理関数名
                'message': '×',  # メッセージ
                'username': self.strUserName,  # ユーザー名
                'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
            }
            await self.channel_layer.group_send(self.strGroupName, data)

    # 「△」ボタンが押された時の処理
    async def cd_vote(self):
        if (ChatConsumer.rooms[self.strGroupName]['vote_state'] == True):
            # 投票時間中なら「△」の数をカウントアップ
            ChatConsumer.rooms[self.strGroupName]['cd'] += 1
        else: # 投票時間中でなければメッセージとして「△」を送信
            data = {
                'type': 'chat_message',  # 受信処理関数名
                'message': '△',  # メッセージ
                'username': self.strUserName,  # ユーザー名
                'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
            }
            await self.channel_layer.group_send(self.strGroupName, data)

    async def end_vote(self):
        ChatConsumer.rooms[self.strGroupName]['vote_state'] = False
        strMessage = '投票を終了しました（〇：' + str(ChatConsumer.rooms[self.strGroupName]['ok']) + ', ×：' + str(ChatConsumer.rooms[self.strGroupName]['ng']) + ', △：' + str(ChatConsumer.rooms[self.strGroupName]['cd']) + '）'
        data = {
            'type': 'chat_message',  # 受信処理関数名
            'message': strMessage,  # メッセージ
            'username': USERNAME_SYSTEM,  # ユーザー名
            'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
        }
        await self.channel_layer.group_send(self.strGroupName, data)

    # 拡散メッセージ受信時の処理
    # （self.channel_layer.group_send()の結果、グループ内の全コンシューマーにメッセージ拡散され、各コンシューマーは本関数で受信処理します）
    
    async def sikai_kettei(self):
            name = self.strGroupName
            obj = JoinChatRoom.objects.filter(room_name=name)
            #ランダムで司会者の名前抽出
            sikai = random.choice(obj)
            reader = sikai.username
            data = {
                'type': 'chat_message',  # 受信処理関数名
                'message': '司会者は「　' + reader + '　」です！',  # メッセージ
                'username': self.strUserName,  # ユーザー名
                'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
            }
            await self.channel_layer.group_send(self.strGroupName, data)

    async def chat_message(self, data):
        data_json = {
            'message': data['message'],
            'username': data['username'],
            'datetime': data['datetime'],
        }

        # WebSocketにメッセージを送信します。
        # （送信されたメッセージは、ブラウザ側のJavaScript関数のsocketChat.onmessage()で受信処理されます）
        # JSONデータをテキストデータにエンコードして送ります。
        await self.send(text_data=json.dumps(data_json))

    # チャットへの参加
    async def join_chat(self, strRoomName):
        # グループに参加
        # self.strGroupName = 'chat'
        self.strGroupName = 'chat_%s' % strRoomName
        await self.channel_layer.group_add(self.strGroupName, self.channel_name)

        # 参加者数の更新
        room = ChatConsumer.rooms.get(self.strGroupName)
        if (None == room):
            # ルーム管理にルーム追加
            ChatConsumer.rooms[self.strGroupName] = {
                'participants_count': 1,
                'vote_state': False, # 投票中かどうか
                'vote_ok': 0, # 投票：〇をカウント
                'vote_ng': 0, # 投票：×をカウント
                'vote_cd': 0} # 投票：△をカウント
        else:
            room['participants_count'] += 1
        # システムメッセージの作成
        strMessage = '"' + self.strUserName + '" joined. there are ' + str(
            ChatConsumer.rooms[self.strGroupName]['participants_count']) + ' participants'
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'chat_message',  # 受信処理関数名
            'message': strMessage,  # メッセージ
            'username': USERNAME_SYSTEM,  # ユーザー名
            'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
        }
        await self.channel_layer.group_send(self.strGroupName, data)

    # チャットからの離脱
    async def leave_chat(self):
        if ('' == self.strGroupName):
            return

        # グループから離脱
        await self.channel_layer.group_discard(self.strGroupName, self.channel_name)

        # 参加者数の更新
        ChatConsumer.rooms[self.strGroupName]['participants_count'] -= 1
        # システムメッセージの作成
        strMessage = '"' + self.strUserName + '" left. there are ' + str(
            ChatConsumer.rooms[self.strGroupName]['participants_count']) + ' participants'
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'chat_message',  # 受信処理関数名
            'message': strMessage,  # メッセージ
            'username': USERNAME_SYSTEM,  # ユーザー名
            'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
        }
        await self.channel_layer.group_send(self.strGroupName, data)

        # 参加者がゼロのときは、ルーム管理からルームの削除
        if (0 == ChatConsumer.rooms[self.strGroupName]['participants_count']):
            del ChatConsumer.rooms[self.strGroupName]

        # ルーム名を空に
        self.strGroupName = ''