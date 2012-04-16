# -*- coding: utf-8 -*-

"""
    Arquia payment gateway
    ~~~~~~~~~~~~~~~~~~~~~~

    This is a python package to interact with the Arquia payment gateway.

"""

import base64
import hashlib

from datetime import datetime
from urllib import quote
from multiprocessing import Lock

import pyDes

DATA = [
    'ID_USU',
    'ID_OPERACION',
    'CONF',
    'REF',
    'DNI_CLI',
    'NOMBRE_CLI',
    'IMPORTE',
    'CONC1',
    'CONC2',
    'CONC3',
    'CONC4',
    'CCVERIF',
]

ENDPOINT_URL = 'https://www.arquia.es/ArquiaRed/pgateway.aspx'

ERROR_CODES = {
    '1016': 'Pin de Operaciones Incorrecto.',
    '1600': 'Error General.',
    '1601': 'Usuario TPV incorrecto.',
    '1602': 'Palabra clave incorrecta.',
    '1603': 'Encriptación errónea.',
    '1604': 'Configuración errónea de modos de pago',
    '1605': 'No existe el banco indicado',
    '1606': 'No existe la sucursal indicada.',
    '1607': 'No existe la C/C de Caja de Arquitectos.',
    '1608': 'Importe incorrecto (<=0).',
    '1609': 'Intento de duplicidad.',
    '1610': 'Datos CCC incorrectos.',
    '1611': 'Demasiados intentos erróneos.',
    '1612': 'No ha indicado el titulal.',
    '1613': 'Cambio IP, diferente sesión.',
    '1614': 'Sociedad no permitida para recibos.',
    '1616': 'El DNI no consta como cliente de Caja de Arquitectos y sólo se '\
            'permite cargo en cuenta.',
    '1010': 'Firma digital incorrecta.',
    '1020': 'Error general en la transacción bancaria.',
    '1200': 'Errores varios en el cargo en cuenta corriente',
    '1201': 'Errores varios en el cargo en cuenta corriente',
    '1202': 'Errores varios en el cargo en cuenta corriente',
    '1203': 'Errores varios en el cargo en cuenta corriente',
    '1204': 'Errores varios en el cargo en cuenta corriente',
    '1205': 'Errores varios en el cargo en cuenta corriente',
    '1206': 'Errores varios en el cargo en cuenta corriente',
    '1207': 'Errores varios en el cargo en cuenta corriente',
    '1208': 'Errores varios en el cargo en cuenta corriente',
    '1209': 'Errores varios en el cargo en cuenta corriente',
    '1210': 'Errores varios en el cargo en cuenta corriente',
    '1211': 'Errores varios en el cargo en cuenta corriente',
    '1212': 'Errores varios en el cargo en cuenta corriente',
    '1213': 'Errores varios en el cargo en cuenta corriente',
    '1214': 'Errores varios en el cargo en cuenta corriente',
    '1215': 'Errores varios en el cargo en cuenta corriente',
    '1216': 'Errores varios en el cargo en cuenta corriente',
    '1217': 'Errores varios en el cargo en cuenta corriente',
    '1218': 'Errores varios en el cargo en cuenta corriente',
    '1219': 'Errores varios en el cargo en cuenta corriente',
    '1220': 'Errores varios en el cargo en cuenta corriente',
    '1221': 'Errores varios en el cargo en cuenta corriente',
    '1222': 'Errores varios en el cargo en cuenta corriente',
    '1223': 'Errores varios en el cargo en cuenta corriente',
    '1224': 'Errores varios en el cargo en cuenta corriente',
    '1225': 'Errores varios en el cargo en cuenta corriente',
    '1226': 'Errores varios en el cargo en cuenta corriente',
    '1227': 'Errores varios en el cargo en cuenta corriente',
    '1228': 'Errores varios en el cargo en cuenta corriente',
    '1229': 'Errores varios en el cargo en cuenta corriente',
    '1700': 'Errores varios en la domiciliación',
    '1701': 'Errores varios en la domiciliación',
    '1702': 'Errores varios en la domiciliación',
    '1703': 'Errores varios en la domiciliación',
    '1704': 'Errores varios en la domiciliación',
    '1705': 'Errores varios en la domiciliación',
    '1706': 'Errores varios en la domiciliación',
    '1707': 'Errores varios en la domiciliación',
    '1708': 'Errores varios en la domiciliación',
    '1709': 'Errores varios en la domiciliación',
    '1710': 'Errores varios en la domiciliación',
    '1711': 'Errores varios en la domiciliación',
    '1712': 'Errores varios en la domiciliación',
    '1713': 'Errores varios en la domiciliación',
    '1714': 'Errores varios en la domiciliación',
    '1715': 'Errores varios en la domiciliación',
    '1716': 'Errores varios en la domiciliación',
    '1717': 'Errores varios en la domiciliación',
    '1718': 'Errores varios en la domiciliación',
    '1719': 'Errores varios en la domiciliación',
    '1720': 'Errores varios en la domiciliación',
    '1721': 'Errores varios en la domiciliación',
    '1722': 'Errores varios en la domiciliación',
    '1723': 'Errores varios en la domiciliación',
    '1724': 'Errores varios en la domiciliación',
    '1725': 'Errores varios en la domiciliación',
    '1726': 'Errores varios en la domiciliación',
    '1727': 'Errores varios en la domiciliación',
    '1728': 'Errores varios en la domiciliación',
    '1729': 'Errores varios en la domiciliación',
    '1730': 'Errores varios en la domiciliación',
    '1731': 'Errores varios en la domiciliación',
    '1732': 'Errores varios en la domiciliación',
    '1733': 'Errores varios en la domiciliación',
    '1734': 'Errores varios en la domiciliación',
    '1735': 'Errores varios en la domiciliación',
    '1736': 'Errores varios en la domiciliación',
    '1737': 'Errores varios en la domiciliación',
    '1738': 'Errores varios en la domiciliación',
    '1739': 'Errores varios en la domiciliación',
    '1740': 'Errores varios en la domiciliación',
    '1741': 'Errores varios en la domiciliación',
    '1742': 'Errores varios en la domiciliación',
    '1743': 'Errores varios en la domiciliación',
    '1744': 'Errores varios en la domiciliación',
    '1745': 'Errores varios en la domiciliación',
    '1746': 'Errores varios en la domiciliación',
    '1747': 'Errores varios en la domiciliación',
    '1748': 'Errores varios en la domiciliación',
    '1749': 'Errores varios en la domiciliación',
    '1750': 'Errores varios en la domiciliación',
    '1751': 'Errores varios en la domiciliación',
    '1752': 'Errores varios en la domiciliación',
    '1753': 'Errores varios en la domiciliación',
    '1754': 'Errores varios en la domiciliación',
    '1755': 'Errores varios en la domiciliación',
    '1756': 'Errores varios en la domiciliación',
    '1757': 'Errores varios en la domiciliación',
    '1758': 'Errores varios en la domiciliación',
    '1759': 'Errores varios en la domiciliación',
    '1760': 'Errores varios en la domiciliación',
    '1761': 'Errores varios en la domiciliación',
    '1762': 'Errores varios en la domiciliación',
    '1763': 'Errores varios en la domiciliación',
    '1764': 'Errores varios en la domiciliación',
    '1765': 'Errores varios en la domiciliación',
    '1766': 'Errores varios en la domiciliación',
    '1767': 'Errores varios en la domiciliación',
    '1768': 'Errores varios en la domiciliación',
    '1769': 'Errores varios en la domiciliación',
    '1770': 'Errores varios en la domiciliación',
    '1771': 'Errores varios en la domiciliación',
    '1772': 'Errores varios en la domiciliación',
    '1773': 'Errores varios en la domiciliación',
    '1774': 'Errores varios en la domiciliación',
    '1775': 'Errores varios en la domiciliación',
    '1776': 'Errores varios en la domiciliación',
    '1777': 'Errores varios en la domiciliación',
    '1778': 'Errores varios en la domiciliación',
    '1779': 'Errores varios en la domiciliación',
    '1780': 'Errores varios en la domiciliación',
    '1781': 'Errores varios en la domiciliación',
    '1782': 'Errores varios en la domiciliación',
    '1783': 'Errores varios en la domiciliación',
    '1784': 'Errores varios en la domiciliación',
    '1785': 'Errores varios en la domiciliación',
    '1786': 'Errores varios en la domiciliación',
    '1787': 'Errores varios en la domiciliación',
    '1788': 'Errores varios en la domiciliación',
    '1789': 'Errores varios en la domiciliación',
    '1790': 'Errores varios en la domiciliación',
    '1791': 'Errores varios en la domiciliación',
    '1792': 'Errores varios en la domiciliación',
    '1793': 'Errores varios en la domiciliación',
    '1794': 'Errores varios en la domiciliación',
    '1795': 'Errores varios en la domiciliación',
    '1796': 'Errores varios en la domiciliación',
    '1797': 'Errores varios en la domiciliación',
    '1798': 'Errores varios en la domiciliación',
    '1799': 'Errores varios en la domiciliación',
}

ID_OPERACION_LOCK = Lock()


class ArquiaPGwClient(object):
    """Main client class.
    """
    counter = 0

    @property
    def endpoint(self):
        return ENDPOINT_URL

    @classmethod
    def increment(cls):
        with ID_OPERACION_LOCK:
            cls.counter += 1

    def __init__(self, userid, password, config):
        """Constructor.

        :param userid: the Arquia provided username
        :param password: the Arquia provided password
        :param config: a dict that should contain the following keys:
          ID_OPERACION: unique operation id
          CONF:         payment modes configuration (1100, 0100 or 1000)
          REF:          payment reference
          DNI_CLI:      customer's VAT number
          NOMBRE_CLI:   customer's name
          IMPORTE:      payment amount
          CONC1:        payment's description line 1
          CONC2:        payment's description line 2
          CONC3:        payment's description line 3
          CONC4:        payment's description line 4
          CCVERIF:      (not required)
        """
        ArquiaPGwClient.increment()
        for param in DATA:
            setattr(self, param, None)
        self.ID_USU = userid
        self.password = password
        for key, value in config.items():
            if key in DATA:
                if not isinstance(value, basestring):
                    value = str(value)
                setattr(self, key, value)
            else:
                raise ValueError("The supplied config key is forbidden.")
        # default values
        if not self.CONF:
            self.CONF = '1100'
        if not self.ID_OPERACION:
            self.ID_OPERACION = str(ArquiaPGwClient.counter)

    def get_payment_form_data(self):
        """Returns the data needed to be submitted to Arquia."""
        if self.ID_OPERACION[:4] == 'DEMO':
            id_op = 'DEMO'  # [0 - 3]
        else:
            id_op = str(self.ID_USU)[:4].zfill(4)  # [0 - 3]
        id_op += datetime.now().strftime('%Y%m%d')  # [4 - 11]
        id_op += self.ID_OPERACION.zfill(8)  # [12 - 19]
        ckey = hashlib.md5(self.password).digest()
        trides = pyDes.triple_des(ckey, pyDes.ECB, padmode=pyDes.PAD_PKCS5)
        id_op_crypt = trides.encrypt(id_op)
        id_op_crypt = base64.b64encode(id_op_crypt)
        res = {}
        for key in DATA:
            value = getattr(self, key, None)
            if value:
                res.update({key: value})
        res.update({'ID_OPERACION': id_op_crypt})
        return res


class ArquiaPGwTestClient(ArquiaPGwClient):
    """Test client class."""

    def __init__(self, userid, password, config, error=False):
        """Test Client constructor.

        config values are set up for the test platform.

        :param error: force error at the payment gateway
        """
        id_op = config.get('ID_OPERACION', 'DEMO')
        id_op = 'DEMO%s' % id_op[4:]
        config.update({'ID_OPERACION': id_op})
        config.update({'NOMBRE_CLI': 'USUARIO DE PRUEBAS'})
        config.update({'DNI_CLI': '13572468F'})
        if error:
            config.update({'IMPORTE': 0})
        super(ArquiaPGwTestClient, self).__init__('testpasarela', password,
                                                  config)
