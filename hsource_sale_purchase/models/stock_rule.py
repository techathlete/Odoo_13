# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    @api.model
    def run(self, procurements):
        new_procurements = []
        for procurement in procurements:
            new_procurements.append(
                self.env['procurement.group'].Procurement(
                    procurement.product_id.with_context(sale_line_id=procurement.values.get('sale_line_id', 0)),
                    procurement.product_qty,
                    procurement.product_uom,
                    procurement.location_id,
                    procurement.name,
                    procurement.origin,
                    procurement.company_id,
                    procurement.values
                )
            )
        return super(ProcurementGroup, self).run(new_procurements)

    
class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _run_buy(self, procurements):
        res = super(StockRule, self)._run_buy(procurements)
        return res

    def _make_po_get_domain(self, company_id, values, partner):
        domain = super(StockRule, self)._make_po_get_domain(company_id, values, partner)
        if values.get('po_name'):
            domain += (('name', '=', values.get('po_name')),)
        return domain

    def _prepare_purchase_order(self, company_id, origins, values):
        vals = super(StockRule, self)._prepare_purchase_order(company_id, origins, values)
        vals.update({'name': values[0].get('po_name', '')})
        return vals
    
    @api.model
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, values, po):
        res = super(StockRule, self)._prepare_purchase_order_line(product_id, product_qty, product_uom, company_id, values, po)
        res.update({
            'cost_center': values.get('cost_center'),
        })
        return res
                
                
    
    


    
