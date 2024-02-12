# -*- coding: utf-8 -*-
import logging

from odoo import Command,models, fields, api, _
from odoo.exceptions import UserError, ValidationError



_logger = logging.getLogger(__name__)

class RealState(models.Model):
    _inherit = 'state.real'

    sequence = fields.Char(readonly=True)
    account_move = fields.Many2one('account.move')

    def act_property_sold(self):               
        curr = self.salesman_id.company_id.currency_id._ids[0]               
        journal = self.env['account.journal'].search([('id','=',1)])

        seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(self.write_date)
                )
        new_seq = self.env['ir.sequence'].next_by_code('sale.order', seq_date) or _("New")

        self.account_move = self.env['account.move'].create({
                'partner_id': self.buyer_id.id,
                'move_type': 'out_invoice',
                'journal_id': journal.id,
                'currency_id': curr,
                'ref': self.name,
                'name': new_seq,
                'invoice_line_ids': [
                   Command.create({
                        'name':'6 porcent of sale of %s' %(self.name),
                        'quantity':'1',
                        'currency_id': curr,
                        'account_id':'24',
		                'display_type':'product',
                        'price_unit': self.selling_price*0.06,
                    }),
                    Command.create({
                        'name':'administratives expenses',
                        'quantity':'1',
                        'currency_id': curr,
                        'account_id':'24',
		                'display_type':'product',
                        'price_unit': '100',
                    })]

            })
        
        super().act_property_sold()

