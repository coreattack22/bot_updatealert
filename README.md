# Bot

特定ページを一日ごとにスクレイピングして、更新があった分だけ

LINEBotで通知するサービスです。

今のところlivedoorBlogとWantedlyに対応

(参考にさせていただきました😍→　https://qiita.com/mtdkki/items/831a35666b35b8e11798)


https://shareshortbot.herokuapp.com/ 


##使い方

このソースコードをherokuとかにデプロイする

GoogleAppsScriptにgas.jsのコードをそのまま貼り付けて、トリガー(時計のマーク)

で任意の時間を指定して実行する(Herokuのトリガーもあるが、動かすと無料枠圧迫するので)

![Demo](https://user-images.githubusercontent.com/34805754/42837630-96ea96a8-8a39-11e8-93a9-d6a3088e503d.png)

###その他

時間があればもっとちゃんとした体裁に書き直したい・・・