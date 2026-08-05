# IIDX SP☆12 OPTION MANAGER

`sp12.iidx.app` の公開APIから、beatmania IIDX のSP☆12楽曲のみを取得して表示するブラウザツールです。

## GitHub Pagesで公開する方法

1. このフォルダ内の `index.html` と `README.md` をGitHubリポジトリ直下へアップロードします。
2. GitHubのリポジトリで **Settings** → **Pages** を開きます。
3. **Build and deployment** の Source を **Deploy from a branch** にします。
4. Branchを `main`、フォルダを `/(root)` にして **Save** を押します。
5. 表示されたGitHub PagesのURLを開きます。

## データについて

- SP☆12のみを取得します。
- ☆11用データは取得しません。
- ノマゲ／ハード難易度表を切り替えられます。
- 選択したオプションはブラウザの `localStorage` に保存されます。
- バックアップの保存と読込に対応しています。

## ファイル構成

```text
index.html  アプリ本体
README.md   説明
```
