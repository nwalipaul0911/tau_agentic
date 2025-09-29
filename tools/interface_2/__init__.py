from .create_payroll_batch import CreatePayrollBatch
from .fetch_approval_request import FetchApprovalRequest
from .fetch_audit_logs import FetchAuditLogs
from .fetch_department import FetchDepartment
from .fetch_dispute import FetchDispute
from .fetch_employee import FetchEmployee
from .fetch_employee_pay import FetchEmployeePay
from .fetch_invoice import FetchInvoice
from .fetch_offboarding_request import FetchOffboardingRequest
from .fetch_onboarding_request import FetchOnboardingRequest
from .fetch_order import FetchOrder
from .fetch_payment import FetchPayment
from .fetch_payroll_run import FetchPayrollRun
from .fetch_pending_approvals import FetchPendingApprovals
from .fetch_vendor import FetchVendor
from .generate_new_invoice import GenerateNewInvoice
from .generate_payment import GeneratePayment
from .log_audit_event import LogAuditEvent
from .make_approval_decision import MakeApprovalDecision
from .modify_employee_pay import ModifyEmployeePay
from .modify_employee_record import ModifyEmployeeRecord
from .modify_invoice_record import ModifyInvoiceRecord
from .modify_offboarding_status import ModifyOffboardingStatus
from .modify_onboarding_status import ModifyOnboardingStatus
from .modify_payment_record import ModifyPaymentRecord
from .modify_vendor_record import ModifyVendorRecord
from .onboard_employee import OnboardEmployee
from .onboard_vendor import OnboardVendor
from .process_external_payment import ProcessExternalPayment
from .raise_dispute import RaiseDispute
from .request_approval import RequestApproval
from .search_data import SearchData
from .set_dispute_status import SetDisputeStatus
from .settle_dispute import SettleDispute
from .start_new_payroll import StartNewPayroll
from .start_offboarding import StartOffboarding

ALL_TOOLS_INTERFACE_2 = [
    CreatePayrollBatch,
    FetchApprovalRequest,
    FetchAuditLogs,
    FetchDepartment,
    FetchDispute,
    FetchEmployee,
    FetchEmployeePay,
    FetchInvoice,
    FetchOffboardingRequest,
    FetchOnboardingRequest,
    FetchOrder,
    FetchPayment,
    FetchPayrollRun,
    FetchPendingApprovals,
    FetchVendor,
    GenerateNewInvoice,
    GeneratePayment,
    LogAuditEvent,
    MakeApprovalDecision,
    ModifyEmployeePay,
    ModifyEmployeeRecord,
    ModifyInvoiceRecord,
    ModifyOffboardingStatus,
    ModifyOnboardingStatus,
    ModifyPaymentRecord,
    ModifyVendorRecord,
    OnboardEmployee,
    OnboardVendor,
    ProcessExternalPayment,
    RaiseDispute,
    RequestApproval,
    SearchData,
    SetDisputeStatus,
    SettleDispute,
    StartNewPayroll,
    StartOffboarding
]
