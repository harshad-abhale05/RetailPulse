# RetailPulse - Data Quality Findings

## 1. Primary Key Validation

- Customers: customer_id is unique.
- Orders: order_id is unique.
- Products: product_id is unique.
- Sellers: seller_id is unique.
- Order Items: (order_id, order_item_id) is unique.
- Payments: (order_id, payment_sequential) is unique.
- Reviews: (review_id, order_id) is unique.
- Reviews: review_id alone is not unique.
- Geolocation: ZIP prefixes are repeated; no unique primary key identified.

## 2. Foreign Key Validation

The following relationships passed validation with zero orphan records:

- Orders -> Customers
- Order Items -> Orders
- Order Items -> Products
- Order Items -> Sellers
- Payments -> Orders
- Reviews -> Orders

## 3. Category Translation Exception

- Products checked: 32,341
- Orphan category records: 13
- Unique orphan categories: 2

Categories:
- pc_gamer: 3 products
- portateis_cozinha_e_preparadores_de_alimentos: 10 products

Handling strategy:
- Preserve all original product records.
- Use LEFT JOIN for category translation.
- Fall back to the original category name when translation is unavailable.
- Never delete source records because of missing translations.

## 4. Source Data Preservation

Original Olist CSV files remain unchanged.
Data cleaning and transformations will be performed in the Silver layer.

## 5. Geolocation Coverage Validation

Customer records:
- Records checked: 99,441
- Unmatched unique ZIP prefixes: 157

Seller records:
- Records checked: 3,095
- Unmatched unique ZIP prefixes: 7

Important:
- These figures represent unique unmatched ZIP prefixes,
  not the number of affected customer or seller records.
- Missing geolocation matches will not cause records to be deleted.
- Use LEFT JOIN when enriching customer and seller data.
- Unmatched geographic coordinates will remain NULL.
- Investigate formatting and source coverage before classifying
  unmatched prefixes as genuine data errors.


## 6. Canceled Orders With Delivery Timestamps

### Finding

During Gold-layer delivery analysis, 6 orders
were found with:

- order_status = canceled
- order_delivered_customer_date IS NOT NULL

### Investigation

All six records were inspected individually.
They contain both purchase and delivery timestamps.

### Decision

- Preserve all six records.
- Do not modify the original order status.
- Flag these records as data-quality exceptions.
- Exclude canceled orders from delivered-order KPIs.
- Investigate the source-system status history if available.

### Impact

The records demonstrate why business status and
timestamp validation are both necessary.