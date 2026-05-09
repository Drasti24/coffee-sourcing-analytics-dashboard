-- ============================================================
-- Coffee Sourcing & Roasting Decision Intelligence Dashboard
-- SQL Server Analysis Script
-- ============================================================

USE CoffeeAnalytics;
GO

-- ============================================================
-- 1. Drop Existing Tables
-- ============================================================

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS coffee_products;
GO

-- ============================================================
-- 2. Create Tables
-- ============================================================

CREATE TABLE coffee_products (
    product_id INT PRIMARY KEY,
    origin VARCHAR(50),
    altitude INT,
    process_method VARCHAR(50),
    roast_level VARCHAR(50),
    temp_min INT,
    temp_max INT,
    quality_score DECIMAL(4,2),
    cost_per_kg DECIMAL(6,2)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    product_id INT,
    order_date DATE,
    quantity INT,
    selling_price DECIMAL(6,2),
    FOREIGN KEY (product_id) REFERENCES coffee_products(product_id)
);

-- ============================================================
-- 3. Insert Coffee Product Data
-- ============================================================

INSERT INTO coffee_products 
(product_id, origin, altitude, process_method, roast_level, temp_min, temp_max, quality_score, cost_per_kg)
VALUES
(1, 'Colombia', 1800, 'Washed', 'Light', 195, 205, 87.50, 8.20),
(2, 'Colombia', 1650, 'Washed', 'Medium', 205, 215, 86.20, 7.80),
(3, 'Ethiopia', 2100, 'Natural', 'Light', 195, 205, 90.10, 9.50),
(4, 'Ethiopia', 2000, 'Washed', 'Medium', 205, 215, 88.70, 9.10),
(5, 'Brazil', 1200, 'Natural', 'Dark', 215, 230, 83.40, 6.20),
(6, 'Brazil', 1150, 'Pulped Natural', 'Medium', 205, 215, 84.60, 6.50),
(7, 'Guatemala', 1700, 'Washed', 'Medium', 205, 215, 86.90, 7.40),
(8, 'Kenya', 1900, 'Washed', 'Light', 195, 205, 89.30, 9.00),
(9, 'Honduras', 1500, 'Washed', 'Dark', 215, 230, 82.80, 6.80),
(10, 'Costa Rica', 1600, 'Honey', 'Medium', 205, 215, 87.10, 8.00);

-- ============================================================
-- 4. Insert Base Order Data
-- ============================================================

INSERT INTO orders
(order_id, product_id, order_date, quantity, selling_price)
VALUES
(101, 1, '2025-01-10', 35, 18.99),
(102, 2, '2025-01-12', 42, 17.99),
(103, 3, '2025-01-15', 28, 21.99),
(104, 5, '2025-01-20', 50, 15.99),
(105, 7, '2025-02-02', 31, 18.49),
(106, 8, '2025-02-08', 26, 20.99),
(107, 4, '2025-02-14', 24, 20.49),
(108, 6, '2025-02-20', 45, 16.49),
(109, 10, '2025-03-01', 38, 18.99),
(110, 3, '2025-03-07', 34, 21.99),
(111, 1, '2025-03-12', 40, 18.99),
(112, 5, '2025-03-18', 58, 15.99),
(113, 8, '2025-04-03', 30, 20.99),
(114, 2, '2025-04-11', 47, 17.99),
(115, 6, '2025-04-16', 52, 16.49),
(116, 9, '2025-04-22', 33, 15.49),
(117, 4, '2025-05-05', 29, 20.49),
(118, 10, '2025-05-12', 41, 18.99),
(119, 7, '2025-05-18', 36, 18.49),
(120, 3, '2025-05-25', 32, 21.99);

-- ============================================================
-- 5. Generate Additional Synthetic Order Data
-- This expands the dataset for dashboard analysis.
-- ============================================================

DECLARE @i INT = 121;

WHILE @i <= 400
BEGIN
    INSERT INTO orders (order_id, product_id, order_date, quantity, selling_price)
    SELECT 
        @i,
        (SELECT TOP 1 product_id FROM coffee_products ORDER BY NEWID()),
        DATEADD(DAY, -ABS(CHECKSUM(NEWID())) % 120, GETDATE()),
        10 + ABS(CHECKSUM(NEWID())) % 50,
        15 + (ABS(CHECKSUM(NEWID())) % 10);

    SET @i = @i + 1;
END;
GO

-- ============================================================
-- 6. Data Validation
-- ============================================================

SELECT COUNT(*) AS total_products
FROM coffee_products;

SELECT COUNT(*) AS total_orders
FROM orders;

-- ============================================================
-- 7. Revenue by Coffee Origin
-- Identifies which origins generate the highest sales revenue.
-- ============================================================

SELECT 
    p.origin,
    SUM(o.quantity * o.selling_price) AS total_revenue
FROM orders o
JOIN coffee_products p 
    ON o.product_id = p.product_id
GROUP BY p.origin
ORDER BY total_revenue DESC;

-- ============================================================
-- 8. Profit by Coffee Origin
-- Compares profitability across coffee origins.
-- ============================================================

SELECT 
    p.origin,
    SUM((o.selling_price - p.cost_per_kg) * o.quantity) AS total_profit
FROM orders o
JOIN coffee_products p 
    ON o.product_id = p.product_id
GROUP BY p.origin
ORDER BY total_profit DESC;

-- ============================================================
-- 9. Demand by Coffee Origin
-- Measures total quantity sold by origin.
-- ============================================================

SELECT 
    p.origin,
    SUM(o.quantity) AS total_quantity_sold
FROM orders o
JOIN coffee_products p 
    ON o.product_id = p.product_id
GROUP BY p.origin
ORDER BY total_quantity_sold DESC;

-- ============================================================
-- 10. Origin Priority Score
-- Combines demand and profit to support sourcing decisions.
-- ============================================================

SELECT 
    p.origin,
    SUM(o.quantity) AS demand,
    SUM((o.selling_price - p.cost_per_kg) * o.quantity) AS profit,
    (
        SUM(o.quantity) * 0.5 
        + SUM((o.selling_price - p.cost_per_kg) * o.quantity) * 0.5
    ) AS priority_score
FROM orders o
JOIN coffee_products p 
    ON o.product_id = p.product_id
GROUP BY p.origin
ORDER BY priority_score DESC;

-- ============================================================
-- 11. Roast-Level Performance
-- Compares demand and profit across roast levels.
-- ============================================================

SELECT 
    p.roast_level,
    SUM(o.quantity) AS demand,
    SUM((o.selling_price - p.cost_per_kg) * o.quantity) AS profit
FROM orders o
JOIN coffee_products p 
    ON o.product_id = p.product_id
GROUP BY p.roast_level
ORDER BY profit DESC;

-- ============================================================
-- 12. Profitability by Origin and Roast Combination
-- Identifies the strongest origin-roast combinations.
-- ============================================================

SELECT 
    p.origin,
    p.roast_level,
    SUM(o.quantity) AS demand,
    SUM((o.selling_price - p.cost_per_kg) * o.quantity) AS profit
FROM orders o
JOIN coffee_products p 
    ON o.product_id = p.product_id
GROUP BY p.origin, p.roast_level
ORDER BY profit DESC;

-- ============================================================
-- 13. Profit Margin by Origin
-- Evaluates profitability efficiency by origin.
-- ============================================================

SELECT 
    p.origin,
    SUM(o.quantity * o.selling_price) AS revenue,
    SUM((o.selling_price - p.cost_per_kg) * o.quantity) AS profit,
    (
        SUM((o.selling_price - p.cost_per_kg) * o.quantity) * 1.0
        / SUM(o.quantity * o.selling_price)
    ) * 100 AS profit_margin_percent
FROM orders o
JOIN coffee_products p 
    ON o.product_id = p.product_id
GROUP BY p.origin
ORDER BY profit_margin_percent DESC;
