#!/usr/bin/env python3
"""
プレビューウィジェット
CustomTkinter版 変換前後の画像を表示するコンポーネント
Compact version for smaller UI

Author: Generated for user
Date: 2025-12-30
Version: 2.1.0 (CustomTkinter - Compact)
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple
import tkinter as tk
import customtkinter as ctk
from PIL import Image


class PreviewWidget(ctk.CTkFrame):
    """画像プレビューウィジェット（コンパクト版）"""
    
    def __init__(self, master, title: str = "プレビュー"):
        super().__init__(master)
        self.title = title
        self.current_image = None
        self.current_image_path = None
        self.image_info = None
        
        self.init_ui()
        
    def init_ui(self):
        """UI初期化（元サイズに戻す）"""
        # フォント設定（元サイズに）
        self.title_font = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")    # 24 -> 12
        self.info_font = ctk.CTkFont(family="Segoe UI", size=10)                     # 20 -> 10
        
        # タイトル
        self.title_label = ctk.CTkLabel(
            self,
            text=self.title,
            font=self.title_font,
            text_color="#ffffff"  # 2b2b2b -> ffffff (ダークモード対応)
        )
        
        # プレビュー用フレーム
        self.preview_frame = ctk.CTkFrame(self, fg_color="#3a3a3a", corner_radius=6)  # f8f9fa -> 3a3a3a
        
        # 画像表示ラベル（縦幅130px版に拡大）
        self.image_label = ctk.CTkLabel(
            self.preview_frame,
            text="ここに画像が\n表示されます",
            font=self.info_font,
            text_color="#e5e5e5",  # 6c757d -> e5e5e5 (ダークモード対応)
            fg_color="#2a2a2a",    # e9ecef -> 2a2a2a
            corner_radius=4,
            anchor="center",
            width=200,   # 200 -> 200
            height=130   # 250 -> 130 (130pxに拡大)
        )
        
        # 情報表示（ компакт 版）
        self.info_label = ctk.CTkLabel(
            self,
            text="画像が選択されていません",
            font=self.info_font,
            text_color="#e5e5e5",  # 6c757d -> e5e5e5 (ダークモード対応)
            anchor="nw",
            justify="left",
            wraplength=280   # 350 -> 280
        )
        
        # 配置（ компакт 版）
        self.title_label.pack(pady=(0, 5))    # 10 -> 5
        self.preview_frame.pack(fill="both", expand=True, padx=3, pady=3)  # 5 -> 3
        self.image_label.pack(fill="both", expand=True, padx=8, pady=8)    # 10 -> 8
        self.info_label.pack(fill="x", padx=8, pady=(3, 15))               # テキスト途切れ解消 - 下部パディング増加
        
        # 初期表示
        self.show_placeholder()
        
    def show_placeholder(self, title_prefix=""):
        """プレースホルダー表示"""
        placeholder_text = "まだ変換されていません"
        if title_prefix:
            placeholder_text = f"{title_prefix}\n{placeholder_text}"
        else:
            placeholder_text = placeholder_text
            
        self.image_label.configure(
            text=placeholder_text,
            text_color="#e5e5e5",  # 6c757d -> e5e5e5 (ダークモード対応)
            fg_color="#2a2a2a",    # e9ecef -> 2a2a2a
            image=None,  # CTkImage警告を避けるため明示的にNoneを設定
            width=200,
            height=130
        )
        
    def set_image(self, image_path: Optional[str], preview_image: Optional[np.ndarray] = None):
        """
        画像を設定
        
        Args:
            image_path: 画像ファイルパス（Noneまたは空文字列の場合はプレースホルダー表示）
            preview_image: プレビュー画像（Noneの場合は自動生成）
        """
        self.current_image_path = image_path
        
        # 画像パスがNoneまたは空の場合、プレースホルダーを表示
        if not image_path or image_path is None:
            self.show_placeholder()
            return
        
        try:
            # プレビュー画像が提供されていない場合は自動生成
            if preview_image is None:
                preview_image = self._create_preview_image(image_path)
                
            if preview_image is not None:
                self.current_image = preview_image
                self._display_image(preview_image)
                self._update_info(image_path)
            else:
                self.show_error("画像の読み込みに失敗しました")
                
        except Exception as e:
            self.show_error(f"画像表示エラー: {str(e)}")
            
    def _create_preview_image(self, image_path: str) -> Optional[np.ndarray]:
        """プレビュー画像を作成"""
        try:
            # OpenCVで画像を読み込み (日本語パス対応版)
            img_array = np.fromfile(image_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                return None
                
            # プレビューサイズにリサイズ（ компакт 版）
            preview_size = self._get_preview_size()
            img_resized = self._resize_image(img, preview_size)
            
            return img_resized
            
        except Exception as e:
            print(f"プレビュー画像作成エラー: {str(e)}")
            return None
            
    def _get_preview_size(self) -> Tuple[int, int]:
        """プレビューサイズを取得（130px対応版）"""
        # 130pxに拡大したプレビューサイズ
        max_width = 280    # 350 -> 280
        max_height = 130   # 200 -> 130 (130pxに拡大)

        return (max_width, max_height)
        
    def _resize_image(self, img: np.ndarray, max_size: Tuple[int, int]) -> np.ndarray:
        """画像をリサイズ（Aspect Ratio維持）"""
        height, width = img.shape[:2]
        max_width, max_height = max_size
        
        # アスペクト比を維持してリサイズ
        if width > max_width or height > max_height:
            scale = min(max_width / width, max_height / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
        return img
        
    def _display_image(self, img: np.ndarray):
        """画像を表示（130px対応版 + アスペクト比維持）"""
        try:
            # OpenCVのBGRをRGBに変換
            if len(img.shape) == 3:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB) if len(img.shape) == 2 else img
            
            # PIL Imageに変換
            pil_image = Image.fromarray(img_rgb)
            
            # フレームサイズを取得
            frame_width = 200
            frame_height = 130
            
            # アスペクト比を維持してリサイズ
            img_width, img_height = pil_image.size
            scale_w = frame_width / img_width
            scale_h = frame_height / img_height
            scale = min(scale_w, scale_h)
            
            # 新しいサイズを計算（ Center 配置用）
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # リサイズ
            resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # CTkImageを使用（ Center 配置）
            ctk_image = ctk.CTkImage(light_image=resized_image, size=(new_width, new_height))
            
            # ラベルサイズをフレームサイズに設定（ Center 配置）
            self.image_label.configure(
                image=ctk_image, 
                text="", 
                fg_color="white",
                width=frame_width,
                height=frame_height
            )
            self.image_label.image = ctk_image  # 参照を保持
            
        except Exception as e:
            print(f"プレビュー表示エラー: {str(e)}")
            self.show_error(f"画像表示エラー: {str(e)}")
            
    def _update_info(self, image_path: str):
        """情報を更新（ компакт 版）"""
        try:
            # ファイル情報取得
            file_info = Path(image_path)
            file_size = file_info.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            # 画像情報取得（複数回試行）
            img = None
            for attempt in range(3):
                try:
                    # 日本語パス対応版
                    img_array = np.fromfile(image_path, dtype=np.uint8)
                    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    if img is not None:
                        break
                except Exception as e:
                    print(f"画像読み込み試行 {attempt + 1} 失敗: {e}")
                    if attempt < 2:
                        continue
                    else:
                        raise e
            
            if img is not None:
                height, width = img.shape[:2]
                channels = img.shape[2] if len(img.shape) == 3 else 1
                
                info_text = f"📁 {file_info.name}\n"
                info_text += f"📏 {width} × {height}\n"
                info_text += f"🎨 {channels}ch\n"
                info_text += f"💾 {file_size_mb:.2f}MB"
                
                self.image_info = {
                    'width': width,
                    'height': height,
                    'channels': channels,
                    'file_size_mb': file_size_mb
                }
            else:
                info_text = f"📁 {file_info.name}\n❌ 画像情報が取得できませんでした"
                self.image_info = None
                
            self.info_label.configure(text=info_text)
            
        except Exception as e:
            error_msg = f"❌ 情報取得エラー: {str(e)}"
            self.info_label.configure(text=error_msg)
            print(f"プレビュー情報更新エラー: {e}")
            
    def show_error(self, message: str):
        """エラーを表示"""
        self.image_label.configure(
            text="!",
            text_color="#dc3545",
            fg_color="#f8d7da",
            width=200,
            height=130
        )
        self.info_label.configure(text=message)
        
    def clear(self):
        """クリア"""
        self.current_image = None
        self.current_image_path = None
        self.image_info = None
        
        # CTkImageの参照を明示的にクリア
        if hasattr(self.image_label, 'image'):
            self.image_label.image = None
        
        # 画像とテキストをクリアしてからプレースホルダーを表示
        self.image_label.configure(image="", text="")
        
        # 強制的に再描画
        self.image_label.update_idletasks()
        
        # プレースホルダーを表示
        self.show_placeholder()
        
    def get_image_info(self) -> Optional[dict]:
        """現在の画像情報を取得"""
        return self.image_info
