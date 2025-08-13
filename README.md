# Machinery Maintenance - Odoo 17 Module

A simple but powerful maintenance management system for tracking industrial equipment. Built for real manufacturing environments where you need to track machines, schedule maintenance, and manage parts ordering.

## What It Does

- **Track your machines** - Serial numbers, locations, who's responsible
- **Maintenance reports** - Document what happened, what needs fixing
- **Approval workflow** - Submit reports, get supervisor approval
- **Auto-order parts** - When you mark "needs part", it creates a purchase order
- **Activity notifications** - Assigned techs get notified automatically
- **Full audit trail** - Every action is logged with timestamps

## Main Features

### Machine Management
- Add machines with details (serial number, manufacturer, location)
- Assign technicians to specific machines
- Track status: Healthy, Due Soon, Under Repair

### Maintenance Reports
Three types of reports:
- **"Good to go!"** - Everything's working fine
- **"Preventive advice"** - Something to watch or fix soon  
- **"Needs part"** - Auto-creates purchase orders

### Workflow
1. Technician creates maintenance report
2. Submits for approval
3. Supervisor approves/rejects with reasons
4. If approved and needs parts → automatic purchase order
5. Mark as "Done" when complete

## Installation

### What You Need
- Odoo 17
- A custom-addons folder in your Odoo setup

### Steps
1. **Download/Clone** this repo into your custom-addons folder:
   ```bash
   cd /path/to/odoo/custom-addons
   git clone https://github.com/AviRamoutar/MachineRegistryOdoo.git machinery_maintenance
   ```

2. **Check the files are there**:
   ```
   machinery_maintenance/
   ├── __init__.py
   ├── __manifest__.py  
   ├── controllers/
   ├── data/
   ├── demo/
   ├── models/
   ├── security/
   └── views/
   ```

3. **Restart Odoo and install**:
   ```bash
   ./odoo-bin -c odoo.conf -d your_database_name -u machinery_maintenance
   ```

4. **Or install through the UI**:
   - Turn on Developer Mode (Settings → Developer Tools)
   - Apps → Update Apps List 
   - Search "Machinery Maintenance"
   - Install

## How to Use

### Add Your First Machine
1. Go to **Machinery → Machines**
2. Click **New**
3. Fill in: Name, Serial Number, Location, etc.
4. Assign a technician (they'll get notified)

### Create a Maintenance Report
1. **Machinery → Maintenance Reports → New**
2. Pick the machine
3. Choose report type:
   - **Good to go** = routine maintenance completed
   - **Preventive advice** = "watch this, might need attention soon"
   - **Needs part** = broken, requires parts (auto-creates purchase order)
4. **Write detailed notes** - the text area is full-width now and supports professional formatting
5. **Submit for Approval**

### Example Professional Report
```
MONTHLY CALIBRATION COMPLETED SUCCESSFULLY

Performance Metrics:
✓ All 3 axes calibrated within 0.001" tolerance
✓ Spindle bearings sound normal at all speeds  
✓ Tool changer: 47 tool changes tested - all successful
✓ Coolant system pressure at 45 PSI (normal)

STATUS: READY FOR PRODUCTION
Next calibration due: 30 days
```

### Approval Process
- Supervisors get activity notifications when reports are submitted
- They can **Approve** (auto-creates purchase orders if parts needed)
- Or **Reject** with detailed reasons
- Everything gets logged in the chatter for audit trails

## What's Different About This Module

- **Actually works** - No broken kanban views or JavaScript errors
- **Professional formatting** - Notes field spans full width, proper text wrapping
- **Real workflow** - Submit → Approve → Execute with proper notifications
- **Integration** - Ties into Odoo's purchasing system seamlessly
- **Practical** - Built for real manufacturing environments, not just demos

## Sample Use Cases

- **CNC machines** needing calibration tracking
- **Hydraulic presses** with safety-critical maintenance
- **Conveyor systems** requiring belt tension monitoring  
- **Robots** needing predictive maintenance alerts
- **Any industrial equipment** where downtime costs money

## Tech Notes

- Built for Odoo 17 (should work on 16+ but tested on 17)
- Uses standard Odoo patterns (mail.thread, activities, purchase integration)
- Custom CSS fixes Odoo's form layout constraints for better user experience
- No external dependencies beyond base Odoo modules

## Contributing

Found a bug? Want to add a feature? 
- Open an issue
- Submit a pull request  
- Keep it simple and practical

## License

LGPL-3 (same as Odoo)

---

Preview Images:
<img width="1910" height="814" alt="Screenshot 2025-08-13 165926" src="https://github.com/user-attachments/assets/3c3daebc-1726-4be3-942d-758bf86ad4a5" />

<img width="1629" height="857" alt="Screenshot 2025-08-13 165906" src="https://github.com/user-attachments/assets/afab5c12-513b-4e6e-a9f4-5d716170fc25" />

<img width="1913" height="864" alt="Screenshot 2025-08-13 165811" src="https://github.com/user-attachments/assets/815bdb7b-46d1-47db-965a-8365932a3d0f" />
