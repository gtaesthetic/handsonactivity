# Testing Claims and Leave Functions

This document provides instructions on how to test the claims and leave functionality in the backend.

## Prerequisites

1. Make sure your Django backend server is running (`python manage.py runserver`)
2. Ensure test users have been created (run `python create_test_users.py` if needed)
3. Make sure at least one leave type exists in the database (ID 1 is expected by the test script)

## Testing Claims

The test script will:
1. Login as an employee and submit a new claim
2. Login as HR and approve the submitted claim

## Testing Leave Requests

The test script will:
1. Login as an employee and submit a new leave request
2. Login as HR and approve the submitted leave request

## Running the Tests

To run the tests, execute the following command:

```bash
python test_claims_leave.py
```

This will produce a detailed output showing the results of each test case.

## Troubleshooting

If tests fail, check the following:

1. **Backend server**: Make sure the Django server is running on `http://localhost:8000`
2. **User credentials**: Ensure test users exist with the correct credentials:
   - `employee@test.com` (password: `employee123`)
   - `hr@test.com` (password: `hr123`)
3. **Leave Types**: Ensure at least one leave type exists with ID = 1
   - You can create it through Django admin interface
4. **Database migrations**: Make sure all migrations are applied

## Manual Testing

You can also test the endpoints manually using tools like cURL or Postman:

### Claims

1. Submit a claim:
```
POST /api/claims/new/
{
    "claim_type": "medical",
    "amount": 1500,
    "currency": "PHP",
    "bill_no": "TEST123",
    "bill_date": "2023-04-01",
    "supplier": "Test Hospital",
    "claimant": "Test Employee",
    "claim_date": "2023-04-01",
    "claim_due_date": "2023-04-02",
    "remarks": "Test claim submission"
}
```

2. Approve a claim:
```
POST /api/claims/{claim_id}/approve_reject/
{
    "action": "approve"
}
```

### Leave Requests

1. Submit a leave request:
```
POST /api/leaves/submit/
{
    "leave_type": 1,
    "start_date": "2023-04-10",
    "end_date": "2023-04-15",
    "reason": "Test leave request"
}
```

2. Approve a leave request:
```
POST /api/leaves/{leave_id}/approve_reject/
{
    "action": "approve"
}
``` 