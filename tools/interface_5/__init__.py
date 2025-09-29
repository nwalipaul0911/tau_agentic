from .amend_employee import AmendEmployee
from .amend_invoice import AmendInvoice
from .amend_offboarding_details import AmendOffboardingDetails
from .amend_onboarding_details import AmendOnboardingDetails
from .amend_pay_details import AmendPayDetails
from .amend_payment import AmendPayment
from .amend_vendor import AmendVendor
from .calculate_and_generate_pays import CalculateAndGeneratePays
from .end_dispute_process import EndDisputeProcess
from .get_approval_queue import GetApprovalQueue
from .initiate_disbursement import InitiateDisbursement
from .make_approval_request import MakeApprovalRequest
from .make_employee_record import MakeEmployeeRecord
from .make_vendor_record import MakeVendorRecord
from .modify_dispute_status import ModifyDisputeStatus
from .open_new_dispute import OpenNewDispute
from .process_approval_request import ProcessApprovalRequest
from .read_approval_record import ReadApprovalRecord
from .read_audit_trail import ReadAuditTrail
from .read_department_record import ReadDepartmentRecord
from .read_dispute_record import ReadDisputeRecord
from .read_employee_pay_record import ReadEmployeePayRecord
from .read_employee_record import ReadEmployeeRecord
from .read_invoice_record import ReadInvoiceRecord
from .read_offboarding_record import ReadOffboardingRecord
from .read_onboarding_record import ReadOnboardingRecord
from .read_order_record import ReadOrderRecord
from .read_payment_record import ReadPaymentRecord
from .read_payroll_run_record import ReadPayrollRunRecord
from .read_vendor_record import ReadVendorRecord
from .record_invoice import RecordInvoice
from .record_offboarding_request import RecordOffboardingRequest
from .record_system_action import RecordSystemAction
from .retrieve_data import RetrieveData
from .run_payroll import RunPayroll
from .transfer_funds_to_account import TransferFundsToAccount

ALL_TOOLS_INTERFACE_5 = [
    AmendEmployee,
    AmendInvoice,
    AmendOffboardingDetails,
    AmendOnboardingDetails,
    AmendPayDetails,
    AmendPayment,
    AmendVendor,
    CalculateAndGeneratePays,
    EndDisputeProcess,
    GetApprovalQueue,
    InitiateDisbursement,
    MakeApprovalRequest,
    MakeEmployeeRecord,
    MakeVendorRecord,
    ModifyDisputeStatus,
    OpenNewDispute,
    ProcessApprovalRequest,
    ReadApprovalRecord,
    ReadAuditTrail,
    ReadDepartmentRecord,
    ReadDisputeRecord,
    ReadEmployeePayRecord,
    ReadEmployeeRecord,
    ReadInvoiceRecord,
    ReadOffboardingRecord,
    ReadOnboardingRecord,
    ReadOrderRecord,
    ReadPaymentRecord,
    ReadPayrollRunRecord,
    ReadVendorRecord,
    RecordInvoice,
    RecordOffboardingRequest,
    RecordSystemAction,
    RetrieveData,
    RunPayroll,
    TransferFundsToAccount
]
