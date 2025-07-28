# 🛡️ QuickFood - Role-Based Access Control (RBAC)

A clear breakdown of permissions and responsibilities for each role in the QuickFood platform.

---

## 🔐 Permission Symbols

| Symbol | Meaning                  |
|--------|--------------------------|
| ✅     | Full Access              |
| ⚠️     | Limited Access           |
| ❌     | No Access                |
| 🔍     | Read-Only                |

---

## 🏢 System-Level Roles

### 👑 Super Admin
| Resource       | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Restaurant     | ✅     | ✅   | ✅     | ✅     | Platform configuration, Force majeure actions |
| Branch         | ✅     | ✅   | ✅     | ✅     | Geographic expansion management |
| User Profile   | ✅     | ✅   | ✅     | ✅     | Role assignment, Security audits |
| Menu           | ✅     | ✅   | ✅     | ✅     | Global menu standardization |
| Food Items     | ✅     | ✅   | ✅     | ✅     | Ingredient-level analytics |
| Orders         | ✅     | ✅   | ✅     | ✅     | Financial reporting, Dispute resolution |
| Ratings        | ❌     | ✅   | ✅     | ✅     | Review moderation, Sentiment analysis |

**🔧 Capabilities**:
- Full platform control and configuration
- Emergency override operations
- Audit trail access & billing management
- API key and user role management

---

### 🛠️ System Staff
| Resource       | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Restaurant     | ⚠️     | ✅   | ⚠️     | ❌     | Onboarding support |
| Branch         | ⚠️     | ✅   | ⚠️     | ❌     | Branch verification |
| User Profile   | ❌     | 🔍   | ⚠️     | ❌     | Support ticket resolution |
| Orders         | ⚠️     | ✅   | ⚠️     | ❌     | Customer support |

**🧭 Boundaries**:
- Action approvals required for modifications
- No access to financial or business-sensitive data

---

## 🍴 Restaurant-Level Roles

### 🧑‍💼 Restaurant Owner
| Resource       | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Restaurant     | ❌     | 🔍   | ✅     | ❌     | Branding management |
| Branch         | ✅     | ✅   | ✅     | ✅     | Expansion & operation control |
| Menu           | ✅     | ✅   | ✅     | ✅     | Menu lifecycle management |
| Food Items     | ✅     | ✅   | ✅     | ✅     | Price & availability control |
| Orders         | ❌     | ✅   | ⚠️     | ❌     | View analytics, sales data |

**📊 Capabilities**:
- Business dashboard & insights
- Staff and performance management
- Menu scheduling & marketing campaigns

---

### 🧑‍🏫 Branch Manager
| Resource       | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Branch         | ❌     | 🔍   | ⚠️     | ❌     | Operational reports |
| Menu           | ✅     | ✅   | ✅     | ✅     | Daily specials management |
| Food Items     | ✅     | ✅   | ⚠️     | ⚠️     | Stock level control |
| Orders         | ❌     | ✅   | ✅     | ❌     | Kitchen order flow |

**📋 Responsibilities**:
- Staff shift & supplier coordination
- Service quality assurance
- Local reporting

---

### 👨‍🍳 Restaurant Staff
| Resource       | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Food Items     | ❌     | 🔍   | ⚠️     | ❌     | Toggle availability |
| Orders         | ❌     | 🔍   | ⚠️     | ❌     | Update order status |

**🔧 Duties**:
- Handle kitchen workflow
- Basic POS tasks
- Shift-wise task management

---

## 👥 Platform Users

### 🧑‍🍽️ Customer
| Resource       | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Address        | ✅     | ✅   | ✅     | ✅     | Location-based service |
| Orders         | ✅     | ✅   | ⚠️     | ❌     | Reorder, track history |
| Ratings        | ✅     | ✅   | ✅     | ✅     | Verified reviews only |

**🎯 Features**:
- Personalized recommendations & offers
- Reward points and loyalty system
- Multiple payment methods

---

### 🛵 Delivery Partner
| Resource       | Create | Read | Update | Delete | Special Privileges |
|----------------|--------|------|--------|--------|--------------------|
| Orders         | ❌     | ⚠️   | ✅     | ❌     | Live tracking updates |

**🚚 Tools**:
- Route optimization & delivery status
- Proof of delivery and logs
- Partner earnings dashboard

---

## 📝 Implementation Notes

- 🔄 **Role Hierarchy**: Super Admin > System Staff > Owner > Manager > Staff
- 🔐 **Security Controls**:
  - Audit logs for delete actions
  - Approval chains for financial changes
- 🌐 **API Access**:
  - Role-scoped endpoints
  - Throttling policies per role