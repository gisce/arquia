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


class ArquiaPGwClient(object):
    """Main client class.
    """

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
        for param in DATA:
            setattr(self, param, None)
        self.ID_USU = userid
        self.password = password
        for key, value in config.items():
            if key in DATA:
                setattr(self, key, str(value))
            else:
                raise ValueError("The supplied config key is forbidden.")
        # default values
        if not self.CONF:
            self.CONF = '1100'

    def get_payment_form_data(self):
        """Returns the data needed to be submitted to Arquia."""
        id_op = str(self.ID_USU)[:4].zfill(4)  # [0 - 3]
        id_op += datetime.now().strftime('%Y%m%d')  # [4 - 11]
        id_op += self.ID_OPERACION.zfill(8)  # [12 - 19]
        id_op = self.ID_OPERACION
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
