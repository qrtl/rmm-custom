Set the value of code to 'openai' in your API configuration.  

This module depends on the 'base_api_connection'. Therefore, please follow the 
configuration steps outlined in that module.

For the OpenAI API configuration:

- Only the api_key field is required to be set.
- The base_url, token_type, and header_api_key_string are prefilled by this module.


Basically, The OpenAI session should be added by a specific module that depends on this
one.
To adjust the session attributes, 

- Go to Settings → Technical →OpenAI Vision Sessions.

For additional options and usage details, refer to the official documentation:
<https://platform.openai.com/docs>
