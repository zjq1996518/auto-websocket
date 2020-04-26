from flask import request
from urllib import parse
import base64
from operator import itemgetter

from src.utils import create_xml_by_dict, md5_encrypt
from .websocket import app
from .websocket import socket_dict
import rsa
import xml.etree.cElementTree as ET

PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\n' \
             'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzSzJ79NvVCd0czx+N4X+PXU0wyZh' \
             'KmKhl67wg9bqvm3QXRDLu82oeYTaljVdNV4AO6qmCnjRU1ZcQ4bnUdWWbT4q+7UIdMwfspYa' \
             'cSgBj4whz1bqE7UG/VC/TvuQP7pzAreB40J5STgNR8XLtRwIodyEvL++T2dfA5HO3BbloATg' \
             'nrd8Xym/LS+VyVTn56HGPRBn0QLM9OR4b0NV+hsjGm+S0dyvDf9KrUj1wmcCJGCOt6fdYDSSn' \
             '+l2PxgZsA73kh93JLwX97j9rUxSoUNKOpNpVit9WYdmR4T/vjqx+Kjetzht2D0wcEOgMXelhE' \
             'hLCkdA4/qcxbGHuCZdlkNZ1QIDAQAB\n' \
             '-----END PUBLIC KEY-----'

WX_API_SECRET = '80L4V1PM7FK5YCATJ6WB92SQONUE3HZX'
WX_APP_ID = 'wx2730d73c61c3c492'
WX_MCH_ID = '1583584731'


@app.route('/pay_success/<module_name>', methods=['POST', 'GET'])
def pay_success(module_name):
    if module_name == 'ali':

        data = request.form.to_dict()

        origin_sign = data['sign']
        origin_sign = base64.b64decode(origin_sign)
        del data['sign']
        del data['sign_type']

        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(PUBLIC_KEY.encode())
        rsa.verify(get_sign(data).encode(), origin_sign, public_key)

        websocket_id = data['out_trade_no'].split('_')[1]
        socket_dict['test2'][websocket_id].send('收到支付宝付款')

        return 'success'

    if module_name == 'wx':

        data = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }

        sign_data = {}
        result = ET.fromstring(request.get_data())
        for element in result.iter():
            sign_data[element.tag] = element.text
        origin_sign = sign_data['sign']
        del sign_data['xml']
        del sign_data['sign']

        sign = get_sign(sign_data, WX_API_SECRET)
        if origin_sign != sign:
            raise RuntimeError('签名验证失败！')

        xml_str = create_xml_by_dict(data)
        xml_data = request.get_data().decode()
        root = ET.fromstring(xml_data)

        websocket_id = root.find('attach').text
        socket_dict['test2'][websocket_id].send('收到微信支付')

        return xml_str


def get_sign(data, key=None):
    sort_data = sorted(data.items(), key=itemgetter(0))

    sign_data = []
    for k, v in sort_data:
        k = parse.unquote(k)
        if isinstance(v, str):
            v = parse.unquote(v)
        sign_data.append(f'{k}={v}')
    sign_data = '&'.join(sign_data)

    if key is None:
        return sign_data

    sign_data += f'&key={key}'
    sign = md5_encrypt(sign_data).upper()
    return sign


if __name__ == '__main__':
    pay_success()
