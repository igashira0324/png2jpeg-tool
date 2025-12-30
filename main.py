#!/usr/bin/env python3
"""
高品質PNG to JPEG変換ツール
CustomTkinter版 Windows用GUIアプリケーション

Author: Generated for user
Date: 2025-12-30
Version: 2.0.0 (CustomTkinter)
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
# import tkinterdnd2 as tkdnd  # windndに切り替えて削除

# アプリケーションフォルダをパスに追加
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(app_dir, 'src'))

from src.main_window import MainWindow


def main():
    """メインアプリケーション実行"""
    # CustomTkinterの外観モード設定（ダークモード）
    ctk.set_appearance_mode("dark")  # "light", "dark", "system" -> ダークモード
    ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue" -> ダークブルー
    
    # CustomTkinterアプリ作成（ドラッグ＆ドロップ対応）
    try:
        # 標準のCTkアプリ作成（windnd対応）
        app = ctk.CTk()
        app.title("高品質PNG to JPEG変換ツール v2.1")
        
        # ベストエフォートのウィンドウサイズ計算
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        
        # 画面サイズの53%（80%×2/3）をベストエフォートとして使用
        best_width = int(screen_width * 0.53)  # 0.8 * 2/3 = 0.53
        best_height = int(screen_height * 0.73)  # 0.75 -> 0.73に調整
        
        # 最小サイズと最大サイズを設定
        min_width, min_height = 800, 550  # 600 -> 550にさらに縮小
        max_width, max_height = screen_width - 100, screen_height - 100
        
        # ベストエフォートサイズを制限
        final_width = max(min_width, min(best_width, max_width))
        final_height = max(min_height, min(best_height, max_height))
        
        app.geometry(f"{final_width}x{final_height}")
        app.resizable(True, True)
        
        # メインウィンドウ作成・表示
        window = MainWindow(app)
        window.pack(fill="both", expand=True, padx=20, pady=20)
        
        # アプリケーション実行
        app.mainloop()
        
    except Exception as e:
        print(f"CTk初期化エラー: {e}")
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        messagebox.showerror("エラー", f"アプリケーションの起動に失敗しました:\n{str(e)}")
        sys.exit(1)
