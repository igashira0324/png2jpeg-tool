@echo off
chcp 65001 >nul
echo ===============================================
echo   🎯 高品質PNG to JPEG変換ツール
echo   📱 アプリケーション起動
echo ===============================================
echo.
echo 📋 このバッチファイルは：
echo    ✓ アプリをすぐに使うため
echo    ✓ Python環境で動作
echo    ✓ 今日からの使用向け
echo.

REM Pythonがインストールされているかチェック
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pythonが見つかりません。Python 3.10以上をインストールしてください。
    echo 💡 Pythonダウンロード: https://python.org
    pause
    exit /b 1
)

REM 依存関係チェック
echo 📦 依存関係をチェック中...
pip show PyQt6 >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyQt6が見つかりません。依存関係をインストールします...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ 依存関係のインストールに失敗しました。
        echo 💡 手動で pip install -r requirements.txt を実行してください
        pause
        exit /b 1
    )
)

echo ✓ 依存関係チェック完了
echo.

REM 動作テスト実行
echo 🧪 動作テストを実行中...
python test_app.py
if errorlevel 1 (
    echo ❌ テストに失敗しました。依存関係を確認してください。
    pause
    exit /b 1
)

echo.
echo 🚀 アプリケーションを起動します...
echo.

REM メインアプリケーション起動
python main.py

echo.
echo ✅ アプリケーションが正常に終了されました。
echo.
echo 💡 次回使用時も、このバッチファイルをダブルクリックしてください！
pause