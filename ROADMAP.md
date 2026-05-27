# Split-Expenses Roadmap

## Phase 1: Fix Current Code & Structure
- [ ] Fix imports in `main.py` (update to new paths)
- [ ] Fix `core/auth.py` (datetime bug, broken user_db reference)
- [ ] Create `database/connection.py` (shared Supabase client)
- [ ] Create `core/security.py` (move password functions from main.py)
- [ ] Create `services/user_service.py` (move create_user logic)
- [ ] Create `api/endpoints/auth.py` (move auth routes)
- [ ] Clean up `main.py` (only app init + router includes)
- [ ] Test signup and login flow end-to-end

## Phase 2: User Management
- [ ] Add user profile endpoint (GET /users/me)
- [ ] Add update profile endpoint (PUT /users/me)
- [ ] Add search users endpoint (GET /users/search?q=)
- [ ] Add proper error responses and validation

## Phase 3: Groups
- [ ] Create group schema (name, description, created_by, members)
- [ ] Create `groups` table in Supabase
- [ ] Create `group_members` table (user_id, group_id, role)
- [ ] POST /groups — create a group
- [ ] GET /groups — list user's groups
- [ ] GET /groups/{id} — get group details
- [ ] POST /groups/{id}/members — add member
- [ ] DELETE /groups/{id}/members/{user_id} — remove member

## Phase 4: Expenses
- [ ] Create expense schema (amount, description, paid_by, group_id, split_type)
- [ ] Create `expenses` table in Supabase
- [ ] Create `expense_splits` table (expense_id, user_id, amount_owed)
- [ ] POST /groups/{id}/expenses — add expense
- [ ] GET /groups/{id}/expenses — list group expenses
- [ ] Support split types: equal, exact, percentage
- [ ] Calculate balances per group

## Phase 5: Settlements & Balances
- [ ] GET /groups/{id}/balances — who owes whom
- [ ] POST /groups/{id}/settle — record a payment
- [ ] Simplify debts algorithm (minimize transactions)
- [ ] GET /users/me/overall-balance — total across all groups

## Phase 6: Redis Integration (Caching)
- [ ] Set up Redis connection
- [ ] Cache user sessions
- [ ] Cache group balances (invalidate on new expense)
- [ ] Rate limiting on auth endpoints

## Phase 7: MongoDB Integration (Activity Log)
- [ ] Set up MongoDB connection
- [ ] Log all expense activities
- [ ] Log group changes (member added/removed)
- [ ] GET /groups/{id}/activity — activity feed

## Phase 8: Production Readiness
- [ ] Add proper logging
- [ ] Add request validation middleware
- [ ] Add CORS configuration
- [ ] Write unit tests (pytest)
- [ ] Write integration tests
- [ ] Add API documentation (FastAPI auto-docs)
- [ ] Dockerize the application
- [ ] Add CI/CD pipeline

## Tech Stack
- **API**: FastAPI
- **Primary DB**: PostgreSQL (via Supabase)
- **Cache**: Redis
- **Activity Log**: MongoDB
- **Auth**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
