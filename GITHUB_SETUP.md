# GitHubリポジトリ作成ガイド

## 📋 プロジェクト概要
**リポジトリ名**: `png2jpeg-tool`
**URL**: https://github.com/igashira0324/png2jpeg-tool

## 🚀 GitHubリポジトリ作成手順

### 1. GitHubリポジトリ作成
1. GitHub (https://github.com) にログイン
2. 右上の「+」ボタンをクリック → 「New repository」
3. Repository name: `png2jpeg-tool` を入力
4. Description: `Windows用高品質PNG to JPEG/WebP変換ツール - CustomTkinter製モダンGUI` を入力
5. Public/Private: ご希望に合わせて選択
6. 「Create repository」ボタンをクリック

### 2. ローカルリポジトリ初期化

現在のプロジェクトディレクトリで以下のコマンドを実行：

```bash
# Gitリポジトリの初期化
git init

# メインファイルとディレクトリを追加
git add main.py requirements.txt README.md src/ assets/ *.bat

# 最初のコミット
git commit -m "Initial commit: High-quality PNG to JPEG/WebP converter tool

- CustomTkinter-based modern GUI
- Dual format support (JPEG/WebP)
- Drag & drop functionality
- Batch processing capability
- File size and quality control
- Preview functionality
- Progress tracking
- Windows optimized"
```

### 3. リモートリポジトリ связать

```bash
# リモートリポジトリを追加
git remote add origin https://github.com/igashira0324/png2jpeg-tool.git

# メイン branchesを作成してコミット
git branch -M main

# リモートリポジトリにプッシュ
git push -u origin main
```

## 📁 プロジェクト構造

```
png2jpeg-tool/
├── main.py                    # アプリケーション起動ポイント
├── requirements.txt           # 依存関係一覧
├── README.md                  # プロジェクトドキュメント
├── GITHUB_SETUP.md           # このファイル
│
├── src/                       # ソースコード
│   ├── main_window.py        # メインウィンドウGUI
│   ├── image_converter.py    # 画像変換エンジン
│   └── preview_widget.py     # プレビュー機能
│
├── assets/                    # アセットフォルダ
├── build/                    # PyInstaller作業フォルダ
├── test/                     # テスト画像フォルダ
│
├── *.bat                     # Windows用起動バッチ
└── build_exe.py             # PyInstaller実行スクリプト
```

## 🔧 依存関係

requirements.txt:
```
customtkinter>=5.4.0
opencv-python>=4.8.0
Pillow>=10.0.0
numpy>=1.24.0
pyinstaller>=5.13.0
windnd>=1.2.8
```

## 📝 プロジェクト情報

### バージョン: v2.1.1
### 最終更新: 2025-12-30
### 対応OS: Windows 10/11
### Python要件: 3.10+

## 🚀 機能一覧

- ✅ **Dual Format Support**: JPEG/WebP選択式変換
- ✅ **モダンUI**: ダークモード、 компакт レイアウト
- ✅ **ファイル選択**: ドラッグ＆ドロップ・ファイル指定・フォルダ選択
- ✅ **プレビュー機能**: 変換前後の画像比較
- ✅ **バッチ処理**: 複数ファイルの同時変換
- ✅ **品質制御**: ファイルサイズ制限・品質設定
- ✅ **進捗表示**: リアルタイム進捗バー
- ✅ **エラーハンドリング**: 堅牢な例外処理

## 📄 ライセンス

MIT License - 商用・非商用利用可

## 🔗 実行方法

### 開発環境
```bash
# 依存関係インストール
pip install -r requirements.txt

# アプリケーション起動
python main.py
```

### 実行ファイル作成
```bash
# PyInstallerで実行ファイル作成
python build_exe.py

# またはWindows用バッチ
今日からアプリを使う.bat
```

## 📊 技術スタック

- **Python 3.10+**: メイン開発言語
- **CustomTkinter 5.4.0+**: モダンGUIフレームワーク
- **OpenCV 4.8.1**: 高品質画像処理エンジン
- **Pillow 11.3.0**: 画像ファイル操作
- **NumPy 1.24.0**: 数値計算処理
- **windnd**: Windows用ドラッグ&ドロップ

## 🎯 今後の拡張予定

- 他の画像フォーマット対応（TIFF, BMP等）
- 画像リサイズ機能追加
- バッチ処理の並列処理最適化
- 設定ファイル保存機能
- テーマ選択機能追加

---

**✨ 高品質画像変換ツールで、より効率的な画像処理をお楽しみください！ ✨**