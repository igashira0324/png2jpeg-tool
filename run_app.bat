@echo off
chcp 65001 >nul
echo ===============================================
echo   高品質PNG to JPEG変換ツール
echo   アプリケーション起動テスト
echo ===============================================
echo.

REM Pythonがインストールされているかチェック
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pythonが見つかりません。Python 3.10以上をインストールしてください。
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
    echo ❌ テストに失敗しました。
    pause
    exit /b 1
)

echo.
echo 🎯 アプリケーションを起動します...
echo.

REM メインアプリケーション起動
python main.py

echo.
echo アプリケーションが正常に終了されました。
pause