from odoo.tests import common

class TestMoveType(common.TransactionCase):
    def setUp(self):
       super(TestMoveType, self).setUp()
       #Create move type
       self.MyModel = self.env['account.move']
       self.record = self.env['account.move'].create({
                'partner_id': 1,
                'move_type': 'out_invoice',
                'journal_id': '1',
            })

    def tearDown(self):
        # Delete created register to end test
        if self.record:
          self.record.unlink()
        super(TestMoveType, self).tearDown()

    def test_invoice_journal(self):
       self.assertEqual(self.record.move_type.name,'clinet', 'The journa of invoice move type is not correct')