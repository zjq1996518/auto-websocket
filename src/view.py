from flask import request
from urllib import parse
import base64
from operator import itemgetter

from src.utils import create_xml_by_dict
from .websocket import app
import rsa
from .websocket import socket_dict
import xml.etree.cElementTree as ET


PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzSzJ79NvVCd0czx+N4X+PXU0wyZhKmKhl67wg9bqvm3QXRDLu82oeYTaljVdNV4AO6qmCnjRU1ZcQ4bnUdWWbT4q+7UIdMwfspYacSgBj4whz1bqE7UG/VC/TvuQP7pzAreB40J5STgNR8XLtRwIodyEvL++T2dfA5HO3BbloATgnrd8Xym/LS+VyVTn56HGPRBn0QLM9OR4b0NV+hsjGm+S0dyvDf9KrUj1wmcCJGCOt6fdYDSSn+l2PxgZsA73kh93JLwX97j9rUxSoUNKOpNpVit9WYdmR4T/vjqx+Kjetzht2D0wcEOgMXelhEhLCkdA4/qcxbGHuCZdlkNZ1QIDAQAB\n-----END PUBLIC KEY-----'
WX_API_SECRET = '80L4V1PM7FK5YCATJ6WB92SQONUE3HZX'
WX_APP_ID = 'wx2730d73c61c3c492'
WX_MCH_ID = '1583584731'


@app.route('/pay_success/<module_name>', methods=['POST', 'GET'])
def pay_success(module_name):
    if module_name == 'ali':

        data = request.form.to_dict()
        origin_sign = data['sign']
        origin_sign = base64.b64decode(origin_sign)

        websocket_id = data['out_trade_no'].split('_')[1]

        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(PUBLIC_KEY.encode())

        sort_data = sorted(data.items(), key=itemgetter(0))
        sign_data = [f'{parse.unquote(k)}={parse.unquote(v)}' for k, v in sort_data if k != 'sign' and k != 'sign_type']
        sign_data = '&'.join(sign_data)

        rsa.verify(sign_data.encode(), origin_sign, public_key)
        socket_dict['test2'][websocket_id].send('支付成功')

        return 'success'

    if module_name == 'wx':

        """
        b'<xml><appid><![CDATA[wx2730d73c61c3c492]]></appid>\n<bank_type><![CDATA[OTHERS]]></bank_type>\n<cash_fee><![CDATA[1]]></cash_fee>\n<fee_type><![CDATA[CNY]]></fee_type>\n<is_subscribe><![CDATA[N]]></is_subscribe>\n<mch_id><![CDATA[1583584731]]></mch_id>\n<nonce_str><![CDATA[5AU1FPDY3QZNRGO9]]></nonce_str>\n<openid><![CDATA[o-De2wGJulO_4w18RtqdiseIPcUA]]></openid>\n<out_trade_no><![CDATA[8356ba0a806b11eab01700f1f3059bbf]]></out_trade_no>\n<result_code><![CDATA[SUCCESS]]></result_code>\n<return_code><![CDATA[SUCCESS]]></return_code>\n<sign><![CDATA[37B4CA8DEE5C0DE98F53DCBCF10B5091]]></sign>\n<time_end><![CDATA[20200417132319]]></time_end>\n<total_fee>1</total_fee>\n<trade_type><![CDATA[NATIVE]]></trade_type>\n<transaction_id><![CDATA[4200000560202004173900465731]]></transaction_id>\n</xml>'
        """

        data = {
            'return_code': 'SUCCESS',
            'return_msg': 'OK'
        }

        # TODO 微信支付验签
        xml_str = create_xml_by_dict(data)
        xml_data = request.get_data().decode()
        root = ET.fromstring(xml_data)
        websocket_id = root.find('attach').text
        socket_dict['test2'][websocket_id].send('支付成功')

        return xml_str


if __name__ == '__main__':
    pay_success()
