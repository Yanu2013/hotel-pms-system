# Hotel PMS Database Schema

## Overview
This document defines the complete database schema for a Hotel Property Management System using PostgreSQL/MySQL.

---

## Tables Structure

### 1. **Users Table** (Staff/Admin)
```sql
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    role ENUM('admin', 'manager', 'receptionist', 'housekeeping', 'accountant') NOT NULL,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role (role)
);
```

### 2. **Properties Table** (Hotel/Branch)
```sql
CREATE TABLE properties (
    property_id INT PRIMARY KEY AUTO_INCREMENT,
    property_name VARCHAR(150) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20),
    country VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    total_rooms INT NOT NULL,
    manager_id INT,
    currency VARCHAR(3) DEFAULT 'USD',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(user_id),
    INDEX idx_city (city),
    INDEX idx_status (status)
);
```

### 3. **Room Types Table**
```sql
CREATE TABLE room_types (
    room_type_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT NOT NULL,
    type_name VARCHAR(100) NOT NULL,
    description TEXT,
    base_price DECIMAL(10, 2) NOT NULL,
    capacity INT NOT NULL,
    amenities JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    INDEX idx_property (property_id),
    UNIQUE KEY unique_type_per_property (property_id, type_name)
);
```

### 4. **Rooms Table**
```sql
CREATE TABLE rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT NOT NULL,
    room_type_id INT NOT NULL,
    room_number VARCHAR(50) NOT NULL,
    floor INT,
    status ENUM('available', 'occupied', 'cleaning', 'maintenance', 'blocked') DEFAULT 'available',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id),
    UNIQUE KEY unique_room_per_property (property_id, room_number),
    INDEX idx_status (status),
    INDEX idx_property (property_id)
);
```

### 5. **Guests Table**
```sql
CREATE TABLE guests (
    guest_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    id_type ENUM('passport', 'license', 'national_id') NOT NULL,
    id_number VARCHAR(50) NOT NULL,
    country VARCHAR(50),
    address VARCHAR(255),
    city VARCHAR(50),
    zip_code VARCHAR(20),
    guest_type ENUM('individual', 'corporate') DEFAULT 'individual',
    loyalty_points INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_phone (phone),
    INDEX idx_id_number (id_number)
);
```

### 6. **Reservations Table**
```sql
CREATE TABLE reservations (
    reservation_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT NOT NULL,
    guest_id INT NOT NULL,
    room_id INT,
    room_type_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    number_of_guests INT NOT NULL,
    number_of_nights INT GENERATED ALWAYS AS (DATEDIFF(check_out_date, check_in_date)) STORED,
    total_amount DECIMAL(12, 2) NOT NULL,
    advance_payment DECIMAL(12, 2) DEFAULT 0,
    status ENUM('pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled') DEFAULT 'pending',
    booking_source ENUM('direct', 'booking.com', 'airbnb', 'expedia', 'other') DEFAULT 'direct',
    notes TEXT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),
    INDEX idx_status (status),
    INDEX idx_check_in (check_in_date),
    INDEX idx_guest (guest_id),
    INDEX idx_property (property_id)
);
```

### 7. **Payments Table**
```sql
CREATE TABLE payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(12, 2) NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'debit_card', 'bank_transfer', 'digital_wallet') NOT NULL,
    transaction_id VARCHAR(100),
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    notes TEXT,
    processed_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id),
    FOREIGN KEY (processed_by) REFERENCES users(user_id),
    INDEX idx_reservation (reservation_id),
    INDEX idx_status (payment_status),
    INDEX idx_date (payment_date)
);
```

### 8. **Invoices Table**
```sql
CREATE TABLE invoices (
    invoice_id INT PRIMARY KEY AUTO_INCREMENT,
    reservation_id INT NOT NULL,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    issue_date DATE NOT NULL,
    due_date DATE,
    subtotal DECIMAL(12, 2) NOT NULL,
    tax DECIMAL(12, 2) DEFAULT 0,
    discount DECIMAL(12, 2) DEFAULT 0,
    total_amount DECIMAL(12, 2) NOT NULL,
    status ENUM('draft', 'issued', 'paid', 'overdue', 'cancelled') DEFAULT 'draft',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reservation_id) REFERENCES reservations(reservation_id),
    INDEX idx_status (status),
    INDEX idx_date (issue_date)
);
```

### 9. **Housekeeping Tasks Table**
```sql
CREATE TABLE housekeeping_tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT NOT NULL,
    room_id INT NOT NULL,
    task_type ENUM('cleaning', 'maintenance', 'inspection', 'linen_change') NOT NULL,
    assigned_to INT,
    status ENUM('pending', 'in_progress', 'completed', 'cancelled') DEFAULT 'pending',
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    scheduled_date DATE NOT NULL,
    completion_date DATETIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    FOREIGN KEY (room_id) REFERENCES rooms(room_id),
    FOREIGN KEY (assigned_to) REFERENCES users(user_id),
    INDEX idx_status (status),
    INDEX idx_room (room_id),
    INDEX idx_date (scheduled_date)
);
```

### 10. **Room Rates Table** (Dynamic Pricing)
```sql
CREATE TABLE room_rates (
    rate_id INT PRIMARY KEY AUTO_INCREMENT,
    room_type_id INT NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    rate_price DECIMAL(10, 2) NOT NULL,
    rate_type ENUM('standard', 'weekend', 'holiday', 'promotion') DEFAULT 'standard',
    min_stay INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id),
    INDEX idx_room_type (room_type_id),
    INDEX idx_dates (check_in_date, check_out_date)
);
```

### 11. **Guest Preferences Table**
```sql
CREATE TABLE guest_preferences (
    preference_id INT PRIMARY KEY AUTO_INCREMENT,
    guest_id INT NOT NULL,
    room_preference VARCHAR(100),
    bed_type ENUM('single', 'double', 'queen', 'king') DEFAULT 'double',
    floor_preference INT,
    smoking BOOLEAN DEFAULT FALSE,
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
    INDEX idx_guest (guest_id)
);
```

### 12. **Expenses Table**
```sql
CREATE TABLE expenses (
    expense_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT NOT NULL,
    expense_category VARCHAR(100) NOT NULL,
    description TEXT,
    amount DECIMAL(12, 2) NOT NULL,
    expense_date DATE NOT NULL,
    payment_method ENUM('cash', 'credit_card', 'bank_transfer', 'check') NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    approved_by INT,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(property_id),
    FOREIGN KEY (approved_by) REFERENCES users(user_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),
    INDEX idx_property (property_id),
    INDEX idx_date (expense_date),
    INDEX idx_status (status)
);
```

### 13. **Audit Log Table**
```sql
CREATE TABLE audit_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT,
    old_value JSON,
    new_value JSON,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    INDEX idx_user (user_id),
    INDEX idx_created_at (created_at),
    INDEX idx_entity (entity_type, entity_id)
);
```

---

## Key Relationships Diagram

```
Properties (1) ──→ (Many) Rooms
                ├─→ (Many) Room_Types
                ├─→ (Many) Reservations
                ├─→ (Many) Housekeeping_Tasks
                └─→ (Many) Expenses

Guests (1) ──→ (Many) Reservations
           ├─→ (Many) Guest_Preferences
           └─→ (One) Loyalty_Points

Reservations (1) ──→ (Many) Payments
               ├─→ (Many) Invoices
               └─→ (One) Room

Room_Types (1) ──→ (Many) Rooms
            ├─→ (Many) Room_Rates
            └─→ (Many) Reservations

Users (1) ──→ (Many) Housekeeping_Tasks
         ├─→ (Many) Payments
         ├─→ (Many) Audit_Logs
         └─→ (Many) Expenses
```

---

## Indexes for Performance

- **Primary Keys**: Automatically indexed
- **Foreign Keys**: Indexed for fast joins
- **Frequently Searched**: status, dates, email, phone
- **Composite Indexes**: For complex queries (room_id + date, property_id + status)

---

## Notes

1. Use **TIMESTAMP** for audit trails
2. Use **ENUM** for fixed values to save space
3. Use **JSON** for flexible data (amenities, preferences)
4. Add **INDEXES** for frequently searched columns
5. Implement **soft deletes** if needed (add `deleted_at` column)
6. Use **transactions** for multi-step operations (booking + payment)
7. Implement **triggers** for automatic timestamps and calculations

---

## Next Steps

1. Create SQL initialization script
2. Set up database connections
3. Create ORM models (Sequelize, SQLAlchemy, etc.)
4. Implement API endpoints
5. Add authentication & authorization layer
