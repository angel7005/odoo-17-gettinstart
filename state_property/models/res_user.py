# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from . import state_real
_logger = logging.getLogger(__name__)

class ResUser(models.Model):      
    _name = 'res.users'
    _inherit = ['res.users']

    is_salesman = fields.Boolean(default=True)

    property_ids = fields.One2many(
        comodel_name='state.real',
        inverse_name='salesman_id',
        string='Properties sold'
    )
      
