# 🛍️ E-Commerce Product Catalog Backend

## 📌 Overview
This backend system powers a product catalog for an e-commerce platform. It manages products, categories, sellers, users, shopping carts, and orders. The project emphasizes scalability, security, and clean API design.

---

## 🎯 Goals
- CRUD operations for users, products, categories, carts, and orders.
- Filtering, searching, sorting, and pagination for efficient product discovery.
- Secure authentication using JWT.
- Scalable PostgreSQL schema with indexing.
- API documentation with Swagger/OpenAPI.

---

## 🛠️ Technologies Used
- **Django** + **Django REST Framework**
- **PostgreSQL**
- **JWT Authentication** (`djangorestframework-simplejwt`)
- **Swagger / OpenAPI Docs** (`drf-yasg`)

---

## ✨ Key Features

### 📦 Product Catalog
- Products linked to categories and sellers.
- CRUD support for admin or seller users.

### 🔐 User Authentication
- Secure registration and JWT-based login.
- Role support (customer/seller/admin).

### 🔎 Product Discovery
- Filter by category and seller.
- Search by product name or description.
- Sort by price (ascending or descending).
- Pagination for large datasets.

### 🛒 Shopping Cart (Shopping List)
- Each user has a cart (`ShoppingList`) with multiple `CartItems`.
- Add, update, or remove items.
- Convert to an order during checkout.

### 📄 Orders
- Orders include multiple products and quantities.
- Maintain purchase history per user.
- Status field for order processing.

### 📚 API Documentation
- Swagger UI at `/swagger/`
- Optional Postman collection for testing

---

## 🧱 Database Design

### Tables:
- `users` – registered users
- `sellers` – optional vendor role tied to user
- `categories` – product classification
- `products` – catalog items
- `shopping_lists` – user carts
- `cart_items` – cart contents
- `orders` – placed orders
- `order_items` – line items in an order

---

## 🔌 API Endpoints

### 🔐 Authentication
| Method | Endpoint         | Description            |
|--------|------------------|------------------------|
| POST   | `/auth/register/`| Register new user      |
| POST   | `/auth/login/`   | Obtain JWT token       |

---

### 📦 Products & Categories
| Method | Endpoint                | Description                     |
|--------|-------------------------|---------------------------------|
| GET    | `/products/`            | List + filter + sort + paginate|
| POST   | `/products/`            | Create product (admin/seller)  |
| GET    | `/products/<id>/`       | View product                   |
| PUT    | `/products/<id>/`       | Update product                 |
| DELETE | `/products/<id>/`       | Delete product                 |
| GET    | `/categories/`          | List categories                |
| POST   | `/categories/`          | Create category                |

---

### 🛒 Shopping Cart
| Method | Endpoint                        | Description               |
|--------|----------------------------------|---------------------------|
| GET    | `/cart/`                        | View current cart         |
| POST   | `/cart/items/`                  | Add product to cart       |
| PUT    | `/cart/items/<id>/`             | Update item quantity      |
| DELETE | `/cart/items/<id>/`             | Remove item from cart     |
| POST   | `/cart/checkout/`               | Place order from cart     |

---

### 📄 Orders
| Method | Endpoint             | Description           |
|--------|----------------------|-----------------------|
| GET    | `/orders/`           | List user's orders    |
| GET    | `/orders/<id>/`      | View specific order   |

---

## 📈 Performance
- Indexes on: `product.price`, `product.category_id`, `product.seller_id`
- Query optimization with `select_related`, `prefetch_related`
- Pagination to reduce load and improve UX

---

## 🧪 API Documentation
- Hosted at `/swagger/`
- Fully interactive
- Includes request/response examples
- Postman collection exportable

---

## 📂 Git Commit Workflow
- Use semantic prefixes: `feat:`, `fix:`, `refactor:`, `docs:`
- Write focused, descriptive commits
- Follow structured branching (feature → main)

---

