# -*- coding: utf-8 -*-

from odoo import models, fields, api

import psutil
import socket


class instance_monitoring(models.Model):
    _name = 'odoo.instance.monitoring'
    _description = 'kzm_client_monitoring.kzm_client_monitoring'

    check_date = fields.Datetime(default=fields.Datetime.now)
    host_name = fields.Char(default=socket.gethostname())

    ram_capacity = fields.Float(default=psutil.virtual_memory().total / (2**30))
    ram_available = fields.Float(default=psutil.virtual_memory().available / (2**30))
    ram_consumption = fields.Float(compute='_compute_ram_consumption')

    disk_capacity = fields.Float(default=psutil.disk_usage('/').total / (2**30))
    disk_available = fields.Float(default=psutil.disk_usage('/').free / (2**30))
    disk_consumption = fields.Float(compute='_compute_disk_consumption')

    cpu_number = fields.Float(default=psutil.cpu_count())
    cpu_consumption = fields.Float(default=psutil.cpu_percent())
    cpu_freq = fields.Float(default=psutil.cpu_freq().current)
    cpu_freq_min = fields.Float(default=psutil.cpu_freq().min)
    cpu_freq_max = fields.Float(default=psutil.cpu_freq().max)

    state = fields.Selection([("0", "NOK"), ("1", "OK")],compute='_compute_host_consumption')
    color = fields.Integer(compute='_compute_host_color')

    @api.depends('state')
    def _compute_host_color(self):
        for r in self:
            if r.state == '0':
                r.color = 1
            else:
                r.color = -1


    @api.depends('ram_capacity', 'ram_available')
    def _compute_ram_consumption(self):
        for r in self:
            r.ram_consumption = 100.0 * (1 - r.ram_available / r.ram_capacity)

    @api.depends('disk_capacity', 'disk_available')
    def _compute_disk_consumption(self):
        for r in self:
            r.disk_consumption = 100.0 * (1 - r.disk_available / r.disk_capacity)

    @api.depends('disk_available','ram_consumption','cpu_consumption')
    def _compute_host_consumption(self):
        for r in self:
            if r.disk_available < 2 or r.ram_consumption > 90 or r.cpu_consumption > 90:
                r.state = '0'
            else:
                r.state = '1'


    @api.model
    def instance_create(self):
        data = {
            'host_name': socket.gethostname(),
            'ram_capacity': psutil.virtual_memory().total / (2**30),
            'ram_available': psutil.virtual_memory().available / (2**30),
            'disk_capacity': psutil.disk_usage('/').total / (2**30),
            'disk_available': psutil.disk_usage('/').free / (2**30),
            'cpu_number': psutil.cpu_count(),
            'cpu_consumption': psutil.cpu_percent(),
            'cpu_freq': psutil.cpu_freq().current,
            'cpu_freq_min' : psutil.cpu_freq().min,
            'cpu_freq_max' : psutil.cpu_freq().max
        }
        self.env["odoo.instance.monitoring"].create(data)

    @api.model
    def instance_create_server(self):
        data = {
            'host_name': socket.gethostname(),
            'ram_capacity': psutil.virtual_memory().total / (2**30),
            'ram_available': psutil.virtual_memory().available / (2**30),
            'disk_capacity': psutil.disk_usage('/').total / (2**30),
            'disk_available': psutil.disk_usage('/').free / (2**30),
            'cpu_number': psutil.cpu_count(),
            'cpu_consumption': psutil.cpu_percent(),
            'cpu_freq': psutil.cpu_freq().current,
        }
        return data