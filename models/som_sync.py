# -*- coding: utf-8 -*-

from odoo import models, fields

class ResPartner(models.Model):
    #_inherit = 'res.partner'
    _inherit = ['res.partner']
    _name = 'res.partner'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")


class AccountJournal(models.Model):
    _inherit = ['account.journal']
    _name = 'account.journal'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

class AccountAccount(models.Model):
    _inherit = ['account.account']
    _name = 'account.account'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

class AccountMove(models.Model):
    _inherit = ['account.move']
    _name = 'account.move'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

class AccountMoveLine(models.Model):
    _inherit = ['account.move.line']
    _name = 'account.move.line'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

class AccountPeriod(models.Model):
    _inherit = ['account.period']
    _name = 'account.period'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")
