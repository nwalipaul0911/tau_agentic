import json
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from faker import Faker

def generate_payroll_data(
    num_onboarding_requests: int = 40,
    num_payroll_runs: int = 20,
    num_orders: int = 30,
) -> dict:
    """
    Generates deterministic fake data for a payroll and invoice management system,
    enforcing dependencies based on the schema and business logic.
    The data simulates a 3-year history of operations.
    """
    Faker.seed(42)
    fake = Faker('en_US')

    def generate_id(prefix: str, count: int) -> str:
        """Generate a unique, incremental string ID with prefix and zero-padded number."""
        return f"{prefix}_{count:03d}"

    def deterministic_bank_account(prefix: str, count: int) -> str:
        """Return a deterministic bank account string."""
        return f"{prefix}{count:010d}"

    def deterministic_routing(count: int) -> str:
        """Return a deterministic 9-digit routing number derived from count."""
        return f"{(100000000 + (count % 900000000)):09d}"

    now = datetime(2025, 9, 23, 12, 0, 0, tzinfo=timezone.utc)
    start_base = now - timedelta(days=3 * 365)
    
    data = defaultdict(dict)

    # --- 1. Generate Departments (independent) ---
    num_departments = 5
    department_ids = []
    for i in range(1, num_departments + 1):
        dept_id = generate_id("dept", i)
        department_ids.append(dept_id)
        data["departments"][dept_id] = {
            "department_id": dept_id,
            "name": fake.job() + " Department",
            "head_id": None, 
        }

    # --- 2. Generate Onboarding Requests (dependent on departments for employees) ---
    onboarding_id_count = 0
    onboarding_entity_types = ["employee", "vendor"]
    for i in range(1, num_onboarding_requests + 1):
        onboarding_id_count += 1
        request_id = generate_id("onb", onboarding_id_count)

        entity_type = onboarding_entity_types[i % len(onboarding_entity_types)]
        
        created_at_dt = start_base + timedelta(days=((i - 1) * 365 * 3) // num_onboarding_requests)
        
        # A deterministic pattern where every other request is "approved"
        status_map = {0: "pending", 1: "approved", 2: "rejected"}
        status = status_map[i % 3]
        
        requested_by = f"emp_{onboarding_id_count % 5 + 1:03d}" # Placeholder ID
        department_id = department_ids[(i - 1) % len(department_ids)] if entity_type == "employee" else None
        
        data["onboarding_requests"][request_id] = {
            "request_id": request_id,
            "entity_type": entity_type,
            "department_id": department_id,
            "requested_by": requested_by,
            "requested_data": {
                "name": fake.name(),
                "role": fake.job(),
                "salary": round(80000 + (i % 5) * 15000, 2),
                "tax_id": f"TAX-{i:05d}",
                "bank_account_number": deterministic_bank_account(f'{entity_type[:4].upper()}', i),
                "bank_routing_number": deterministic_routing(i),
                "legal_name": fake.company(),
                "service": fake.catch_phrase(),
            },
            "status": status,
            "created_at": created_at_dt.isoformat(),
            "updated_at": now.isoformat(),
        }

    # --- 3. Onboard Employees & Vendors (dependent on approved requests) ---
    employee_ids = []
    vendor_ids = []
    emp_bank_counter = 0
    vend_bank_counter = 0

    for request_id, req in data["onboarding_requests"].items():
        if req["status"] == "approved":
            onb_data = req["requested_data"]
            onb_created_at = datetime.fromisoformat(req["created_at"])
            
            if req["entity_type"] == "employee":
                emp_bank_counter += 1
                employee_id = generate_id("emp", emp_bank_counter)
                employee_ids.append(employee_id)
                req["entity_id"] = employee_id
                data["employees"][employee_id] = {
                    "employee_id": employee_id,
                    "name": onb_data["name"],
                    "role": onb_data["role"],
                    "salary": onb_data["salary"],
                    "tax_id": onb_data["tax_id"],
                    "bank_account_number": onb_data["bank_account_number"],
                    "bank_routing_number": onb_data["bank_routing_number"],
                    "department_id": req["department_id"],
                    "created_at": onb_created_at.isoformat(),
                    "updated_at": now.isoformat(),
                    "status": "active",
                }
            elif req["entity_type"] == "vendor":
                vend_bank_counter += 1
                vendor_id = generate_id("vend", vend_bank_counter)
                vendor_ids.append(vendor_id)
                data["vendors"][vendor_id] = {
                    "vendor_id": vendor_id,
                    "legal_name": onb_data["legal_name"],
                    "tax_id": onb_data["tax_id"],
                    "bank_account_number": onb_data["bank_account_number"],
                    "bank_routing_number": onb_data["bank_routing_number"],
                    "service": onb_data["service"],
                    "created_at": onb_created_at.isoformat(),
                    "updated_at": now.isoformat(),
                    "status": "active",
                }

    # Link department heads to existing employees
    for i, dept_id in enumerate(department_ids):
        head_id = employee_ids[i % len(employee_ids)] if employee_ids else None
        data["departments"][dept_id]["head_id"] = head_id
    
    # --- 4. Generate Payroll Runs and Employee Pays (dependent on employees) ---
    payroll_run_ids = []
    employee_pay_id_count = 0
    run_dt = start_base
    for i in range(1, num_payroll_runs + 1):
        payroll_run_id = generate_id("prun", i)
        payroll_run_ids.append(payroll_run_id)

        start_date = run_dt
        end_date = start_date + timedelta(days=14)
        run_dt = end_date + timedelta(days=7)

        status_map = {0: "draft", 1: "pending_approval", 2: "approved", 3: "executed", 4: "failed"}
        status = status_map[i % len(status_map)]
        
        data["payroll_runs"][payroll_run_id] = {
            "payroll_run_id": payroll_run_id,
            "payroll_period_start": start_date.date().isoformat(),
            "payroll_period_end": end_date.date().isoformat(),
            "status": status,
            "created_at": start_date.isoformat(),
            "updated_at": now.isoformat(),
        }

        eligible_employees = [eid for eid, e in data["employees"].items() if datetime.fromisoformat(e["created_at"]) <= end_date]
        if not eligible_employees:
            continue 
        num_pays = max(1, len(eligible_employees) // 4)
        selected_employees = eligible_employees[i % len(eligible_employees) : (i % len(eligible_employees)) + num_pays]

        for emp in selected_employees:
            employee_pay_id_count += 1
            employee_pay_id = generate_id("epay", employee_pay_id_count)
            
            base_salary = data["employees"][emp]["salary"]
            gross_pay = round(base_salary / 24, 2)
            deductions = round(gross_pay * 0.2, 2)
            net_pay = gross_pay - deductions

            paid_at = end_date + timedelta(days=(employee_pay_id_count % 5))
            
            pay_status_map = {0: "pending", 1: "paid", 2: "failed", 3: "disputed"}
            pay_status = pay_status_map[employee_pay_id_count % len(pay_status_map)]

            data["employee_pays"][employee_pay_id] = {
                "pay_id": employee_pay_id,
                "employee_id": emp,
                "payroll_run_id": payroll_run_id,
                "gross_pay": gross_pay,
                "deductions": deductions,
                "net_pay": net_pay,
                "status": pay_status,
                "paid_at": paid_at.isoformat(),
            }

    # --- 5. Generate Orders and Invoices (dependent on vendors) ---
    order_ids = []
    invoice_id_count = 0
    for i in range(1, num_orders + 1):
        order_id = generate_id("ord", i)
        order_ids.append(order_id)
        
        vendor_id = vendor_ids[(i - 1) % len(vendor_ids)] if vendor_ids else None
        if not vendor_id: continue

        amount = round(500 + (i % 10) * 500, 2)
        order_dt = datetime.fromisoformat(data["vendors"][vendor_id]["created_at"]) + timedelta(days=((i - 1) * 365 * 3) // num_orders)
        created_at = order_dt.isoformat()
        updated_at = now.isoformat()
        
        order_status_map = {0: "open", 1: "fulfilled", 2: "cancelled"}
        status = order_status_map[i % len(order_status_map)]

        data["orders"][order_id] = {
            "order_id": order_id,
            "vendor_id": vendor_id,
            "order_type": ["goods", "services", "licensing"][i % 3],
            "description": f"Order {order_id} for {data['vendors'][vendor_id]['legal_name']}",
            "amount": amount,
            "status": status,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        
        invoice_id_count += 1
        invoice_id = generate_id("inv", invoice_id_count)
        
        invoice_dt = order_dt + timedelta(days=(i % 30))
        invoice_created_at = invoice_dt.isoformat()
        invoice_updated_at = now.isoformat()

        invoice_status_map = {0: "draft", 1: "pending_approval", 2: "approved", 3: "paid", 4: "rejected"}
        invoice_status = invoice_status_map[i % len(invoice_status_map)]
        
        data["invoices"][invoice_id] = {
            "invoice_id": invoice_id,
            "vendor_id": vendor_id,
            "order_id": order_id,
            "amount": amount,
            "due_date": (invoice_dt + timedelta(days=30)).date().isoformat(),
            "status": invoice_status,
            "created_at": invoice_created_at,
            "updated_at": invoice_updated_at,
        }
            
    # --- 6. Generate Payments (dependent on invoices and employee pays) ---
    payment_id_count = 0
    
    entity_ids = list(data["employee_pays"].keys()) + list(data["invoices"].keys())
    for i, entity_id in enumerate(entity_ids):
        payment_id_count += 1
        payment_id = generate_id("pay", payment_id_count)
        
        is_employee_pay = entity_id in data["employee_pays"]
        
        if is_employee_pay:
            entity_type = "employee_pay"
            amount = data["employee_pays"][entity_id]["net_pay"]
            start_date = datetime.fromisoformat(data["employee_pays"][entity_id]["paid_at"])
        else:
            entity_type = "invoice"
            amount = data["invoices"][entity_id]["amount"]
            start_date = datetime.fromisoformat(data["invoices"][entity_id]["created_at"])
        
        executed_at = start_date + timedelta(days=(i % 10))

        payment_status_map = {0: "completed", 1: "pending", 2: "failed"}
        status = payment_status_map[i % len(payment_status_map)]
        
        payment_method_map = {0: "bank_transfer", 1: "check", 2: "wallet"}
        method = payment_method_map[i % len(payment_method_map)]
        
        data["payments"][payment_id] = {
            "payment_id": payment_id,
            "entity_id": entity_id,
            "entity_type": entity_type,
            "amount": amount,
            "method": method,
            "status": status,
            "executed_at": executed_at.isoformat(),
        }

    # --- 7. Generate Approvals (dependent on other entities) ---
    approval_id_count = 0
    approval_entities = {
        "payroll_run": payroll_run_ids,
        "invoice": list(data["invoices"].keys()),
        "order": order_ids,
        "onboarding": list(data["onboarding_requests"].keys()),
    }
    
    for entity_type, entity_list in approval_entities.items():
        for i, entity_id in enumerate(entity_list):
            approval_id_count += 1
            approval_id = generate_id("app", approval_id_count)

            ent_created = now
            if entity_type == "payroll_run":
                ent_created = datetime.fromisoformat(data["payroll_runs"][entity_id]["created_at"])
            elif entity_type == "invoice":
                ent_created = datetime.fromisoformat(data["invoices"][entity_id]["created_at"])
            elif entity_type == "order":
                ent_created = datetime.fromisoformat(data["orders"][entity_id]["created_at"])
            elif entity_type == "onboarding":
                ent_created = datetime.fromisoformat(data["onboarding_requests"][entity_id]["created_at"])
            
            app_dt = ent_created + timedelta(days=(i % 10))
            
            decision_map = {0: "approved", 1: "rejected", 2: "escalated"}
            decision = decision_map[i % len(decision_map)]

            data["approvals"][approval_id] = {
                "approval_id": approval_id,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "approver_id": employee_ids[i % len(employee_ids)] if employee_ids else "system",
                "level": (i % 3) + 1,
                "decision": decision,
                "comments": f"Approval comments for {entity_type} {entity_id}",
                "created_at": app_dt.isoformat(),
                "updated_at": now.isoformat(),
            }

    # --- 8. Generate Disputes (dependent on other entities) ---
    dispute_id_count = 0
    dispute_entities = {
        "payroll": list(data["employee_pays"].keys()),
        "invoice": list(data["invoices"].keys()),
        "payment": list(data["payments"].keys()),
    }
    
    for dispute_type, entity_list in dispute_entities.items():
        for i, entity_id in enumerate(entity_list):
            if i % 5 == 0: 
                dispute_id_count += 1
                dispute_id = generate_id("disp", dispute_id_count)
                
                start_date = now
                if dispute_type == 'invoice':
                    start_date = datetime.fromisoformat(data["invoices"][entity_id]["created_at"])
                elif dispute_type == 'payroll':
                    start_date = datetime.fromisoformat(data["employee_pays"][entity_id]["paid_at"])
                else:
                    start_date = datetime.fromisoformat(data["payments"][entity_id]["executed_at"])
                
                created_at = start_date + timedelta(days=(i % 10))
                updated_at = now
                
                raised_by = employee_ids[i % len(employee_ids)] if dispute_type == "payroll" else (vendor_ids[i % len(vendor_ids)] if vendor_ids else "system")
                
                dispute_status_map = {0: "open", 1: "under_review", 2: "resolved", 3: "escalated"}
                status = dispute_status_map[i % len(dispute_status_map)]
                
                data["disputes"][dispute_id] = {
                    "dispute_id": dispute_id,
                    "dispute_type": dispute_type,
                    "entity_id": entity_id,
                    "raised_by": raised_by,
                    "description": f"Dispute for {dispute_type} ID: {entity_id}",
                    "resolution": f"Resolution for {dispute_type} dispute {dispute_id}",
                    "status": status,
                    "created_at": created_at.isoformat(),
                    "updated_at": updated_at.isoformat(),
                }

    # --- 9. Generate Offboarding Requests (dependent on employees/vendors) ---
    offboarding_id_count = 0
    entities_for_offboarding = [(eid, "employee") for eid in employee_ids] + [(vid, "vendor") for vid in vendor_ids]
    
    for i, (entity_id, entity_type) in enumerate(entities_for_offboarding):
        if i % 4 == 0: # Create an offboarding request every 4th entity
            offboarding_id_count += 1
            request_id = generate_id("off", offboarding_id_count)

            ent_created_at_str = data["employees"][entity_id]["created_at"] if entity_type == "employee" else data["vendors"][entity_id]["created_at"]
            ent_created_at_dt = datetime.fromisoformat(ent_created_at_str)
            
            created_at_dt = ent_created_at_dt + timedelta(days=(i % 30))
            
            status_map = {0: "pending", 1: "approved", 2: "rejected", 3: "completed"}
            status = status_map[i % len(status_map)]
            
            data["offboarding_requests"][request_id] = {
                "request_id": request_id,
                "entity_id": entity_id,
                "entity_type": entity_type,
                "reason": f"Offboarding reason for {entity_type} {entity_id}",
                "status": status,
                "created_at": created_at_dt.isoformat(),
                "updated_at": now.isoformat(),
            }
        
    # --- 10. Generate Audit Log (dependent on other entities) ---
    audit_id_count = 0
    audit_entities = {
        "payroll_run": payroll_run_ids,
        "invoice": list(data["invoices"].keys()),
        "payment": list(data["payments"].keys()),
        "onboarding": list(data["onboarding_requests"].keys()),
        "offboarding": list(data["offboarding_requests"].keys()),
    }
    
    all_entity_ids = []
    for etype, elist in audit_entities.items():
        all_entity_ids.extend([(etype, eid) for eid in elist])
        
    for i, (entity_type, entity_id) in enumerate(all_entity_ids):
        if i % 3 == 0:
            audit_id_count += 1
            audit_id = generate_id("audit", audit_id_count)
            
            audit_ts = now - timedelta(seconds=audit_id_count)
            
            action_map = {0: "created", 1: "approved", 2: "rejected", 3: "paid", 4: "updated"}
            action = action_map[i % len(action_map)]
            
            role_map = {0: "system", 1: "HR", 2: "Finance"}
            role = role_map[i % len(role_map)]
            
            data["audit_logs"][audit_id] = {
                "audit_id": audit_id,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "action_performed": action,
                "timestamp": audit_ts.isoformat(),
                "performed_by": employee_ids[i % len(employee_ids)] if employee_ids else "system",
                "role": role,
                "details": {},
            }
    
    return data

if __name__ == "__main__":
    generated_data = generate_payroll_data()
    
    # Save each table to a separate JSON file
    for table_name, table_data in generated_data.items():
        with open(f"data/{table_name}.json", "w") as f:
            json.dump(table_data, f, indent=2)

    print("Deterministic database seeding complete! JSON files have been created. 🎉")