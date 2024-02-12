from odoo.tests import common
from datetime import date, timedelta 

#from odoo.addons.state_property.models.state_real import RealState

class TestStateProperty(common.TransactionCase):
    def setUp(self, *args, **kwargs):
       super().setUp(*args, **kwargs)       
       
       #Create property type
       self.MyModel = self.env['state.property.type']
       self.MyModel.create({
           'sequence':'1',
           'name':'Penthouse'
       })
       self.recordPropertyType = self.MyModel.search([('name','=','Penthouse')],limit=1)

       #Create state real 
       self.Property = self.env["state.real"]
       self.recordProperty = self.Property.create({
            "name": "House1",
            "property_type_id": self.recordPropertyType.id,
            "date_availability": date.today()+timedelta(days=93),
            "expected_price": '1000000',
            "description": "Prueba de state.real model create",        
        })              
       
    def tearDown(self):
        # Delete created register to end test
        if self.record:
          self.record.unlink()

        if self.recordProperty:
            self.recordProperty.unlink()
        
        super(TestStateProperty, self).tearDown()
    
    def test_property_type_name(self):    
       self.assertEqual('Penthouse', self.recordProperty.property_type_id.name, msg='PropertyType expexted: %s' %(actual_property_type))            
    
    def test_property_name(self):         
         self.assertTrue(self.recordProperty, 'Actual property type is null')		
         self.assertEqual('House',self.recordProperty.name, 'Property name')		        

    def test_property_notnull(self):
           "Model state.real are import correctly..."
           model_a = self.env['state.real']
           self.assertTrue(model_a!=None,'The model state_real is not import correctly en state_account')           
