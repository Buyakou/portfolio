SELECT users.id, users.name, orders.order_id
FROM users
JOIN orders ON users.id = orders.user_id;
