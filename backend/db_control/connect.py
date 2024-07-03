# SQLiteのDBに接続

import platform  # プラットフォームに依存した情報を取得するためのモジュールをインポートしています。
# print(platform.uname())

from sqlalchemy import create_engine  # SQLAlchemyライブラリからcreate_engine関数をインポートしています。create_engineはデータベースエンジンを作成し、データベースとの接続を管理します。
import sqlalchemy  # SQLAlchemyライブラリ全体をインポートしています。これにより、SQLAlchemyの機能をすべて利用できます。
import os  # OSモジュールをインポートして、ファイルシステムに関する操作を行うことができます。


main_path = os.path.dirname(os.path.abspath(__file__))
# __file__変数は現在のスクリプトファイルのパスを表します。
# os.path.abspath(__file__)はそのパスを絶対パスで取得し、os.path.dirname()でそのディレクトリのパスを取得しています。
# これにより、スクリプトのあるディレクトリの絶対パスがmain_pathに格納されます。

path = os.chdir(main_path)  # os.chdir()関数を使ってカレントディレクトリをmain_pathに設定しています。これにより、スクリプトの実行ディレクトリが設定されます。

# print(path)
engine = create_engine("sqlite:///step4.db", echo=True)