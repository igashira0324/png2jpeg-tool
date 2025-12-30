#!/usr/bin/env python3
"""
メインウィンドウクラス
CustomTkinter版 高品質PNG to JPEG変換ツールのGUI
 компакт版 UI

Author: Generated for user
Date: 2025-12-30
Version: 2.1.1 (CustomTkinter - Compact)
"""

import os
import sys
import threading
from pathlib import Path
from typing import List, Optional
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import windnd

from image_converter import ImageConverter
from preview_widget import PreviewWidget


class ConversionThread:
    """画像変換処理クラス"""
    
    def __init__(self, files: List[str], output_dir: str, 
                 max_size_mb: int, quality: int, output_format: str = "JPEG", callback=None):
        self.files = files
        self.output_dir = output_dir
        self.max_size_mb = max_size_mb
        self.quality = quality
        self.output_format = output_format
        self.callback = callback
        self.converter = ImageConverter()
        
    def start(self):
        """変換処理開始"""
        def conversion_worker():
            total_files = len(self.files)
            
            for i, file_path in enumerate(self.files):
                try:
                    # ファイル名生成
                    if self.output_format.upper() == "WEBP":
                        file_name = Path(file_path).stem + '.webp'
                    else:
                        file_name = Path(file_path).stem + '.jpg'
                    output_path = os.path.join(self.output_dir, file_name)
                    
                    # 変換実行
                    if self.output_format.upper() == "WEBP":
                        success = self.converter.convert_to_webp(
                            file_path, output_path, self.max_size_mb, self.quality
                        )
                    else:
                        success = self.converter.convert_to_jpeg(
                            file_path, output_path, self.max_size_mb, self.quality
                        )
                    
                    if success:
                        if self.callback:
                            self.callback("progress", i + 1, total_files)
                            self.callback("processed", file_path, output_path)
                    else:
                        if self.callback:
                            self.callback("error", f"変換失敗: {file_path}")
                    
                except Exception as e:
                    if self.callback:
                        self.callback("error", f"エラー: {file_path} - {str(e)}")
            
            if self.callback:
                self.callback("completed", None, None)
        
        thread = threading.Thread(target=conversion_worker, daemon=True)
        thread.start()
        return thread


class MainWindow(ctk.CTkFrame):
    """メインウィンドウ（ компакт版 ）"""
    
    def __init__(self, master):
        super().__init__(master)
        self.selected_files = []
        self.conversion_thread = None
        self.current_file_index = 0
        self.converter = ImageConverter()
        
        self.setup_styles()
        self.setup_ui()
        self.setup_callbacks()
        self.setup_responsive_handlers()
        
    def setup_styles(self):
        """スタイルとフォントのセットアップ（元サイズに戻す）"""
        # フォントサイズを元に戻す
        self.title_font = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")       # 40 -> 20
        self.group_title_font = ctk.CTkFont(family="Segoe UI", size=15, weight="bold") # 30 -> 15
        self.label_font = ctk.CTkFont(family="Segoe UI", size=13)                       # 26 -> 13
        self.button_font = ctk.CTkFont(family="Segoe UI", size=13, weight="bold")       # 26 -> 13
        self.info_font = ctk.CTkFont(family="Segoe UI", size=11)                        # 22 -> 11
        
        # モダンな色設定
        self.accent_color = "#3b82f6"     # モダンなブルー
        self.hover_color = "#2563eb"      # ホバー時のブルー
        self.success_color = "#10b981"    # グリーン
        self.error_color = "#ef4444"      # レッド
        self.warning_color = "#f59e0b"    # オレンジ
        self.high_contrast_text = "#ffffff"  # 高コントラスト白文字
        self.light_gray_text = "#f5f5f5"     # 明るい灰色文字
        
    def setup_ui(self):
        """UIコンポーネントのセットアップ（スクロール対応版）"""
        self.pack(fill="both", expand=True)

        # スクロール可能なメインコンテンツフレーム
        self.main_scrollable = ctk.CTkScrollableFrame(self)
        self.main_scrollable.pack(fill="both", expand=True, padx=8, pady=8)

        # --- 上段: 設定とファイル選択（横並び） ---
        top_container = ctk.CTkFrame(self.main_scrollable, fg_color="transparent")
        top_container.pack(fill="x", padx=8, pady=8)

        # 左: 変換設定
        self.setup_settings_panel(top_container)

        # 右: ファイル選択（レイアウト変更対応）
        self.setup_file_selection_panel(top_container)

        # --- 中段: プレビューエリア ---
        self.setup_preview_area(self.main_scrollable)

        # --- 下段: ログ ---
        self.setup_bottom_area(self.main_scrollable)
        
    def setup_settings_panel(self, parent):
        """変換設定パネル（幅縮小版：現在の2/3程度）"""
        self.settings_frame = ctk.CTkFrame(parent, width=400)  # 幅を制限
        self.settings_frame.pack(side="left", fill="both", expand=False, padx=(0, 8))
        self.settings_frame.pack_propagate(False)
        
        title = ctk.CTkLabel(self.settings_frame, text="⚙️ 変換設定", font=self.group_title_font)
        title.pack(pady=(12, 8))                  # 15,10 -> 12,8
        
        # ファイルサイズ制限
        size_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        size_frame.pack(fill="x", padx=12, pady=3)  # 15,5 -> 12,3
        
        size_label = ctk.CTkLabel(size_frame, text="最大サイズ:", font=self.label_font, width=80, anchor="w")  # 100 -> 80
        size_label.pack(side="left")
        
        self.size_slider = ctk.CTkSlider(
            size_frame, from_=1, to=10, number_of_steps=9,
            command=self.on_size_change
        )
        self.size_slider.set(4)
        self.size_slider.pack(side="left", fill="x", expand=True, padx=8)  # 10 -> 8
        
        self.size_value_label = ctk.CTkLabel(size_frame, text="4 MB", font=self.label_font, width=50)  # 60 -> 50
        self.size_value_label.pack(side="right")
        
        # JPEG品質
        quality_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        quality_frame.pack(fill="x", padx=12, pady=3)  # 15,5 -> 12,3
        
        quality_label = ctk.CTkLabel(quality_frame, text="JPEG品質:", font=self.label_font, width=80, anchor="w")  # 100 -> 80
        quality_label.pack(side="left")
        
        self.quality_slider = ctk.CTkSlider(
            quality_frame, from_=1, to=100, number_of_steps=99,
            command=self.on_quality_change
        )
        self.quality_slider.set(100)
        self.quality_slider.pack(side="left", fill="x", expand=True, padx=8)  # 10 -> 8
        
        self.quality_value_label = ctk.CTkLabel(quality_frame, text="100%", font=self.label_font, width=50)  # 60 -> 50
        self.quality_value_label.pack(side="right")
        

        
        # 説明（ компакт版 ）
        quality_info = ctk.CTkLabel(
            self.settings_frame,
            text="💡 品質が高いほど高品質ですが、ファイルサイズが大きくなります。",
            font=self.info_font, text_color="#e5e5e5", wraplength=300  # 666666 -> e5e5e5 (ダークモード対応)
        )
        quality_info.pack(pady=3)                # 5 -> 3
        
        # 出力先
        output_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        output_frame.pack(fill="x", padx=12, pady=(3, 12))

        output_label = ctk.CTkLabel(output_frame, text="出力フォルダ:", font=self.label_font, anchor="w", width=80)
        output_label.pack(side="left")

        self.default_output_path = str(Path.home() / "Desktop")
        self.output_path_label = ctk.CTkLabel(
            output_frame, text=self.default_output_path, font=self.info_font,
            fg_color="#000000", text_color="#ffffff", corner_radius=6, height=30,
            anchor="w", padx=8
        )
        self.output_path_label.pack(side="left", fill="x", expand=True, padx=8)

        self.select_output_btn = ctk.CTkButton(
            output_frame, text="参照", font=self.button_font, width=80, height=30,
            command=self.select_output_folder,
            fg_color="#3b82f6", hover_color="#2563eb", text_color="#ffffff",
            corner_radius=6
        )
        self.select_output_btn.pack(side="right")

        # 下部コントロールエリアに2つの変換ボタンを配置
        convert_btn_frame = ctk.CTkFrame(self.settings_frame, fg_color="transparent")
        convert_btn_frame.pack(fill="x", padx=12, pady=(8, 12))

        # 下段: ボタン用コンテナ
        btns_container = ctk.CTkFrame(convert_btn_frame, fg_color="transparent")
        btns_container.pack(fill="x")
        
        self.convert_jpeg_btn = ctk.CTkButton(
            btns_container, text="🚀 JPEGに変換", font=self.button_font,
            width=120, height=35, command=self.start_conversion_jpeg
        )
        self.convert_jpeg_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        
        self.convert_webp_btn = ctk.CTkButton(
            btns_container, text="🚀 WebPに変換", font=self.button_font,
            width=120, height=35, command=self.start_conversion_webp
        )
        self.convert_webp_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))
        
    def setup_file_selection_panel(self, parent):
        """ファイル選択パネル（レイアウト変更版：左側欄、右側3ボタン縦配置）"""
        self.file_frame = ctk.CTkFrame(parent)
        self.file_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

        title = ctk.CTkLabel(self.file_frame, text="📁 ファイル選択", font=self.group_title_font)
        title.pack(pady=(12, 8))

        # メインコンテナ（左右分割）
        file_container = ctk.CTkFrame(self.file_frame, fg_color="transparent")
        file_container.pack(fill="both", expand=True, padx=15, pady=8)

        # 左側: ドラッグ&ドロップエリア（360pxに調整）
        left_area = ctk.CTkFrame(file_container, fg_color="transparent", width=360)  # 400 -> 360
        left_area.pack(side="left", fill="y", expand=False, padx=(0, 4))
        left_area.pack_propagate(False)

        # ドラッグ&ドロップエリア（標準tkinter Frameを使用）
        drop_container = tk.Frame(left_area, bg="#2a2a2a", highlightthickness=1, highlightbackground="#3a3a3a")
        drop_container.pack(fill="both", expand=True, padx=2, pady=2)

        self.drop_area = ctk.CTkLabel(
            drop_container, 
            text="PNGファイルをここに\nドラッグ&ドロップ",
            font=self.label_font, text_color="#e5e5e5", fg_color="transparent",
            corner_radius=4, height=100, anchor="center"
        )
        self.drop_area.pack(fill="both", expand=True)
        
        # ドラッグ&ドロップ機能のバインド
        self.setup_drop_handlers(drop_container)

        # 右側: 3つのボタンを縦配置
        right_buttons = ctk.CTkFrame(file_container, fg_color="transparent")
        right_buttons.pack(side="right", fill="y", expand=False, padx=(4, 0))

        self.select_files_btn = ctk.CTkButton(
            right_buttons, text="ファイル選択", font=self.button_font, 
            height=35, command=self.select_files
        )
        self.select_files_btn.pack(fill="x", pady=(0, 6))

        self.select_folder_btn = ctk.CTkButton(
            right_buttons, text="フォルダ選択", font=self.button_font, 
            height=35, command=self.select_folder
        )
        self.select_folder_btn.pack(fill="x", pady=3)

        self.clear_files_btn = ctk.CTkButton(
            right_buttons, text="クリア", font=self.button_font, 
            fg_color="#ef4444", hover_color="#dc2626", height=35,  # dc3545 -> ef4444, c82333 -> dc2626
            command=self.clear_files
        )
        self.clear_files_btn.pack(fill="x", pady=(6, 0))

        # ファイル数表示（クリアボタンの下）
        self.file_count_label = ctk.CTkLabel(
            right_buttons, text="選択なし", font=self.info_font, text_color="#e5e5e5"  # 666666 -> e5e5e5
        )
        self.file_count_label.pack(pady=(6, 0))

    def setup_convert_button(self, parent):
        """右上の余ったスペースに「JPEGに変換」ボタンを配置"""
        # フロート配置用のフレーム
        float_frame = ctk.CTkFrame(parent, fg_color="transparent")
        float_frame.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=10)

        self.convert_btn = ctk.CTkButton(
            float_frame, text="🚀 JPEGに変換", font=self.button_font,
            width=180, height=45, command=self.start_conversion
        )
        self.convert_btn.pack()

        # プログレスバーも同位置に配置
        self.progress_bar = ctk.CTkProgressBar(float_frame)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(8, 0))
        
    def setup_preview_area(self, parent):
        """プレビューエリア（改善版：左側元画像、右側変換後画像 + 情報パネル）"""
        self.preview_frame = ctk.CTkFrame(parent)
        self.preview_frame.pack(fill="both", expand=True, padx=15, pady=8)

        title = ctk.CTkLabel(self.preview_frame, text="👁️ プレビュー", font=self.group_title_font)
        title.pack(pady=(12, 8))

        # スクロール可能なプレビューコンテナ
        self.preview_scrollable = ctk.CTkScrollableFrame(self.preview_frame)
        self.preview_scrollable.pack(fill="both", expand=True, padx=12, pady=4)

        # プレビューコンテナ（横幅縮小版）
        preview_main = ctk.CTkFrame(self.preview_scrollable, fg_color="transparent")
        preview_main.pack(fill="both", expand=True)

        # 左側: 元画像（PNG）- 横幅を4/5に縮小
        left_original = ctk.CTkFrame(preview_main, fg_color="transparent", width=280)  # 350 -> 280 (4/5)
        left_original.pack(side="left", fill="both", expand=False, padx=(0, 4))
        left_original.pack_propagate(False)

        self.original_preview = PreviewWidget(left_original, "元画像 (PNG)")
        self.original_preview.pack(fill="both", expand=True)

        # 中央: 矢印（Compact）
        center_info = ctk.CTkFrame(preview_main, fg_color="transparent", width=40)
        center_info.pack(side="left", fill="y", expand=False, padx=4)
        center_info.pack_propagate(False)

        arrow_label = ctk.CTkLabel(center_info, text="→", font=ctk.CTkFont(size=20, weight="bold"), text_color="#007bff")
        arrow_label.pack(expand=True)

        # 右側: 変換後画像（選択された形式）
        right_converted = ctk.CTkFrame(preview_main, fg_color="transparent", width=280)  # 350 -> 280 (4/5)
        right_converted.pack(side="left", fill="both", expand=False, padx=(4, 8))
        right_converted.pack_propagate(False)

        self.converted_preview = PreviewWidget(right_converted, "変換後 (選択形式)")
        self.converted_preview.pack(fill="both", expand=True)

        # 右端: 情報パネル（縮小）
        right_info = ctk.CTkFrame(preview_main, width=200)  # 280 -> 200
        right_info.pack(side="right", fill="both", expand=False)
        right_info.pack_propagate(False)

        # ファイル情報
        self.file_info_title = ctk.CTkLabel(right_info, text="📁 ファイル詳細", font=self.label_font, anchor="w")
        self.file_info_title.pack(pady=(8, 4), padx=10, anchor="w")

        # フォントサイズを縮小
        small_info_font = ctk.CTkFont(family="Segoe UI", size=9)

        self.file_info_label = ctk.CTkLabel(
            right_info, text="選択してください", font=small_info_font,
            text_color="#666666", anchor="nw", justify="left", wraplength=190,
            height=150, fg_color="#f0f0f0", corner_radius=6, padx=5, pady=5
        )
        self.file_info_label.pack(fill="both", expand=True, padx=10, pady=4)

        # 設定情報
        self.config_info_title = ctk.CTkLabel(right_info, text="⚙️ 現在の設定", font=self.label_font, anchor="w")
        self.config_info_title.pack(pady=(6, 4), padx=10, anchor="w")

        self.config_info_label = ctk.CTkLabel(
            right_info, text="", font=small_info_font,
            text_color="#666666", anchor="nw", justify="left", wraplength=190,
            height=150, fg_color="#f0f0f0", corner_radius=6, padx=5, pady=5
        )
        self.config_info_label.pack(fill="both", expand=True, padx=10, pady=(4, 10))
        
    def setup_bottom_area(self, parent):
        """下部エリア（スクロール対応版 - 横並び配置版）"""
        self.bottom_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.bottom_frame.pack(fill="x", padx=15, pady=8)

        # 横並びコンテナ（ログとプログレスバー）
        horizontal_container = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        horizontal_container.pack(fill="x", pady=(0, 4))

        # 左側: ログセクション
        log_section = ctk.CTkFrame(horizontal_container, fg_color="transparent")
        log_section.pack(side="left", fill="both", expand=True, padx=(0, 8))

        log_title = ctk.CTkLabel(log_section, text="📋 変換ログ", font=self.label_font, anchor="w")
        log_title.pack(pady=(6, 3), anchor="w")

        # ログテキストボックス
        self.log_text = ctk.CTkTextbox(
            log_section, 
            height=60,
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color="white",
            text_color="black",
            border_width=1,
            border_color="#cccccc"
        )
        self.log_text.pack(fill="both", expand=True)
        
        # 右側: プログレスバーセクション
        progress_section = ctk.CTkFrame(horizontal_container, fg_color="transparent")
        progress_section.pack(side="right", fill="y", expand=False)
        
        progress_title = ctk.CTkLabel(progress_section, text="進捗状況", font=self.label_font, anchor="w")
        progress_title.pack(pady=(6, 3), anchor="w")
        
        # プログレスバー（明るい色設定）
        self.progress_bar = ctk.CTkProgressBar(
            progress_section,
            width=200,
            height=20,
            fg_color="#e8f5e8",      # 明るい緑色の背景
            progress_color="#4CAF50"  # 明るい緑色の進捗部分
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(anchor="w", pady=(0, 4))
        
    def setup_responsive_handlers(self):
        """レスポンシブ対応とリサイズハンドラー"""
        # 親ウィンドウのリサイズイベントを取得
        parent = self.master
        if hasattr(parent, 'bind'):
            parent.bind("<Configure>", self.on_window_resize)
            
        # 初期サイズを保存
        self.after(100, self.initialize_responsive_layout)
        
    def initialize_responsive_layout(self):
        """レスポンシブレイアウトの初期化"""
        try:
            self.update_idletasks()
            current_width = self.winfo_width()
            self.adjust_layout_for_width(current_width)
        except:
            pass
            
    def on_window_resize(self, event):
        """ウィンドウリサイズ時の処理"""
        if event.widget == self.master:
            # デバウンス用のタイマー
            if hasattr(self, 'resize_timer'):
                self.after_cancel(self.resize_timer)
            
            self.resize_timer = self.after(200, lambda: self.adjust_layout_for_width(event.width))
            
    def adjust_layout_for_width(self, width):
        """横幅に応じたレイアウト調整"""
        try:
            # 画面幅が狭い場合は информацияパネルを非表示にするなど
            if width < 1000:
                # 小さな画面用の компакт 配置
                self.apply_compact_layout()
            else:
                # 大きな画面用の通常配置
                self.apply_normal_layout()
        except Exception as e:
            print(f"レイアウト調整エラー: {e}")
            
    def apply_compact_layout(self):
        """ компакт レイアウト（小画面用）"""
        # 情報パネルの幅を縮小
        if hasattr(self, 'right_info'):
            self.right_info.configure(width=150)
            
        # プレビュー画像のサイズを調整
        if hasattr(self, 'left_original') and hasattr(self, 'right_converted'):
            self.left_original.configure(width=250)
            self.right_converted.configure(width=250)
            
        # ログの高さを縮小
        if hasattr(self, 'log_text'):
            self.log_text.configure(height=60)
            
    def apply_normal_layout(self):
        """通常レイアウト（大画面用）"""
        # 情報パネルの幅を通常に戻す
        if hasattr(self, 'right_info'):
            self.right_info.configure(width=200)
            
        # プレビュー画像のサイズを通常に戻す
        if hasattr(self, 'left_original') and hasattr(self, 'right_converted'):
            self.left_original.configure(width=350)
            self.right_converted.configure(width=350)
            
        # ログの高さを通常に戻す
        if hasattr(self, 'log_text'):
            self.log_text.configure(height=80)
            
    def setup_callbacks(self):
        """初期化コールバック（ компакт版 и ボタンが確実に表示される ）"""
        self.original_preview.clear()
        self.converted_preview.clear()
        self.update_config_info()
        
        # ボタンを確実に表示・アクティブに
        self.convert_jpeg_btn.configure(state="normal")
        self.convert_webp_btn.configure(state="normal")
        print(f"初期化完了: JPEGボタン={self.convert_jpeg_btn.cget('state')}, WebPボタン={self.convert_webp_btn.cget('state')}")
        
    def setup_drop_handlers(self, drop_container):
        """ドラッグ&ドロップイベントハンドラの設定（windnd版）"""
        # Windows用windndのドロップ機能
        try:
            # windndでドロップを無効化
            windnd.hook_dropfiles(self.master, self.on_drop_windnd)
            print("windndのドロップ機能が有効になりました")
            
        except Exception as e:
            print(f"windndの設定エラー: {e}")
            # フォールバックとして標準Tkinterのイベントを使用
            self.setup_fallback_drop_handlers(drop_container)
            
        # クリックイベントもバインド（利便性向上）
        self.drop_area.bind("<Button-1>", lambda e: self.select_files())  # 左クリックでファイル選択
        self.drop_area.bind("<Button-3>", lambda e: self.select_folder())  # 右クリックでフォルダ選択
        
    def on_drop_windnd(self, files):
        """windndによるドロップイベントハンドラ"""
        try:
            file_list = []
            for file_path in files:
                if isinstance(file_path, bytes):
                    # Windows環境ではmbcsでデコード（日本語パス対応）
                    try:
                        file_path = file_path.decode('mbcs')
                    except:
                        file_path = file_path.decode('utf-8', errors='replace')
                else:
                    file_path = str(file_path)

                file_path = file_path.strip('"').strip("'")

                if file_path.lower().endswith('.png') and os.path.isfile(file_path):
                    file_list.append(file_path)

            if file_list:
                self.add_files(file_list)
                self.append_log(f"ドロップで{len(file_list)}個のファイルを追加しました")
            else:
                self.append_log("PNGファイルが見つかりませんでした")

        except Exception as e:
            print(f"windndドロップ処理エラー: {e}")
            self.append_log(f"ドロップエラー: {str(e)}")

    def setup_fallback_drop_handlers(self, drop_container):
        """フォールバック用ドラッグ&ドロップハンドラ"""
        # 標準Tkinterでのフォーカス取得
        drop_container.focus_set()
        
        # ホバー効果を追加
        drop_container.bind('<Enter>', self.on_hover_enter)
        drop_container.bind('<Leave>', self.on_hover_leave)
        
        # ダブルクリックでファイル選択
        drop_container.bind('<Double-Button-1>', lambda e: self.select_files())
        
        print("フォールバックハンドラを設定しました")
        
    def on_size_change(self, value):
        self.size_value_label.configure(text=f"{int(value)} MB")
        self.update_config_info()
        
    def on_format_change(self, value):
        """出力形式変更時の処理（ComboBox削除により使用不可）"""
        # このメソッドはComboBox削除により使用されません
        pass
            
    def on_quality_change(self, value):
        self.quality_value_label.configure(text=f"{int(value)}%")
        self.update_config_info()
        
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="PNGファイルを選択",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if files:
            self.add_files(list(files))
            
    def select_folder(self):
        folder = filedialog.askdirectory(title="フォルダを選択")
        if folder:
            png_files = []
            for ext in ['*.png', '*.PNG']:
                png_files.extend(Path(folder).glob(ext))
            
            if png_files:
                self.add_files([str(f) for f in png_files])
                self.output_path_label.configure(text=folder)
                self.append_log(f"出力先を自動設定: {folder}")
            else:
                messagebox.showinfo("情報", "PNGファイルが見つかりません。")
                
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="出力先を選択")
        if folder:
            self.output_path_label.configure(text=folder)
            self.check_convert_button_state()
            
    def add_files(self, files: List[str]):
        new = [f for f in files if f.lower().endswith('.png') and f not in self.selected_files and os.path.exists(f)]
        if new:
            self.selected_files.extend(new)
            self.update_file_count()
            self.append_log(f"{len(new)}個のファイルを追加しました")
            
            # プレビュー更新（元版本）
            self.update_preview_for_file(new[0])
            self.check_convert_button_state()
            
    def clear_files(self):
        self.selected_files.clear()
        self.update_file_count()
        # プレビュー画像を完全にクリア
        self.original_preview.clear()
        self.converted_preview.clear()
        # ファイル情報パネルもクリア
        self.file_info_label.configure(text="選択してください")
        # ログに追加
        self.append_log("全プレビューとファイルリストをクリアしました")
        self.check_convert_button_state()
        
    def update_file_count(self):
        count = len(self.selected_files)
        text = f"{count}個のファイルを選択中" if count > 0 else "選択なし"
        self.file_count_label.configure(text=text)
        
    def check_convert_button_state(self):
        """ボタンの状態確認（ компакт版 и デバッグ ）"""
        can = len(self.selected_files) > 0 and self.output_path_label.cget("text") != "未選択"
        state = "normal" if can else "disabled"
        self.convert_jpeg_btn.configure(state=state)
        self.convert_webp_btn.configure(state=state)
        print(f"ボタン状態更新: {state} (ファイル数: {len(self.selected_files)}, 出力先: {self.output_path_label.cget('text')})")
        
    def append_log(self, msg):
        self.log_text.insert("end", f"> {msg}\n")
        self.log_text.see("end")
        
    def start_conversion_jpeg(self):
        """JPEG変換開始"""
        self._start_conversion("JPEG")
        
    def start_conversion_webp(self):
        """WebP変換開始"""
        self._start_conversion("WEBP")
        
    def _start_conversion(self, output_format):
        # 変換前にエラーチェック
        if not self.selected_files:
            messagebox.showwarning("警告", "変換するファイルを選択してください。")
            return
            
        output_dir = self.output_path_label.cget("text")
        if not output_dir or output_dir == "未選択":
            messagebox.showwarning("警告", "出力先フォルダを選択してください。")
            return
            
        # 出力先がディレクトリかどうかチェック
        if not os.path.isdir(output_dir):
            messagebox.showwarning("警告", "無効な出力先フォルダです。別のフォルダを選択してください。")
            return
        
        self.progress_bar.set(0)
        self.convert_jpeg_btn.configure(state="disabled", text="変換中...")
        self.convert_webp_btn.configure(state="disabled", text="変換中...")
        format_text = "JPEG" if output_format == "JPEG" else "WebP"
        self.append_log(f"{format_text}変換プロセス開始...")
        
        self.conversion_thread = ConversionThread(
            self.selected_files, output_dir,
            int(self.size_slider.get()), int(self.quality_slider.get()),
            output_format,
            self.conversion_callback
        )
        self.conversion_thread.start()
        
    def conversion_callback(self, etype, p1, p2):
        if etype == "progress":
            self.progress_bar.set(p1 / p2)
            self.append_log(f"進捗: {p1}/{p2}")
        elif etype == "processed":
            self.append_log(f"✓ 完了: {os.path.basename(p1)}")
        elif etype == "error":
            self.append_log(f"❌ {p1}")
        elif etype == "completed":
            self.append_log("✨ 全ての変換が正常に完了しました！")
            self.convert_jpeg_btn.configure(state="normal", text="🚀 JPEGに変換")
            self.convert_webp_btn.configure(state="normal", text="🚀 WebPに変換")
            messagebox.showinfo("完了", "全ての変換が完了しました！")
            
    def update_preview_for_file(self, path: str):
        try:
            if not path or not os.path.exists(path):
                return
                
            img = self.converter.create_preview(path)
            if img is not None:
                self.original_preview.set_image(path, img)
                self.update_file_info_panel(path)
                self.converted_preview.show_placeholder()
            else:
                self.append_log(f"プレビュー生成失敗: {path}")
                
        except Exception as e:
            print(f"プレビューエラー: {e}")
            self.append_log(f"プレビューエラー: {e}")
            
    def _get_output_path(self, png, format_type="JPEG"):
        """出力ファイルパスを取得"""
        p = Path(png)
        if format_type.upper() == "WEBP":
            return str(p.parent / f"{p.stem}.webp")
        else:
            return str(p.parent / f"{p.stem}.jpg")
    
    def update_file_info_panel(self, path: str):
        try:
            f = Path(path)
            sz = f.stat().st_size / (1024 * 1024)
            info = self.converter.get_image_info(path)
            if info:
                txt = f"📄 {f.name}\n\n📏 {info['width']} x {info['height']}\n🎨 {info['channels']} ch\n💾 {sz:.2f} MB\n📂 {f.parent}"
            else: txt = "情報取得不可"
            self.file_info_label.configure(text=txt)
            self.update_config_info()
        except: pass
            
    def update_config_info(self):
        try:
            txt = f"📊 最大サイズ: {int(self.size_slider.get())} MB\n🎯 品質設定: {int(self.quality_slider.get())}%\n📁 出力先: {self.output_path_label.cget('text')}\n📄 総ファイル: {len(self.selected_files)}"
            self.config_info_label.configure(text=txt)
        except: pass
        
    def on_drag_enter(self, event):
        """ドラッグ進入時の処理"""
        self.drop_area.configure(text="ファイルをドロップしてください")
        
    def on_drag_leave(self, event):
        """ドラッグ退出時の処理"""
        self.drop_area.configure(text="PNGファイルをここに\nドラッグ&ドロップ")
        
    def on_drop(self, event):
        """ドロップ時の処理"""
        try:
            # tkinterdnd2からのデータの場合
            data = event.data
            if not data:
                return

            # Windowsのファイルパス形式を処理
            files = []
            if data.startswith('{') and data.endswith('}'):
                # 波括弧で囲まれた複数ファイル
                data = data[1:-1]  # 波括弧を除去
                # 複数ファイルの分割（ } { で区切られている場合）
                files = data.split('} {')
                files = [f.strip() for f in files]
            else:
                # 単一ファイルまたはスペース区切りの可能性
                import re
                # {}で囲まれたパスやスペースを含むパスに対応
                pattern = r'\{(.*?)\}|(\S+)'
                matches = re.findall(pattern, data)
                files = [m[0] if m[0] else m[1] for m in matches]

            # PNGファイルのみをフィルタリング
            png_files = []
            for f in files:
                # 余分な文字（波括弧や引用符）を除去
                f = f.strip().strip('{}').strip('"').strip("'")
                if f.lower().endswith('.png') and os.path.isfile(f):
                    png_files.append(f)

            if png_files:
                self.add_files(png_files)
                self.append_log(f"ドラッグ＆ドロップで{len(png_files)}個のファイルを追加しました")
            else:
                self.append_log("PNGファイルが認識できませんでした")

        except Exception as e:
            self.append_log(f"ドラッグ＆ドロップエラー: {e}")
            print(f"ドロップ処理エラー: {e}")
        finally:
            # ドロップエリアの表示を元に戻す
            self.drop_area.configure(text="PNGファイルをここに\nドラッグ&ドロップ")

    def on_drag_motion(self, event):
        """ドラッグ移動時の処理（フォールバック用）"""
        pass

    def on_drop_fallback(self, event):
        """ドロップフォールバック処理"""
        try:
            import tkinter as tk
            clipboard_content = self.master.clipboard_get()
            if os.path.isfile(clipboard_content) and clipboard_content.lower().endswith('.png'):
                self.add_files([clipboard_content])
        except:
            pass

    def on_hover_enter(self, event):
        """ホバー時の処理"""
        self.drop_area.configure(fg_color="#3a3a3a")

    def on_hover_leave(self, event):
        """ホバー終了時の処理"""
        self.drop_area.configure(fg_color="#2a2a2a")

    def on_drop_windows(self, event):
        """Windows用のドラッグ&ドロップ処理"""
        # Windowsファイルエクスプローラーからのドラッグ&ドロップ対応
        data = event.data
        # 波括弧で囲まれたファイルパスを処理
        files = []
        if data.startswith('{') and data.endswith('}'):
            data = data[1:-1]  # 波括弧を除去
            files = data.split('} {')  # 複数ファイルの分割
        else:
            files = [data]
            
        png_files = [f.strip() for f in files if f.lower().endswith('.png')]
        if png_files:
            self.add_files(png_files)
