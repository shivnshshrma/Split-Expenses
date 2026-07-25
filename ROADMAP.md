# Split-Expenses Roadmap

## Product Direction

Split-Expenses is moving toward a private, offline-first mobile app for shared expenses, settlements, and personal lending.

The core idea is not to store readable financial data on the server. Expenses, balances, settlements, and lending records should live locally on user devices first. When users choose to sync with other group members, the backend should act as an encrypted event relay.

## Guiding Principles

- Mobile-first for Android and iPhone.
- Offline-first: users can create groups, add expenses, settle balances, and track lending without internet.
- Sync-later: changes made offline are queued and synced when internet is available.
- Privacy-first: the backend should not be able to read transaction details.
- Group-aware: expenses created by one member should eventually appear on other members' devices.
- Payment-aware: support cash settlement and UPI-assisted settlement.
- Trust-aware: future lending features may include private borrower insights based on the lender's own history.

## Phase 0: Current Backend Foundation

- [ ] Restore and maintain `ROADMAP.md`.
- [ ] Add `.gitignore` for local/generated files such as `.env`, `node_modules/`, and `__pycache__/`.
- [ ] Keep FastAPI auth, user, and group APIs working while the product direction evolves.
- [ ] Fix route consistency with the current API design.
- [ ] Ensure protected endpoints never return password hashes.
- [ ] Decide whether user references should use usernames, UUIDs, or both.
- [ ] Document required environment variables.

## Phase 1: Product Architecture Decision

- [ ] Choose mobile framework: Expo React Native or Flutter.
- [ ] Choose local database: SQLite is the preferred default.
- [ ] Decide backend role: encrypted sync relay, not full readable source of truth.
- [ ] Define local data ownership model.
- [ ] Define group invite flow.
- [ ] Define event sync model.
- [ ] Define how conflicts will be handled when multiple users edit offline.

## Phase 2: Offline-First Mobile MVP

- [ ] Create mobile app project.
- [ ] Add local SQLite storage.
- [ ] Add local user profile.
- [ ] Create groups locally.
- [ ] Add group members locally.
- [ ] Add expenses locally.
- [ ] Support split types: equal, exact, percentage.
- [ ] Calculate balances locally.
- [ ] Record cash settlements locally.
- [ ] Show pending/synced state for local changes.

## Phase 3: Encrypted Group Sync

- [ ] Create sync event model.
- [ ] Add local outbox for pending events.
- [ ] Add backend tables for users, devices, groups, group members, encrypted events, and sync cursors.
- [ ] Upload encrypted events when online.
- [ ] Download encrypted events for groups where the user is a member.
- [ ] Apply downloaded events to local database.
- [ ] Track per-device sync state.
- [ ] Show sync status inside the app.
- [ ] Handle duplicate events safely.

## Phase 4: Group Collaboration

- [ ] Invite users to groups.
- [ ] Accept or reject group invites.
- [ ] Add members to encrypted groups.
- [ ] Remove members from groups.
- [ ] Decide what removed members can still see from old history.
- [ ] Notify members when a group update is available.
- [ ] Support manual refresh and background sync.

## Phase 5: Expenses and Balances

- [ ] Add expense categories.
- [ ] Edit expenses.
- [ ] Delete expenses.
- [ ] Attach notes to expenses.
- [ ] Calculate per-group balances.
- [ ] Simplify debts to minimize settlement transactions.
- [ ] Calculate total balance across all groups.
- [ ] Add audit history for expense changes.

## Phase 6: Settlements and UPI-Assisted Payments

- [ ] Record cash settlement.
- [ ] Generate UPI payment intent/deep link for settlement.
- [ ] Let user choose installed UPI app such as Google Pay, PhonePe, Paytm, or BHIM.
- [ ] Return user to the app after payment attempt.
- [ ] Let payer mark payment as completed.
- [ ] Notify receiver that payment confirmation is requested.
- [ ] Let receiver confirm or dispute received payment.
- [ ] Track settlement statuses: pending, payer_marked_paid, receiver_confirmed, disputed, cancelled.

## Phase 7: Notifications

- [ ] Register device push tokens.
- [ ] Store push token per device.
- [ ] Send notification when encrypted group event is available.
- [ ] Send payment confirmation request notifications.
- [ ] Add notification privacy levels: private, balanced, detailed.
- [ ] Default to private notification content.
- [ ] Avoid sending readable expense/payment details in push payloads unless the user explicitly chooses detailed notifications.

## Phase 8: Personal Lending

- [ ] Let users record personal loans to contacts.
- [ ] Support repayment schedule and due dates.
- [ ] Support partial repayments.
- [ ] Support lender-defined credit limit.
- [ ] Let lender mark a loan as defaulted or written off.
- [ ] Keep borrower insights private to the lender.
- [ ] Build a simple borrower score based only on lender-owned history.
- [ ] Avoid presenting this as an official credit score.

## Phase 9: AI-Assisted Insights

- [ ] Generate private repayment insights.
- [ ] Summarize borrowing/lending history.
- [ ] Warn when a new loan exceeds the lender's usual comfort limit.
- [ ] Explain borrower score factors transparently.
- [ ] Keep AI optional and privacy-aware.
- [ ] Avoid regulated lending decisions or public credit scoring.

## Phase 10: Production Readiness

- [ ] Add structured logging.
- [ ] Add API validation and consistent error responses.
- [ ] Add CORS configuration.
- [ ] Write unit tests for balance and split calculations.
- [ ] Write integration tests for sync and auth.
- [ ] Add mobile app test coverage.
- [ ] Add Docker setup for backend.
- [ ] Add CI/CD pipeline.
- [ ] Add backup and restore strategy.
- [ ] Review privacy, security, and regulatory risk before public launch.

## Current Backend Tech Stack

- **API**: FastAPI
- **Database Prototype**: PostgreSQL via Supabase
- **Auth**: JWT using `python-jose`
- **Password Hashing**: bcrypt

## Possible Future Mobile Stack

- **Mobile App**: Expo React Native or Flutter
- **Local Storage**: SQLite
- **Sync**: Encrypted event relay
- **Push Notifications**: Expo Push Notifications initially, FCM/APNs later if needed
- **Payments**: UPI intent/deep link with manual receiver confirmation
