from odoo.tests import common

class TestPropertyType(common.TransactionCase):
    def setUp(self):
       super(TestPropertyType, self).setUp()
       #Create property type
       self.MyModel = self.env['state.property.type']
       self.MyModel.create({
           'sequence':'1',
           'name':'Penthouse'
       })
       self.record = self.MyModel.search([('name','=','Penthouse')],limit=1)

    def tearDown(self):
        # Delete created register to end test
        if self.record:
          self.record.unlink()
        super(TestPropertyType, self).tearDown()

    def test_find_recordByName(self):        
        self.assertTrue(self.record,'Record not found')

    def test_find_recordById(self):        
        self.assertTrue(self.record,'Record not found')

    def test_compareByName(self):
        self.assertEqual(self.record.name,'Penthouse', 'Record searched is no Penthouse')