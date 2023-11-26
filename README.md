# statech-interview-backend
スタテクの選考を受けて合格するまでの物語

## ローカルでの起動方法

### Python環境のセットアップ
```shell
$ make setup-poetry
```
- 「Author」パートは"n"を入力してEnter。それ以外のパートは全てEnterのみ。

### FastAPIのインストール
```shell
$ make setup
```

### API起動
```shell
$ make up
```
- APPコンテナとMySQLコンテナが立ち上がる<br>
- Uvicornが立ち上がるので、そこに表示されたURL（[http://0.0.0.0:8000](http://0.0.0.0:8000)）に/docsをつけるとSwaggerUI上でAPIの挙動を確認できる。

### コンテナ終了
```shell
$ make down
```

### テーブル作成（最初の1回のみ）
```shell
$ make create
```

### 1からコンテナ立ち上げ
```shell
$ make build
```
- Docker環境に関わるコードを変更し、イメージのビルドから行う必要がある場合に使う