# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class PropertyType(models.Model):
    _name = 'state.property.type'
    _description = _('Property Type')
    _order = 'sequence, name asc'

    name = fields.Char('Property type', required=True)
    offer_ids = fields.One2many('state.property.offer','property_type_id',string='Offers id')
    offers_count = fields.Integer(compute='_compute_offers_count', string='Offers')
    property_ids = fields.One2many('state.real','property_type_id')
    sequence = fields.Integer()

    @api.depends('offer_ids')
    def _compute_offers_count(self):
        count = 0
        for record in self:
          if (record):
             _logger.info('..................%s-%s:%s' %(record.name, record.offer_ids.property_type_id, len(record.offer_ids)))
          count = count + 1
          #record.offers_count = self.env['state.property.offer'].search_count([('property_type_id.id', '=', self.id)])
          record.offers_count = len(record.offer_ids)

    def act_offer_open(self):
        return {
           'type': 'ir.actions.act_window',
            'name': '%(action_state_property_offer)d',
            'view_mode': 'tree',
            'res_model': 'state.property.offer',
            'domain': [('property_type_id', '=', self.id)],
            'context': "{'create': False}"
        }
        