from .add_new_employee import AddNewEmployee
from .add_new_vendor import AddNewVendor
from .approve_or_reject import ApproveOrReject
from .change_dispute_state import ChangeDisputeState
from .change_employee_details import ChangeEmployeeDetails
from .change_employee_pay_status import ChangeEmployeePayStatus
from .change_invoice_status import ChangeInvoiceStatus
from .change_offboarding_record import ChangeOffboardingRecord
from .change_onboarding_record import ChangeOnboardingRecord
from .change_payment_status import ChangePaymentStatus
from .change_vendor_details import ChangeVendorDetails
from .close_dispute_case import CloseDisputeCase
from .create_audit_record import CreateAuditRecord
from .filter_records import FilterRecords
from .find_approval_by_id import FindApprovalById
from .find_department_by_id import FindDepartmentById
from .find_dispute_by_id import FindDisputeById
from .find_employee_by_id import FindEmployeeById
from .find_employee_pay_by_id import FindEmployeePayById
from .find_invoice_by_id import FindInvoiceById
from .find_offboarding_by_id import FindOffboardingById
from .find_onboarding_by_id import FindOnboardingById
from .find_order_by_id import FindOrderById
from .find_payment_by_id import FindPaymentById
from .find_payroll_run_by_id import FindPayrollRunById
from .find_vendor_by_id import FindVendorById
from .get_entity_audits import GetEntityAudits
from .initiate_offboarding import InitiateOffboarding
from .initiate_payroll_period import InitiatePayrollPeriod
from .list_unapproved_requests import ListUnapprovedRequests
from .log_dispute import LogDispute
from .process_employee_salaries import ProcessEmployeeSalaries
from .process_payment import ProcessPayment
from .send_funds import SendFunds
from .submit_for_approval import SubmitForApproval
from .submit_invoice import SubmitInvoice

ALL_TOOLS_INTERFACE_3 = [
    AddNewEmployee,
    AddNewVendor,
    ApproveOrReject,
    ChangeDisputeState,
    ChangeEmployeeDetails,
    ChangeEmployeePayStatus,
    ChangeInvoiceStatus,
    ChangeOffboardingRecord,
    ChangeOnboardingRecord,
    ChangePaymentStatus,
    ChangeVendorDetails,
    CloseDisputeCase,
    CreateAuditRecord,
    FilterRecords,
    FindApprovalById,
    FindDepartmentById,
    FindDisputeById,
    FindEmployeeById,
    FindEmployeePayById,
    FindInvoiceById,
    FindOffboardingById,
    FindOnboardingById,
    FindOrderById,
    FindPaymentById,
    FindPayrollRunById,
    FindVendorById,
    GetEntityAudits,
    InitiateOffboarding,
    InitiatePayrollPeriod,
    ListUnapprovedRequests,
    LogDispute,
    ProcessEmployeeSalaries,
    ProcessPayment,
    SendFunds,
    SubmitForApproval,
    SubmitInvoice
]
