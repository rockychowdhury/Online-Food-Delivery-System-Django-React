# QuickFood - Role-Based Access Control (RBAC) Matrix

## Permission Legend
| Symbol | Meaning                  |
|--------|--------------------------|
| ✅     | Full permission          |
| ⚠️     | Partial/limited permission |
| ❌     | No permission            |
| 🔍     | Read-only access         |

---

## System-Level Roles

### 1. Super Admin
| Model          | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Restaurant     | ✅     | ✅   | ✅     | ✅     | Platform configuration, Force majeure actions |
| Branches       | ✅     | ✅   | ✅     | ✅     | Geographic expansion management |
| UserProfile    | ✅     | ✅   | ✅     | ✅     | Role assignment, Security audits |
| Menu           | ✅     | ✅   | ✅     | ✅     | Global menu standardization |
| FoodItems      | ✅     | ✅   | ✅     | ✅     | Ingredient-level analytics |
| Orders         | ✅     | ✅   | ✅     | ✅     | Financial reporting, Dispute resolution |
| Ratings        | ❌     | ✅   | ✅     | ✅     | Review moderation, Sentiment analysis |

**System Capabilities**:
- Full platform configuration
- Emergency override capabilities
- Audit trail access
- API key management
- Billing system administration

---

### 2. System Staff
| Model          | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Restaurant     | ⚠️     | ✅   | ⚠️     | ❌     | Onboarding support |
| Branches       | ⚠️     | ✅   | ⚠️     | ❌     | Branch verification |
| UserProfile    | ❌     | 🔍   | ⚠️     | ❌     | Support ticket resolution |
| Orders         | ⚠️     | ✅   | ⚠️     | ❌     | Customer support |

**Operational Boundaries**:
- All modifications require approval workflow
- Limited to assigned support queues
- No financial data access
- Restricted to business hours operations

---

## Restaurant-Level Roles

### 3. Restaurant Owner
| Model          | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Restaurant     | ❌     | 🔍   | ✅     | ❌     | Branding management |
| Branches       | ✅     | ✅   | ✅     | ✅     | Expansion management |
| Menu           | ✅     | ✅   | ✅     | ✅     | Seasonal menu planning |
| FoodItems      | ✅     | ✅   | ✅     | ✅     | Pricing strategy |
| Orders         | ❌     | ✅   | ⚠️     | ❌     | Business analytics |

**Business Controls**:
- Staff management console
- Financial performance dashboards
- Inventory integration
- Marketing campaign tools

---

### 4. Branch Manager
| Model          | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Branches       | ❌     | 🔍   | ⚠️     | ❌     | Operational reports |
| Menu           | ✅     | ✅   | ✅     | ✅     | Daily specials |
| FoodItems      | ✅     | ✅   | ⚠️     | ⚠️     | Stock management |
| Orders         | ❌     | ✅   | ✅     | ❌     | Kitchen workflow |

**Branch Authority**:
- Staff scheduling
- Local supplier management
- Quality control checks
- Customer complaint resolution

---

### 5. Restaurant Staff
| Model          | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| FoodItems      | ❌     | 🔍   | ⚠️     | ❌     | Availability toggle |
| Orders         | ❌     | 🔍   | ⚠️     | ❌     | Status updates |

**Workflow Access**:
- Order preparation console
- POS system integration
- Shift management
- Basic customer lookup

---

## Platform Roles

### 6. Customer
| Model          | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Address        | ✅     | ✅   | ✅     | ✅     | Geocoding |
| Orders         | ✅     | ✅   | ⚠️     | ❌     | Reorder function |
| Ratings        | ✅     | ✅   | ✅     | ✅     | Verified purchases |

**User Features**:
- Personalized recommendations
- Loyalty program
- Multi-payment options
- Dietary preference settings

---

### 7. Delivery Partner
| Model          | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Orders         | ❌     | ⚠️   | ✅     | ❌     | Live GPS tracking |

**Delivery Tools**:
- Route optimization
- Earnings dashboard
- Vehicle management
- Delivery proof system

---

## Permission Implementation Notes

1. **Hierarchy Enforcement**:
   - Role inheritance follows: Super Admin > System Staff > Restaurant Owner > Branch Manager > Staff
   - Customer and Delivery roles operate on separate permission planes

2. **Context-Sensitive Restrictions**:
   - Time-based restrictions for order modifications
   - Geographic limitations for branch managers
   - Verification requirements for sensitive operations

3. **Audit Requirements**:
   - All delete operations require audit logging
   - Financial modifications need dual approval
   - Role changes trigger verification workflows

4. **API Access Levels**:
   - System roles: Full API access with rate limits
   - Business roles: Restricted to relevant endpoints
   - Customer roles: Read-only for most endpoints
