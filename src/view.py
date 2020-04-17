from flask import request
from urllib import parse
import base64
from operator import itemgetter
from .websocket import app
import rsa


PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzSzJ79NvVCd0czx+N4X+PXU0wyZhKmKhl67wg9bqvm3QXRDLu82oeYTaljVdNV4AO6qmCnjRU1ZcQ4bnUdWWbT4q+7UIdMwfspYacSgBj4whz1bqE7UG/VC/TvuQP7pzAreB40J5STgNR8XLtRwIodyEvL++T2dfA5HO3BbloATgnrd8Xym/LS+VyVTn56HGPRBn0QLM9OR4b0NV+hsjGm+S0dyvDf9KrUj1wmcCJGCOt6fdYDSSn+l2PxgZsA73kh93JLwX97j9rUxSoUNKOpNpVit9WYdmR4T/vjqx+Kjetzht2D0wcEOgMXelhEhLCkdA4/qcxbGHuCZdlkNZ1QIDAQAB\n-----END PUBLIC KEY-----'


@app.route('/alipay_success', methods=['POST', 'GET'])
def alipay_success():
    data = request.form.to_dict()
    origin_sign = data['sign']
    origin_sign = base64.b64decode(origin_sign)

    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(PUBLIC_KEY.encode())

    sort_data = sorted(data.items(), key=itemgetter(0))
    sign_data = [f'{parse.unquote(k)}={parse.unquote(v)}' for k, v in sort_data if k != 'sign' and k != 'sign_type']
    sign_data = '&'.join(sign_data)

    rsa.verify(sign_data.encode(), origin_sign, public_key)

    return 'success'


if __name__ == '__main__':
    alipay_success()
