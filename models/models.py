# -*- coding: utf-8 -*-

from odoo import models, fields, api

import psutil
import socket


class instance_monitoring(models.Model):
    _name = 'odoo.instance.monitoring'
    _description = 'kzm_client_monitoring.kzm_client_monitoring'

    check_date = fields.Datetime(default=fields.Datetime.now)
    host_name = fields.Char(default=socket.gethostname())

    ram_capacity = fields.Float(default=psutil.virtual_memory().total)
    ram_available = fields.Float(default=psutil.virtual_memory().available)
    ram_consumption = fields.Float(compute='_compute_ram_consumption')

    disk_capacity = fields.Float(default=psutil.disk_usage('/').total)
    disk_available = fields.Float(default=psutil.disk_usage('/').free)
    disk_consumption = fields.Float(compute='_compute_disk_consumption')

    cpu_number = fields.Float(default=psutil.cpu_count())
    cpu_consumption = fields.Float(default=psutil.cpu_percent())
    cpu_freq = fields.Float(default=psutil.cpu_freq().current)

    @api.depends('ram_capacity', 'ram_available')
    def _compute_ram_consumption(self):
        for r in self:
            r.ram_consumption = 100.0 * (1 - r.ram_available / r.ram_capacity)

    @api.depends('disk_capacity', 'disk_available')
    def _compute_disk_consumption(self):
        for r in self:
            r.disk_consumption = 100.0 * (1 - r.disk_available / r.disk_capacity)

    @api.model
    def instance_create(self):
        data = {
            'host_name': socket.gethostname(),
            'ram_capacity': psutil.virtual_memory().total,
            'ram_available': psutil.virtual_memory().available,
            'disk_capacity': psutil.disk_usage('/').total,
            'disk_available': psutil.disk_usage('/').free,
            'cpu_number': psutil.cpu_count(),
            'cpu_consumption': psutil.cpu_percent(),
            'cpu_freq': psutil.cpu_freq().current,
        }
        self.env["odoo.instance.monitoring"].create(data)