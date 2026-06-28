#!/bin/bash
source .venv/bin/activate
python3 odoo-bin -c odoo.conf -u purchase_discount -d odoo19
