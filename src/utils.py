import hashlib
from xml.dom import minidom


def create_xml_by_dict(data):
    doc = minidom.Document()
    root = doc.createElement('xml')

    for k, v in data.items():
        node = doc.createElement(k)
        node.appendChild(doc.createTextNode(str(v)))
        root.appendChild(node)

    doc.appendChild(root)
    xml_str = doc.toxml().encode('utf-8')

    return xml_str


def md5_encrypt(data):
    m = hashlib.md5()
    b = data.encode(encoding='utf-8')
    m.update(b)
    return m.hexdigest()
