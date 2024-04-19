import base64

message = "Python is fun"
message_bytes = message.encode('utf-8')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('utf-8')

print('Encoded1', base64_message)

base64_message = base64.b64encode(message.encode('utf-8')).decode('utf-8')

print('Encoded2', base64_message)

decoded_message = base64.b64decode(base64_message).decode('utf-8')

print('Decoded', decoded_message)
print('-' * 200)


def encode_base64_safe(text_to_encode: str):
    """ Genera una codificación Base64 pero sin los caracteres "+", "/", "=" a fines de
    poder ser utilizado para url

    * "+" se cambia a -> "."
    * "=" se cambia a -> "-"
    * "/" se cambia a -> "_"

    Args:
        text_to_encode (str): Texto a ser codificado
    """
    resp_base64 = base64.b64encode(text_to_encode.encode('utf-8')).decode('utf-8')
    resp_base64_safe = resp_base64.replace("+", ".").replace("=", "-").replace("/", "_")

    return resp_base64_safe


def decode_base64_safe(text_to_decode: str):
    """ Decodifica la codificación segura de la funcion encode_base64_safe

    * "." se cambia a -> "+"
    * "-" se cambia a -> "="
    * "_" se cambia a -> "/"

    Args:
        text_to_encode (str): Texto a ser decodificado
    """

    str_to_decode = text_to_decode.replace(".", "+").replace("-", "=").replace("_", "/")
    decoded_string = base64.b64decode(str_to_decode).decode('utf-8')

    return decoded_string


texto = 'Nos los representantes del pueblo de la Nación Argentina, reunidos en Congreso General Constituyente'
encoded_text = encode_base64_safe(texto)
decoded_text = decode_base64_safe(encoded_text)

print("Safe Encode:", encoded_text)
print("Safe Decode:", decoded_text)
