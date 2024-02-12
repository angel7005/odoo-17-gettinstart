# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta
from . import res_user
_logger = logging.getLogger(__name__)


class RealState(models.Model):
    _name = 'state.real'
    _description = 'Real State'
    _order = 'id desc'
    
    bedrooms = fields.Integer('Bedrooms', default=2)   
    best_offer = fields.Float(compute='_compute_best_offer')
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    
    date_availability = fields.Date('Date availivility', default=date.today()+timedelta(days=93))
    description = fields.Char(_('Description'))  
    
    expected_price = fields.Float('Expected price', required=True)
     
    facades = fields.Integer('Facades')
    
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area(sqm)')
    garden_orientation = fields.Selection(
                                          [
                                              ('N','North'),
                                              ('S','Sur'),
                                              ('E','Este'),
                                              ('O','Oeste'),
                                          ], default='S'
                                          )
    name = fields.Char('Real State', required=True)

    offers_ids = fields.One2many('state.property.offer', 'property_id')

    postcode = fields.Char(string = 'Postcode')
    property_type_id = fields.Many2one(        
        'state.property.type',
        string='Property type',        
        ondelete='restrict',
        create=False,
        required=True,       
    )

    living_area = fields.Integer('Living area(sqm)')

    salesman_id = fields.Many2one(
        comodel_name='res.users',        
        string='Salesman',        
        default=lambda self: self.env.user
    )
    selling_price = fields.Float('Selling Price', readonly=True, )
    status = fields.Selection([
        ('N','NEW'),
        ('R','OFFER RECEIVED'),
        ('A','OFFER ACCEPT'),
        ('S','SOLD'),
        ('C','CANCELED')
    ], default='N', string='Status',       
    )

    tags_id = fields.Many2many('state.property.tag',string='Tags',)
    total_area = fields.Float(compute="_compute_total_area")

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price more than cero'),
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price more than cero'),    
    ]
    #  ('check_living_area_positive', 'CONSTRAINT must_be_different UNIQUE', 'The tag must be unique')        

    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for record in self:
           record.total_area = record.living_area + record.garden_area

    @api.depends('offers_ids')
    def _compute_best_offer(self):    
        for record in self:
            record.best_offer = max(record.mapped('offers_ids.price')) if (record.offers_ids) else 0.0
          
    @api.onchange('garden')
    def _onChange(self):
        self.garden_area = 100 if self.garden else 0
        self.garden_orientation = 'N' if self.garden else ''

    def act_property_sold(self):
        message='Property is %s' % (self.status)

        if (self.status=='C'):
            #raise UserError("Can't sold an CANCELED property!")
            message = _("Can't sold a CANCELED property") 
        else:
            self.status='S'
           
    def act_property_cancel(self):
        message='Property is %s' % (self.status)

        if (self.status=='S'):
            #raise UserError("Can't canceld an SOLD property!")            
            message = _("Can't cancel a SOLD property") 
            #lambda self: self.env.user.notify_info(message=message)
        else:
            self.status='C'
        
    def act_name1(self):
        return True
    
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            min_price = 0.9 * record.expected_price
            if record.selling_price < min_price:
                raise ValidationError("The price of selling can't be less thant %2f (90 porcents) of the expect price" % (min_price))                                          

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_user(self):        
        for record in self:
            if (record.status not in ['C','N']):
                raise UserError("The property s% can't to be delete because its state %c is not new or canceled" % (record.name,record.status))                                          