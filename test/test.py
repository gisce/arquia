# -*- coding: utf-8 -*-
import unittest
from arquiapgw import ArquiaPGwTestClient, ArquiaPGwClient
from test_config import ARQUIA_SECRET, ARQUIA_USER



class TddArquiaPGw(unittest.TestCase):

    def test_create_arquia_test_client(self):
        config = {
            'REF': 12345,
            'IMPORTE': 100,
            'CONC': 'Quota',
            'CONF': '0100'
        }
        arq = ArquiaPGwTestClient(ARQUIA_USER, ARQUIA_SECRET, config)
        self.assertTrue(arq)

    def test_create_arquia_client(self):
        config = {
            'ID_OPERACION': '12345456',
             'REF': 12345,
             'DNI_CLI': '13572468F',
             'NOMBRE_CLI': 'USUARIO DE PRUEBAS',
             'IMPORTE': 100,
             'CONC': 'Quota',
             'CONF': '0100'}
        arq = ArquiaPGwClient(ARQUIA_USER, ARQUIA_SECRET, config)
        self.assertTrue(arq)

    def test_get_post_data_test(self):
        config = {
            'ID_OPERACION': 'DEMO12345',
            'REF': 12345,
            'IMPORTE': 100,
            'DNI_CLI': '13572468F',
            'NOMBRE_CLI': 'USUARIO DE PRUEBAS',
            'CONC': 'Quota',
            'CONF': '0100',
            'MANDATO': 'd17009d7111f4b368d6f83a144529de1',
            'F_MANDATO': '20140819'
        }
        arq = ArquiaPGwClient(ARQUIA_USER, ARQUIA_SECRET, config)
        data = arq.get_payment_form_data()

        self.assertTrue(data)

if __name__ == '__main__':
    unittest.main()
