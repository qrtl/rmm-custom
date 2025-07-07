This module is intended to be used programmatically by other Odoo modules.  
You create and configure `openai.vision.session` records and call the method `call_openai()` from your own business logic.

For example, a product name generator module may call this module's session as follows:

```python
session = env.ref('product_name_generator.openai_vision_session_product_name_generator')
input_image = f"{base_url}/web/image/{self._name}/{self.id}/image_1920"
input_data = json.dumps([
    {"role": "user", "content": [{"type": "input_image", "image_url": image_url}]}
])
response = session.call_openai(input_data)
```

It is advised to delegate execution to background job queues (e.g.,
queue.job) for asynchronous and fault-tolerant processing.