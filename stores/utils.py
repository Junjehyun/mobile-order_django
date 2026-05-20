#stores/utils.py
import qrcode
from io import BytesIO
import os
from django.conf import settings
from django.core.files.base import ContentFile

def generate_qr_code(table):
    """テーブルごとのQRコード自動生成"""
    # 顧客がスキャンした際、移動するURL(C01ページ)
    qr_data = f"http://127.0.0.1:8000/customer/landing/?table={table.table_number}&store{table.store.store_id}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # media/qrcode フォルダー生成
    qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
    os.makedirs(qr_dir, exist_ok=True)
    
    # ファイル名とパス
    filename = f"qr_{table.store.store_id}_{table.table_number}.png"
    file_path = os.path.join(qr_dir, filename)
    
    img.save(file_path)
    
    #モデルにURLを保存
    table.qr_code_url = f"{settings.MEDIA_URL}qrcodes/{filename}"
    table.save()
    
    return table.qr_code_url