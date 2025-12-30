#!/usr/bin/env python3
"""
実行ファイル作成スクリプト
PyInstallerを使用して.exeファイルを生成

Author: Generated for user
Date: 2025-12-30
Version: 1.0.0
"""

import os
import sys
import subprocess
from pathlib import Path


def create_spec_file():
    """PyInstaller用のspecファイルを作成"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'cv2',
        'numpy',
        'PIL',
        'PIL.Image'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PNG2JPEG_Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version_file=None
)
'''
    
    with open('png2jpeg_converter.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("specファイルを作成しました: png2jpeg_converter.spec")


def build_executable():
    """実行ファイルを作成"""
    try:
        print("実行ファイル作成を開始します...")
        
        # specファイルを使用してビルド
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--onefile',
            '--windowed',
            '--name', 'PNG2JPEG_Converter',
            '--icon', 'assets/icon.ico',  # アイコンファイルが存在する場合
            'main.py'
        ]
        
        # アイコンファイルが存在しない場合は、アイコンなしでビルド
        if not os.path.exists('assets/icon.ico'):
            cmd.remove('--icon')
            cmd.remove('assets/icon.ico')
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ 実行ファイルの作成が完了しました")
        print(f"出力先: {os.path.join('dist', 'PNG2JPEG_Converter.exe')}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"ビルドエラー: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
        
    except Exception as e:
        print(f"予期しないエラー: {e}")
        return False


def create_batch_file():
    """バッチファイルを作成（テスト用）"""
    batch_content = '''@echo off
echo PNG to JPEG Converter テスト開始
echo.

REM Python環境を検出してアプリケーションを起動
python main.py

echo.
echo テスト終了
pause
'''
    
    with open('test_run.bat', 'w', encoding='shift-jis') as f:
        f.write(batch_content)
    
    print("テスト用バッチファイルを作成しました: test_run.bat")


def main():
    """メイン処理"""
    print("=== PNG to JPEG Converter 実行ファイル作成ツール ===")
    print()
    
    # 現在のディレクトリチェック
    if not os.path.exists('main.py'):
        print("エラー: main.py が見つかりません")
        return False
    
    # specファイル作成
    create_spec_file()
    
    # 実行ファイル作成確認
    response = input("\n実行ファイルを作成しますか？ (y/N): ")
    if response.lower() in ['y', 'yes']:
        success = build_executable()
        if success:
            print("\n✓ 全ての処理が完了しました！")
            print("\n使用方法:")
            print("1. GUIテスト: test_run.bat を実行")
            print("2. 配布用: dist/PNG2JPEG_Converter.exe を配布")
        else:
            print("\n✗ 実行ファイルの作成に失敗しました")
            return False
    else:
        print("specファイルが作成されました。手動で PyInstaller を実行してください。")
    
    # テスト用バッチファイル作成
    create_batch_file()
    
    return True


if __name__ == "__main__":
    main()