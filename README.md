# Split-Expenses

Split-Expenses is currently a FastAPI backend prototype for an expense-sharing app.

The product direction is evolving from a simple Splitwise-style backend into a private, offline-first mobile app for shared expenses, settlements, and personal lending.

## Current Development State

The repository currently contains:

- FastAPI application entry point.
- Auth endpoints for signup and token login.
- User profile update and user search endpoints.
- Basic group creation, listing, details, add member, and remove member logic.
- Early expense schema and service work.
- Supabase connection setup.

This backend is still experimental. The next major architecture decision is whether to keep the backend as a traditional source of truth or move toward an encrypted sync relay for a mobile offline-first app.

## Product Direction

The planned app should support:

- Android and iPhone mobile apps.
- Offline-first expense tracking.
- Local group and expense storage.
- Sync-later behavior when internet becomes available.
- Optional encrypted cloud sync.
- Group updates shared between members.
- Cash settlements.
- UPI-assisted settlements through installed UPI apps.
- Payment confirmation notifications.
- Future personal lending and private borrower insights.

## Privacy Goal

The long-term goal is that readable expense and payment details should live on user devices, not on the backend.

The backend should eventually store only encrypted sync events and delivery metadata, such as group id, device id, timestamps, and sync status.

## Current Backend Stack

- FastAPI
- Supabase/PostgreSQL
- JWT auth
- bcrypt password hashing

