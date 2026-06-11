# Advanced Construction Management Module

نظام متقدم وشامل لإدارة مشاريع المقاولات في Odoo.

## 📦 المرحلة الأولى - النسخة الأساسية (مكتملة ✅)

تم إنشاء البنية الأساسية للنظام مع جميع Models والعلاقات والحقول المحسوبة.

### 🧱 Layer 1: Core Operational Layer

#### Models المُنشأة:

1. **construction.project** ✅
   - Project Hub الأساسي
   - Computed Fields:
     - `actual_expense_cost` - مجموع المصاريف المعتمدة
     - `actual_labor_cost` - تكاليف العمالة من Timesheets
     - `actual_subcontract_cost` - تكاليف الـ Subcontractors
     - `actual_cost` - إجمالي التكاليف (بدون معدات)
     - `equipment_cost` - تكاليف المعدات
     - `total_actual_cost` - الإجمالي الشامل
     - `profit` - الربح (Budget - Total Cost)
     - `profit_margin` - نسبة الربح %
     - `progress` - الإنجاز الكلي %
     - `is_over_budget` - هل تجاوز الميزانية
   - Tracking & Activities enabled

2. **construction.stage** ✅
   - مراحل المشروع (Foundation, Structure, Finishing)
   - تتبع التقدم والتكاليف
   - State computation (not_started/in_progress/completed/delayed)

3. **construction.expense** ✅
   - سجل المصاريف
   - أنواع: Materials, Labor, Equipment, Other
   - Approval system

4. **construction.worker** ✅
   - إدارة العمال
   - Daily Rate التسعير

5. **construction.timesheet** ✅
   - تسجيل ساعات العمل
   - Auto-compute cost based on hours × daily_rate / 8

6. **construction.subcontract** ✅
   - إدارة الـ Subcontractors
   - Retention percentage handling
   - Auto-compute paid/remaining amounts

7. **construction.milestone** ✅
   - Milestones بنسبة من الميزانية
   - Auto-compute amount

8. **construction.boq** ✅
   - Bill of Quantities
   - Totals computation

9. **construction.boq_line** ✅
   - BOQ Lines with quantity/unit cost
   - Variance computation

10. **construction.change_order** ✅
    - Change Orders management
    - Auto-apply budget/end_date changes

11. **construction.equipment** ✅
    - Equipment master list
    - Daily cost tracking

12. **construction.equipment_usage** ✅
    - Equipment usage in projects
    - Auto-compute days and total cost

13. **construction.risk** ✅
    - Risk Register
    - Probability × Impact calculation

### 📊 Views المُنشأة:

✅ Form & List views لجميع Models
✅ Search views مع filters ديناميكية
✅ Tree views مع decorations
✅ Actions و Menu items

### 🔒 Security:

✅ `ir.model.access.csv` - Access control
✅ Groups: `group_construction_user` و `group_construction_manager`

### 📋 Data:

✅ Demo data شامل:
- عميل تجريبي
- عمال (مهندس + عامل)
- معدات (حفار + سقالة)
- مشروع سكني كامل
- مراحل البناء
- BOQ جاهز

## 🔥 Core Engine Features:

### Automatic Calculations:
```python
actual_expense_cost = SUM(approved expenses)
actual_labor_cost = SUM(timesheet costs)
actual_subcontract_cost = SUM(paid amounts)
actual_cost = expense_cost + labor_cost + subcontract_cost
equipment_cost = SUM(equipment usage costs)
total_actual_cost = actual_cost + equipment_cost
profit = budget - total_actual_cost
profit_margin = (profit / budget) * 100
progress = AVERAGE(stage progress)
```

### Performance Optimization:
- جميع الحقول المحسوبة مع `store=True`
- SQL constraints للتحقق من البيانات
- Proper indexing من خلال `_sql_constraints`

## 📁 File Structure:

```
adv_construction_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── construction_project.py
│   ├── construction_stage.py
│   ├── construction_expense.py
│   ├── construction_worker.py
│   ├── construction_timesheet.py
│   ├── construction_subcontract.py
│   ├── construction_milestone.py
│   ├── construction_boq.py
│   ├── construction_boq_line.py
│   ├── construction_change_order.py
│   ├── construction_equipment.py
│   ├── construction_equipment_usage.py
│   └── construction_risk.py
├── views/
│   ├── construction_project_views.xml
│   ├── construction_stage_views.xml
│   ├── construction_expense_views.xml
│   ├── construction_worker_views.xml
│   ├── construction_timesheet_views.xml
│   ├── construction_subcontract_views.xml
│   ├── construction_milestone_views.xml
│   ├── construction_boq_views.xml
│   ├── construction_change_order_views.xml
│   ├── construction_equipment_views.xml
│   ├── construction_risk_views.xml
│   ├── dashboard_view.xml (placeholder)
│   ├── kanban_custom_view.xml (placeholder)
│   ├── cost_matrix_view.xml (placeholder)
│   └── timeline_view.xml (placeholder)
├── security/
│   └── ir.model.access.csv
├── data/
│   └── demo_data.xml
├── static/
│   └── src/
│       ├── js/ (placeholder controllers)
│       ├── css/ (placeholder styles)
│       └── xml/ (placeholder templates)
└── report/
```

## 🚀 الخطوات التالية (في انتظار التطوير):

1. ✅ **Layer 1** - مكتمل
2. ⏳ **Layer 2** - BOQ & Change Orders (مكتمل في Models)
3. ⏳ **Layer 3** - Equipment (مكتمل في Models)
4. ⏳ **Support Systems** - Risk Register (مكتمل)
5. ⏳ **Dashboard** - Executive Dashboard (في الانتظار)
6. ⏳ **Custom Kanban** - Kanban View مخصصة (في الانتظار)
7. ⏳ **Cost Matrix View** - Advanced reporting (في الانتظار)
8. ⏳ **Timeline View** - Interactive timeline (في الانتظار)

## 📝 الميزات المُتضمنة:

✅ Multi-layer architecture
✅ Automatic cost calculations
✅ Full expense tracking
✅ Labor cost management
✅ Subcontractor payments
✅ Equipment usage tracking
✅ Milestone management
✅ Change order handling
✅ Risk register
✅ BOQ integration
✅ Real-time profit calculations
✅ Over-budget alerts
✅ Progress tracking
✅ Mail thread integration
✅ Activity tracking
✅ Access control

## 🔐 Test Data Available:

- Project: "Residential Building - Cairo"
- Budget: EGP 10,000,000
- Duration: Jan 15 - Dec 31, 2024
- 3 Stages: Foundation, Structure, Finishing
- 2 Workers: Engineer (EGP 800/day), Laborer (EGP 400/day)
- 2 Equipment: Excavator (EGP 5,000/day), Scaffold (EGP 1,000/day)

## 📌 Notes:

- جميع الحقول المحسوبة مُخزّنة في DB للأداء
- Constraints SQL لضمان data integrity
- Views تدعم decorations حسب الحالة
- Menu structure متسلسل وسهل التنقل

---

**Version**: 1.0.0
**Status**: Phase 1 Complete - Ready for Frontend Development
