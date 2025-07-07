This module defines openai.vision.session, which enables programmatic
access to OpenAI’s GPT-4o model using structured payloads. It supports
multimodal input (images and text), optional web search, and structured
output via JSON Schema.

The module is designed as a backend service and is intended to be
invoked by other modules. Requests can be triggered using the method
call_openai(). When store_response is enabled, the session retains the
previous_response_id to support continuation of conversations.

It is advised to delegate execution to background job queues (e.g.,
queue.job) for asynchronous and fault-tolerant processing.
