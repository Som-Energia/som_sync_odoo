# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.osv.orm import except_orm

class SyncError(except_orm):
    """ Syncronization with OpenERP error.
    Example: When you try write or delete an object created from OpenERP."""
    def __init__(self, msg):
        super(SyncError, self).__init__(msg)


class ResPartner(models.Model):
    _inherit = ['res.partner']
    _name = 'res.partner'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

    @api.multi
    def write(self, vals):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot modify this Partner from Odoo. You have to do it from OpenERP'))
        return super(ResPartner, self).write(vals)

    @api.multi
    def unlink(self):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot delete this Partner from Odoo. You have to do it from OpenERP'))
        return super(ResPartner, self).unlink()

class AccountJournal(models.Model):
    _inherit = ['account.journal']
    _name = 'account.journal'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

    @api.multi
    def write(self, vals):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot modify this Journal from Odoo. You have to do it from OpenERP'))
        return super(AccountJournal, self).write(vals)

    @api.multi
    def unlink(self):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot delete this Journal from Odoo. You have to do it from OpenERP'))
        return super(AccountJournal, self).unlink()

class AccountAccount(models.Model):
    _inherit = ['account.account']
    _name = 'account.account'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

    @api.multi
    def write(self, vals):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot modify this Account from Odoo. You have to do it from OpenERP'))
        return super(AccountAccount, self).write(vals)

    @api.multi
    def unlink(self):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot delete this Account from Odoo. You have to do it from OpenERP'))
        return super(AccountAccount, self).unlink()

class AccountAccountType(models.Model):
    _inherit = ['account.account.type']
    _name = 'account.account.type'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

    @api.multi
    def write(self, vals):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot modify this Account Type from Odoo. You have to do it from OpenERP'))
        return super(AccountAccountType, self).write(vals)

    @api.multi
    def unlink(self):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot delete this Account Type from Odoo. You have to do it from OpenERP'))
        return super(AccountAccountType, self).unlink()

class AccountMove(models.Model):
    _inherit = ['account.move']
    _name = 'account.move'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

    @api.multi
    def write(self, vals):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot modify this Move from Odoo. You have to do it from OpenERP'))
        return super(AccountMove, self).write(vals)

    @api.multi
    def unlink(self):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot delete this Move from Odoo. You have to do it from OpenERP'))
        return super(AccountMove, self).unlink()


class AccountMoveLine(models.Model):
    _inherit = ['account.move.line']
    _name = 'account.move.line'

    openerp_id = fields.Integer('ID in OpenERP', readonly=True,
            help="ID in OpenERP for syncronization")

    @api.multi
    def write(self, vals):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot modify this Move Line from Odoo. You have to do it from OpenERP'))
        return super(AccountMoveLine, self).write(vals)

    @api.multi
    def unlink(self):
        if self.read(['openerp_id'])[0]['openerp_id']:
            raise SyncError(_('You cannot delete this Move Line from Odoo. You have to do it from OpenERP'))
        return super(AccountMoveLine, self).unlink()

