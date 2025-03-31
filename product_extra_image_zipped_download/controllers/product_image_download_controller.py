# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import io
import zipfile
from datetime import datetime

from odoo import http
from odoo.http import request


class ProductImageDownloadController(http.Controller):
    @http.route("/download/product/images", type="http", auth="user")
    def download_product_images(self, ids=None, model=None, **kwargs):
        if not ids or not model:
            return request.not_found()
        id_list = [int(i) for i in ids.split(",")]
        Model = request.env[model].sudo()
        records = Model.browse(id_list)
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for record in records:
                images = getattr(record, "product_template_image_ids", [])
                for img in images:
                    image_data = base64.b64decode(img.image_1920)
                    zipf.writestr(img.img_name, image_data)
        zip_buffer.seek(0)
        today_str = datetime.today().strftime("%Y_%m_%d")
        zip_filename = f"[{today_str}]_product_extra_images.zip"
        return request.make_response(
            zip_buffer.getvalue(),
            headers=[
                ("Content-Type", "application/zip"),
                ("Content-Disposition", http.content_disposition(zip_filename)),
            ],
        )
