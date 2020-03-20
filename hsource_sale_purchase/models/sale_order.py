# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    supplierinfo_id = fields.Many2one('product.supplierinfo', ondelete='set null', string='Supplier Info', readonly=True)

    supplier_id = fields.Many2one('res.partner', string='Vendor')
    supplier_price = fields.Float(string='Vendor Price')

    po_name = fields.Char('PO Name')
    cost_center = fields.Char('Cost Center')
    
    def _create_update_supplierinfo(self, line_vals):
        vals = self._prepare_supplier_vals(line_vals)
        if not vals:
            return
        
        for line in self:
            if not line.supplierinfo_id:
                supplier_id = vals.get('name')
                if not supplier_id:
                    continue
                line.supplierinfo_id = self.env['product.supplierinfo'].create({'name': supplier_id})
            else:
                line.supplierinfo_id.write(vals)
                
    def _prepare_supplier_vals(self, line_vals):
        supplier_vals = {}
        supplier_id = line_vals.get('supplier_id', 0)
        if supplier_id:
            supplier_vals.update({
                'name': supplier_id,
            })
        supplier_price = line_vals.get('supplier_price', 0.0)
        if supplier_price:
            supplier_vals.update({
                'price': supplier_price,
            })
        return supplier_vals
                
    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        res._create_update_supplierinfo(vals)
        return res

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        self._create_update_supplierinfo(vals)
        return res
    
    def _prepare_procurement_values(self, group_id=False):
        vals = super(SaleOrderLine, self)._prepare_procurement_values(group_id=group_id)
        vals.update({
            'po_name': self.po_name,
            'cost_center': self.cost_center
        })
        return vals
    
