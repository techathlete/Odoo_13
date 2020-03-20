# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    def name_get(self):
        res = []
        for supplier in self:
            res.append((supplier.id, '{} - {}'.format(supplier.name.display_name, str(supplier.price))))
        return res
    
class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _select_seller(self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False):        
        sale_line_id = self.env.context.get('sale_line_id')
        if sale_line_id:
            sale_line = self.env['sale.order.line'].sudo().browse(sale_line_id)
            if sale_line and sale_line.supplierinfo_id:
                return sale_line.supplierinfo_id

        res = super(ProductProduct, self)._select_seller(partner_id=partner_id, quantity=quantity, date=date, uom_id=uom_id, params=params)
            
        return res

