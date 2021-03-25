# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('manager', 'Manager'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    def action_confirm(self):
        self.state = 'manager'

    def action_manager_approve(self):
        record = super(SaleOrderInh, self).action_confirm()


class PurchaseOrderInh(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('manager', 'Approval From Manager'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def button_confirm(self):
        self.state = 'manager'

    def action_manager_approve(self):
        record = super(PurchaseOrderInh, self).button_confirm()
        if record:
            self.state = 'purchase'


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('manager', 'Approval from Manager'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')

    def action_post(self):
        self.state = 'manager'

    def action_manager_approve(self):
        record = super(AccountMoveInh, self).action_post()


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('manager', 'Approval from Manager'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")

    def button_validate(self):
        self.state = 'manager'

    def action_manager_approve(self):
        record = super(StockPickingInh, self).button_validate()
        return record

