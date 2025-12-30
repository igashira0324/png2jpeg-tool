@echo off
chcp 65001 >nul
echo ===============================================
echo   📦 高品質PNG to JPEG変換ツール
echo   🔧 exeファイル作成ツール
echo ===============================================
echo.
echo 📋 このバッチファイルは：
echo    ✓ Python不要の.exeファイルを作る
echo    ✓ 配布用パッケージ作成
echo    ✓ 他人に渡す時使用
echo    ⚠️  数分かかる場合があります
echo.

REM PyInstallerがインストールされているかチェック
echo 📦 PyInstallerをチェック中...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyInstallerが見つかりません。インストールします...
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ PyInstallerのインストールに失敗しました。
        pause
        exit /b 1
    )
)

echo ✓ PyInstallerチェック完了
echo.

REM 依存関係チェック
echo 📋 依存関係をチェック中...
pip install -r requirements.txt --quiet
echo ✓ 依存関係インストール完了
echo.

REM 実行ファイル作成開始
echo 🏗️  実行ファイルを作成中...
echo    ⏳ 時間：約3-5分
echo    💾 容量：約100-200MB
echo.

pyinstaller --onefile --windowed --name "PNG2JPEG_Converter" main.py

if errorlevel 1 (
    echo ❌ 実行ファイルの作成に失敗しました。
    echo.
    echo 💡 ヒント:
    echo    - アンチウイルスソフトの一時停止
    echo    - 管理者権限での実行
    echo    - 十分な空き容量の確認（最低1GB）
    pause
    exit /b 1
)

echo.
echo ✅ 実行ファイル作成完了！
echo.
echo 📁 作成されたファイル:
echo    📂 dist\PNG2JPEG_Converter.exe
echo.
echo 🚀 使用方法:
echo    📂 dist\PNG2JPEG_Converter.exe をダブルクリック
echo    💻 Python不要で動作します
echo.

REM distフォルダの存在確認
if exist "dist\PNG2JPEG_Converter.exe" (
    echo 🎉 準備完了！exeファイルが使用可能です。
    echo.
    echo 📦 配布用ファイル:
    echo    ファイル名: PNG2JPEG_Converter.exe
    echo    保存場所: dist\フォルダ内
    echo    容量: 
    for %%A in ("dist\PNG2JPEG_Converter.exe") do echo     %%~zA bytes
    echo.
    echo 💡 他人に渡す際は、dist\PNG2JPEG_Converter.exe をコピーしてください
) else (
    echo ❌ exeファイルが見つかりません。作成に失敗した可能性があります。
)

pause