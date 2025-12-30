#!/usr/bin/env python3
"""
画像変換エンジン
高品質PNG to JPEG変換の中核機能

Author: Generated for user
Date: 2025-12-30
Version: 1.0.0
"""

import cv2
import numpy as np
from PIL import Image
import os
from pathlib import Path
from typing import Tuple, Optional
import tempfile


class ImageConverter:
    """高品質画像変換クラス"""
    
    def __init__(self):
        """初期化"""
        self.temp_dir = tempfile.mkdtemp()
        
    def convert_to_jpeg(self, input_path: str, output_path: str, 
                       max_size_mb: int, quality: int) -> bool:
        """
        PNGをJPEGに変換
        
        Args:
            input_path: 入力PNGファイルパス
            output_path: 出力JPEGファイルパス
            max_size_mb: 最大ファイルサイズ（MB）
            quality: JPEG品質（1-100）
            
        Returns:
            bool: 成功時True、失敗時False
        """
        try:
            # OpenCVで画像を読み込み
            # 日本語パス対応
            img_array = np.fromfile(input_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                print(f"画像読み込み失敗: {input_path}")
                return False
            
            # カラー画像の場合、BGRからRGBに変換
            if len(img.shape) == 3:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                img_rgb = img
                
            # PILで最高品質JPEG変換
            pil_img = Image.fromarray(img_rgb)
            
            # 初期品質設定
            current_quality = quality
            temp_output = self._get_temp_path(output_path)
            
            # ファイルサイズ制限を満たすまで品質を調整
            while current_quality > 10:  # 最低品質10
                # 一時ファイルに保存
                pil_img.save(temp_output, 'JPEG', quality=current_quality, optimize=True)
                
                # ファイルサイズチェック
                if os.path.getsize(temp_output) <= max_size_mb * 1024 * 1024:
                    break
                    
                # 品質を10%ずつ下げる
                current_quality = max(10, int(current_quality * 0.9))
            
            # 最終ファイルをコピー
            os.replace(temp_output, output_path)
            
            return True
            
        except Exception as e:
            print(f"変換エラー: {input_path} - {str(e)}")
            return False
            
    def convert_to_webp(self, input_path: str, output_path: str, 
                       max_size_mb: int, quality: int) -> bool:
        """
        PNGをWebPに変換
        
        Args:
            input_path: 入力PNGファイルパス
            output_path: 出力WebPファイルパス
            max_size_mb: 最大ファイルサイズ（MB）
            quality: WebP品質（1-100）
            
        Returns:
            bool: 成功時True、失敗時False
        """
        try:
            # OpenCVで画像を読み込み
            # 日本語パス対応
            img_array = np.fromfile(input_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                print(f"画像読み込み失敗: {input_path}")
                return False
            
            # カラー画像の場合、BGRからRGBに変換
            if len(img.shape) == 3:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            else:
                img_rgb = img
                
            # PILでWebP変換
            pil_img = Image.fromarray(img_rgb)
            
            # 初期品質設定
            current_quality = quality
            temp_output = self._get_temp_path(output_path)
            
            # ファイルサイズ制限を満たすまで品質を調整
            while current_quality > 10:  # 最低品質10
                # 一時ファイルに保存
                pil_img.save(temp_output, 'WEBP', quality=current_quality, optimize=True)
                
                # ファイルサイズチェック
                if os.path.getsize(temp_output) <= max_size_mb * 1024 * 1024:
                    break
                    
                # 品質を10%ずつ下げる
                current_quality = max(10, int(current_quality * 0.9))
            
            # 最終ファイルをコピー
            os.replace(temp_output, output_path)
            
            return True
            
        except Exception as e:
            print(f"WebP変換エラー: {input_path} - {str(e)}")
            return False
            
    def get_image_info(self, image_path: str) -> Optional[dict]:
        """
        画像情報を取得
        
        Args:
            image_path: 画像ファイルパス
            
        Returns:
            dict: 画像情報（None if error）
        """
        try:
            # OpenCVで画像を読み込み
            # 日本語パス対応
            img_array = np.fromfile(image_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                return None
                
            height, width, channels = img.shape
            
            # ファイルサイズ
            file_size = os.path.getsize(image_path)
            
            return {
                'width': width,
                'height': height,
                'channels': channels,
                'file_size': file_size,
                'file_size_mb': round(file_size / (1024 * 1024), 2)
            }
            
        except Exception as e:
            print(f"画像情報取得エラー: {image_path} - {str(e)}")
            return None
            
    def create_preview(self, image_path: str, max_size: Tuple[int, int] = (300, 300)) -> Optional[np.ndarray]:
        """
        プレビュー画像を作成
        
        Args:
            image_path: 画像ファイルパス
            max_size: 最大サイズ (width, height)
            
        Returns:
            np.ndarray: プレビュー画像（None if error）
        """
        try:
            # OpenCVで画像を読み込み
            # 日本語パス対応
            img_array = np.fromfile(image_path, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                return None
                
            # リサイズ
            height, width = img.shape[:2]
            max_width, max_height = max_size
            
            # アスペクト比を維持してリサイズ
            if width > max_width or height > max_height:
                scale = min(max_width / width, max_height / height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            return img
            
        except Exception as e:
            print(f"プレビュー作成エラー: {image_path} - {str(e)}")
            return None
            
    def _get_temp_path(self, original_path: str) -> str:
        """一時ファイルパスを取得"""
        dir_name = os.path.dirname(original_path)
        file_name = os.path.basename(original_path)
        temp_file = f".tmp_{file_name}"
        return os.path.join(dir_name, temp_file)
        
    def cleanup(self):
        """リソースクリーンアップ"""
        try:
            # 一時ディレクトリを削除
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except Exception:
            pass