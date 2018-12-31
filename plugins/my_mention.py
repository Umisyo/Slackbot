# -*- coding: utf-8 -*-
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from　datetime import datetime
from libs import my_functions           # 外部関数の読み込み

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')      @発言者名: string でメッセージを送信
# message.send('string')       string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                              文字列中に':'はいらない

Kadai_ls = []

date_now = datetime.now()
def new_year(date_now, message):
    if int(date_now.month) == 1 and int(date_now.day) == 1:
        message.reply('Happy new year!')

#課題一覧
@respond_to('kadai')
def send_kadai(message):
    message.reply('課題一覧です' + str(Kadai_ls))

@listen_to(':kadai')
def method1(message):
    send_kadai(message)

#課題の追加
@listen_to(r'^:add\s+\S.*')
def add_kadai(message):
    global Kadai_ls
    text = message.body['text']
    temp, word = text.split(None, 1)
    Kadai_ls.append(word)
    msg = '課題を追加しました、現在の課題は以下の通りです\n```' + str(Kadai_ls) + '```'
    print(msg)
    message.reply(msg)

@respond_to(r'^add\s+\S.*')
def method2(message):
    add_kadai(message)

#リセット
@respond_to('reset')
def reset_kadai(message):
    global Kadai_ls
    Kadai_ls.clear()
    msg1 = '課題をリセットしました' 
    print(msg1)
    message.reply(msg1)
    

@listen_to(':reset')
def method3(message):
    reset_kadai(message)

#任意の課題の削除
@respond_to(r'^delete\s+\S.*')
def delete_kadai(message):
    global Kadai_ls
    num = message.body['text']
    temp, delete_num = num.split(None, 1)

    if delete_num.isdecimal() == True:
        msg2 = 次の課題を削除しました```' + str(Kadai_ls[int(delete_num)]) + '```'
        print(msg2)
        message.reply(msg2)
        del Kadai_ls[int(delete_num)]

    else:
        message.reply('数字以外は入力しないでください')

@listen_to(r'^:delete\s+\S.*')
def method4(message):
    delete_kadai(message)

#help
@respond_to('help')
def help_kadai(message):
    message.reply('これは課題管理botです、次のコマンドで以下のことができます。\n```' + 
                  'kadai - 現在の課題一覧を表示します。\n' + 
                  'add 〇〇 - 任意の課題を登録します。\n' + 
                  'delete X - 課題リストの任意の番号の部分を削除します。リストは先頭が0です。\n' +
                  'reset - 課題をすべて削除します。\n' + 
                  'help - 使い方を表示します\n'+
                  'source - このbotのコードが置いてあるgithubのリンクを送ります。センスのないコードが置いてあるので見ないでね。\n' +
                  'コマンドは、直接リプライを送るか、先頭に:をつけてチャットで入力してください。\n' +
                  '```')

@listen_to(':help')
def method5(message):
    help_kadai(message)

#コードを見せる
@respond_to('source')
def send_source(message):
    message.reply('僕のすべてを見て/// https://github.com/Umisyo/Slackbot')

@listen_to(':source')
def method6(message):
    send_source(message)
