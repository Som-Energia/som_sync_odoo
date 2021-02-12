# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    #_inherit = 'res.partner'
    _inherit = ['res.partner']
    _name = 'res.partner'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")
