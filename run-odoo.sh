#!/bin/bash
# يرجع خطوة لورا


# يفعل الـ virtual environment
# غيّر المسار لو venv عندك في مكان تاني
# source venv/bin/activate

# يطبع حالة لتأكيد التفعيل
# echo "Virtual environment activated: $(which python)"



python odoo-bin -c ./odoo.conf --dev=all -u construction_management