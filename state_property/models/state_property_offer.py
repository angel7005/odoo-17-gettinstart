# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, timedelta

_logger = logging.getLogger(__name__)


class StatePropertyOffer(models.Model):
    _name = 'state.property.offer'
    _description = _('StatePropertyOffer')
    _order = 'price desc'

    date_deadline = fields.Date(string='DeadLine date', compute='_compute_deadline_date', 
                                inverse='_compute_validity')

    name = fields.Char(_('Name'))
    
    partner_id  = fields.Many2one('res.partner', required=True)    
    price  = fields.Float("Price", required=True, default=0.0)
    property_id = fields.Many2one('state.real', 'Property', required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    status = fields.Selection([('A', 'Accepted'),('R','Refused'),('P','Proccessing')])

    validity = fields.Integer(string='Validity', default=7)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price more than cero'),
    ]

    @api.depends('validity')
    def _compute_deadline_date(self):
        for record in self:
            if (record.property_id and record.property_id.create_date):
              record.date_deadline = record.property_id.create_date + timedelta(days=record.validity + 1)              
              if(record.property_id.status=='N'):
                 record.property_id.status='R'                                    
    
    def _compute_validity(self):
        for record in self:       
            if (record.date_deadline and record.property_id and record.property_id.create_date):     
              record.validity = (record.date_deadline - record.property_id.create_date.date()).days - 1

    def action_accept(self):       
          self.status = 'A'
          self.property_id.status='A'
          self.property_id.selling_price = self.price
          self.property_id.buyer_id = self.partner_id                 
    
    def action_refuse(self):
         self.status = 'R'      

    @api.constrains('price')
    def _check_offer_price(self):
        min_price = min(self.mapped('price'))
        for record in self:
            if record.price < min_price:
                raise ValidationError("The price of offer can't be less thant %2f, that is minimun offert price" % (min_price))                                             
            
    @api.model
    def create(self, vals):        
        offers_record = self.env['state.property.offer'].search([('property_id','=',vals['property_id'])]) 
        property = self.env['state.real'].search([('id','=',vals['property_id'])])
        _logger.info('..........vals %s' %vals)
        _logger.info('..........vals %s' %property)

        if (property[0].status=='N' ):
            property[0].status='R' 

        if(offers_record):
          min_price = min(offers_record.mapped("price"))
          price = vals["price"]
       
          if price < min_price:
             min_price = f'{min_price:,.2f}'
             price = f'{price:,.2f}'
             raise ValidationError("The price %s of offer can't be less thant %s, that it is minimun offert " % (price,min_price))                                             

        return super(StatePropertyOffer,self).create(vals)        
       