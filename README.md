Machinery Maintenance – Odoo Custom Module

This custom Odoo module provides a centralized registry for tracking machinery and equipment in an organization.
It allows users to:

- Maintain a detailed list of machines with serial numbers, statuses, and maintenance dates.

- View machinery records in list, form, and Kanban layouts for flexible management.

- Quickly add, edit, or delete machines from the registry.

- Organize machines by their current status (e.g., Healthy, Due Soon, Under Repair).

- Store upcoming maintenance schedules for proactive servicing.





*** INSTALLATION ***

(If you dont have a CustomAddons folder just create one on the same level as the basic addons folder in structure)

1. Clone into Your  Own Custom Addons Directory 
From inside your Odoo server (where your custom-addons folder is):

cd /path/to/odoo/custom-addons
git clone [https://github.com/AviRamoutar/MachineRegistryOdoo.git machinery_maintenance](https://github.com/AviRamoutar/MachineRegistryOdoo/)


2. Check Folder Structure
    
Make Sure your custom addons folder contains this

machinery_maintenance/
  ├── __init__.py  
  
  ├── __manifest__.py
  
  ├── models/
  
  ├── views/
  
  ├── security/
  
  ├── data/




3. Restart Odoo and run this in the root directory
./odoo-bin -c odoo.conf -d <your_database_name> -u machinery_maintenance



4. Activate Dev Mode in the UI settings tab then
   Apps--> Update Apps List --> Search Machinery Maintenance --> Install/Upgrade


Preview Image

<img width="1918" height="870" alt="Machinery Test" src="https://github.com/user-attachments/assets/6799619f-ccdf-45c0-91eb-eda04c234cac" />
