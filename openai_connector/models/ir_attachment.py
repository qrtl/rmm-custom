import base64
import uuid

from odoo import api, models


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def analyze_with_openai_vision(
        self,
        attachment_id,
        prompt_text="この画像に何が写っていますか？またこの写真は見えていますか？見えていない場合は教えてください？",
    ):
        attachment = self.browse(attachment_id)
        if not attachment or not attachment.datas:
            return "指定された添付ファイルが存在しないか、データがありません。"

        try:
            # base64エンコードされた画像URLを作成
            image_data = base64.b64decode(attachment.datas)
            base64_str = base64.b64encode(image_data).decode("utf-8")
            input_image = f"data:{attachment.mimetype};base64,{base64_str}"

            # セッションの作成
            session = self.env["openai.vision.session"].create(
                {
                    "name": f"Attachment Analysis: {attachment.name or str(uuid.uuid4())}",
                    "model": "gpt-4o",
                    "temperature": 0.7,
                }
            )

            # メッセージをセッションに関連付けて作成
            Message = self.env["openai.vision.message"]
            Message.create(
                {
                    "role": "user",
                    "type": "input_text",
                    "content": prompt_text,
                    "sequence": 10,
                    "input_session_id": session.id,
                }
            )
            Message.create(
                {
                    "role": "user",
                    "type": "input_image",
                    "content": input_image,
                    "sequence": 10,
                    "input_session_id": session.id,
                }
            )

            # OpenAI APIを呼び出し
            return_message = session.call_openAI()

            return (
                return_message.content
                or session.response_refusal_message
                or "応答がありませんでした。"
            )

        except Exception as e:
            return f"エラー: {str(e)}"
