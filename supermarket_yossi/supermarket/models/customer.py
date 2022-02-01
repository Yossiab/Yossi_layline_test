# -*- coding: utf-8 -*-
from odoo import fields, models, api
import datetime


class Customer(models.Model):
    _name = 'supermarket.customer'
    _description = 'Customer'

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    city = fields.Char(string='City')
    street = fields.Char(string='Street')


class ProductCategory(models.Model):
    _name = 'supermarket.product.category'
    _description = 'Product Category'

    name = fields.Char(string='Name')


class Product(models.Model):
    _name = 'supermarket.product'
    _description = 'Product'

    name = fields.Char('Name')
    product_category_id = fields.Many2one(comodel_name='supermarket.product.category', string='Product Category')
    unit_price = fields.Float('Unit Price')


class Cart(models.Model):
    _name = 'supermarket.cart'
    _description = 'Cart'

    customer_id = fields.Many2one(comodel_name='supermarket.customer', string='Customer', required=True)
    date = fields.Date(string='Date')


class CartItem(models.Model):
    _name = 'supermarket.cart.item'
    _description = 'Cart Item'

    product_id = fields.Many2one(comodel_name='supermarket.product', string="Product", required=True)
    quantity = fields.Integer('quantity')
    cart_id = fields.Many2one(comodel_name='supermarket.cart', string="cart", required=True)
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')

    @api.depends('product_id.unit_price', 'quantity')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.product_id.unit_price * record.quantity


class PremiumStatus(models.Model):
    _name = 'supermarket.premium.status'
    _description = "Premium Status"
    _inherit = 'supermarket.customer'

    premium = fields.Boolean(string='Premium Status', compute='_compute_premium_status', default=False)

    @api.depends('name')
    def _compute_premium_status(self):
        old_date = None
        days_dif = 10
        # Stores all the records of the carts made by a specific customer
        date_records = self.env['supermarket.cart'].search([('customer_id', '=', 'self.id')])
        # Iterates over all the records we got and checks the difference between the dates
        for rec in self:
            for record in date_records:
                new_date = record.date
                if old_date:
                    days_dif = (new_date - old_date).days
                # If the difference between carts created is less than a week, then the customer should be premium
                if days_dif < 7:
                    rec.premium = True
                old_date = new_date
            # If we passed the entire loop without finding a difference of less than a week, the customer is not premium
            rec.premium = False
  