# Run Examples

Example:

Query: "Give me Orders over amount 100"


Response:

```
{
    'orderId': 'ORD001',
    'productId': 'PROD1001',
    'customerId': 'CUST5001',
    'orderDate': '2025-03-25 10:15:00',
    'orderStatus': 'Shipped',
    'orderAmount': 199.99
}
{
    'orderId': 'ORD003',
    'productId': 'PROD1003',
    'customerId': 'CUST5003',
    'orderDate': '2025-03-27 15:45:00',
    'orderStatus': 'Delivered',
    'orderAmount': 349.75
}
{
    'orderId': 'ORD004',
    'productId': 'PROD1004',
    'customerId': 'CUST5004',
    'orderDate': '2025-03-28 08:20:00',
    'orderStatus': 'Cancelled',
    'orderAmount': 125.0
}
{
    'orderId': 'ORD005',
    'productId': 'PROD1005',
    'customerId': 'CUST5005',
    'orderDate': '2025-03-29 17:10:00',
    'orderStatus': 'Processing',
    'orderAmount': 220.3
}
{
    'orderId': 'ORD006',
    'productId': 'PROD1006',
    'customerId': 'CUST5006',
    'orderDate': '2025-03-30 14:55:00',
    'orderStatus': 'Shipped',
    'orderAmount': 499.99
}
{
    'orderId': 'ORD008',
    'productId': 'PROD1008',
    'customerId': 'CUST5008',
    'orderDate': '2025-04-01 09:05:00',
    'orderStatus': 'Pending',
    'orderAmount': 159.49
}
{
    'orderId': 'ORD009',
    'productId': 'PROD1009',
    'customerId': 'CUST5009',
    'orderDate': '2025-04-02 16:25:00',
    'orderStatus': 'Shipped',
    'orderAmount': 275.0
}
{
    'orderId': 'ORD010',
    'productId': 'PROD1010',
    'customerId': 'CUST5010',
    'orderDate': '2025-04-03 13:35:00',
    'orderStatus': 'Delivered',
    'orderAmount': 329.99
}
```


Query: "give me top three order by amount and their customer info"

```
{
    'orderId': 'ORD006',
    'productId': 'PROD1006',
    'customer': {
        'customerId': 'CUST5006',
        'customerName': 'John Doe',
        'customerEmail': 'john@example.com',
        'customerPhone': '123-456-7890'
    },
    'orderDate': '2025-03-30 14:55:00',
    'orderStatus': 'Shipped',
    'orderAmount': 499.99
}
{
    'orderId': 'ORD003',
    'productId': 'PROD1003',
    'customer': {
        'customerId': 'CUST5003',
        'customerName': 'Jane Smith',
        'customerEmail': 'jane@example.com',
        'customerPhone': '987-654-3210'
    },
    'orderDate': '2025-03-27 15:45:00',
    'orderStatus': 'Delivered',
    'orderAmount': 349.75
}
{
    'orderId': 'ORD010',
    'productId': 'PROD1010',
    'customer': {
        'customerId': 'CUST5010',
        'customerName': 'Alice Johnson',
        'customerEmail': 'alice@example.com',
        'customerPhone': '555-678-1234'
    },
    'orderDate': '2025-04-03 13:35:00',
    'orderStatus': 'Delivered',
    'orderAmount': 329.99
}
```
