from .add_invoice import AddInvoice
from .amend_dispute_status import AmendDisputeStatus
from .dispatch_payment_externally import DispatchPaymentExternally
from .edit_employee_data import EditEmployeeData
from .edit_invoice_details import EditInvoiceDetails
from .edit_pay_record import EditPayRecord
from .edit_payment_details import EditPaymentDetails
from .edit_vendor_data import EditVendorData
from .finalize_approval import FinalizeApproval
from .finalize_dispute import FinalizeDispute
from .find_audit_entries import FindAuditEntries
from .find_pending_approvals import FindPendingApprovals
from .generate_payroll_draft import GeneratePayrollDraft
from .get_all_entities import GetAllEntities
from .initiate_approval import InitiateApproval
from .lookup_approval_request import LookupApprovalRequest
from .lookup_department import LookupDepartment
from .lookup_dispute import LookupDispute
from .lookup_employee import LookupEmployee
from .lookup_employee_pay import LookupEmployeePay
from .lookup_invoice import LookupInvoice
from .lookup_offboarding import LookupOffboarding
from .lookup_onboarding import LookupOnboarding
from .lookup_order import LookupOrder
from .lookup_payment import LookupPayment
from .lookup_payroll_run import LookupPayrollRun
from .lookup_vendor import LookupVendor
from .produce_pay_records import ProducePayRecords
from .record_payment import RecordPayment
from .register_employee import RegisterEmployee
from .register_vendor import RegisterVendor
from .report_issue import ReportIssue
from .request_offboarding_action import RequestOffboardingAction
from .set_offboarding_request_status import SetOffboardingRequestStatus
from .set_onboarding_request_status import SetOnboardingRequestStatus
from .write_to_audit_log import WriteToAuditLog

ALL_TOOLS_INTERFACE_4 = [
    AddInvoice,
    AmendDisputeStatus,
    DispatchPaymentExternally,
    EditEmployeeData,
    EditInvoiceDetails,
    EditPayRecord,
    EditPaymentDetails,
    EditVendorData,
    FinalizeApproval,
    FinalizeDispute,
    FindAuditEntries,
    FindPendingApprovals,
    GeneratePayrollDraft,
    GetAllEntities,
    InitiateApproval,
    LookupApprovalRequest,
    LookupDepartment,
    LookupDispute,
    LookupEmployee,
    LookupEmployeePay,
    LookupInvoice,
    LookupOffboarding,
    LookupOnboarding,
    LookupOrder,
    LookupPayment,
    LookupPayrollRun,
    LookupVendor,
    ProducePayRecords,
    RecordPayment,
    RegisterEmployee,
    RegisterVendor,
    ReportIssue,
    RequestOffboardingAction,
    SetOffboardingRequestStatus,
    SetOnboardingRequestStatus,
    WriteToAuditLog
]
