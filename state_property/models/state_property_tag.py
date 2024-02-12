# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class StatePropertyTag(models.Model):
    _name = 'state.property.tag'
    _description = _('State Property Tag')
    _order = 'name asc'

    color = fields.Integer("Color")
    name = fields.Char(_('Name'), required=True)
    
_sql_constraints = [
      ('check_unique_tag', '(unique (name))', 'The tag must be unique'),             
    ]
