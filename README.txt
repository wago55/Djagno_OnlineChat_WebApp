
01班：オンラインディスカッション支援システム

ローカル環境で実行する場合
　【　ローカル環境で実行するための事前準備　】
　　　　Redisのインストール（Windowsの場合）
	　　　１．「https://www.memurai.com/」からインストーラをダウンロード
	　　　２．インストーラを起動し，表示に従ってインストール（標準のままでOK）
	　　　※　Mac環境では
	          https://qiita.com/sawa-@github/items/1f303626bdc219ea8fa1
          	を参照
　　　　　python環境の準備
	　　　pip install django channels bootstrap4 channels_redis

　【　アプリケーション実行方法　】
	  1. SouraceCode01班.zip」をダウンロード・解凍
	  2. その中の「onlin_chat_sit」のディレクトリに移動
	  3. online_chat_sit/online_discussion/settings.pyの157-162行目までをコメントアウトする.
      4. 164-168行目のコメントアウトを外す.
	  5. コマンド「python manage.py runserver」を実行
	  6. ブラウザで「http://127.0.0.1:8000/accounts/home/」にアクセス
	　※　チャット機能がうまくいかない場合は…
　　　 再度Redisのインストーラを実行し，「Repair」してみる

本番環境で実行する場合
     「https://onlinechatdiscussion.herokuapp.com/accounts/home/」 にアクセス.

