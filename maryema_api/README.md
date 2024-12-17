# Maryema API Documentation (The backend)

## API Endpoints

### User Endpoints

#### Roadmap

- **Product endpoints**

  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/products`
  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/products/<uuid>`

- **Feedback endpoints**

  - [x] <span style="border-radius: 2px; background-color: #faaf; color: white;">POST</span> `/api/v1/products/<uuid>/feedbacks`
  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/products/<uuid>/feedbacks`
  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/products/<uuid>/feedbacks/<uuid>`
  - [x] <span style="border-radius: 2px; background-color: #addd; color: white;">PUT</span> `/api/v1/products/<uuid>/feedbacks/<uuid>`

- **Authentication endpoints**

  - [ ] <span style="border-radius: 2px; background-color: #faaf; color: white;">POST</span> `/api/v1/auth/register`
  - [ ] <span style="border-radius: 2px; background-color: #faaf; color: white;">POST</span> `/api/v1/auth/login`
  - [ ] <span style="border-radius: 2px; background-color: #faaf; color: white;">POST</span> `/api/v1/auth/logout`
  - [ ] <span style="border-radius: 2px; background-color: #faaf; color: white;">POST</span> `/api/v1/auth/refresh`
  - [ ] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/auth/me`
  - [ ] <span style="border-radius: 2px; background-color: #addd; color: white;">PUT</span> `/api/v1/auth/me`
  - [ ] <span style="border-radius: 2px; background-color: #addd; color: white;">PUT</span> `/api/v1/auth/me/password`

- **Cart endpoints**

  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/cart`
  - [x] <span style="border-radius: 2px; background-color: #faaf; color: white;">POST</span> `/api/v1/cart`
  - [x] <span style="border-radius: 2px; background-color: #addd; color: white;">PUT</span> `/api/v1/cart`
  - [x] <span style="border-radius: 2px; background-color: red; color: white;">DELETE</span> `/api/v1/cart`
  - [x] <span style="border-radius: 2px; background-color: #faaf; color: white;">POST</span> `/api/v1/cart/checkout`

- **Orders endpoints**
  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/orders`
  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/orders/\<uuid>`
  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/orders/<uuid>/cancel`
  - [x] <span style="border-radius: 2px; background-color: green; color: white;">GET</span> `/api/v1/orders/<uuid>/return`

#### GET /api/v1/products

- Description: List all products for the user
- Request: `GET /api/products`
  - Body: empty
  - Query: `page=<int>&division=<uuid>&category=<uuid>&color=<uuid>&size=<uuid>&min_price=<float>&max_price=<float>&search=<string>`
- Response: 200
- Response body: list of products

```json
{
  "count": 34,
  "next": "http://maryema.ae/api/products-list/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "created_at": "2021-01-01T00:00:00Z",
      "name": "Product 1",
      "category": {
        "id": 1,
        "name": "Category 1"
      },
      "display_price": 100,
      "display_image": "product1.jpg",
      "description": "Product 1 description",
      "average_rating": 4.5
    }
  ]
}
```

### GET /api/products/<uuid>

- Description: Get a product by id
- Request: `GET /api/products/<uuid>`
  - Body: empty
  - Params: `uuid` - product id
  - Query: empty
- Response: 200
- Response body: product

```json
{
  "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
  "created_at": "2021-01-01T00:00:00Z",
  "name": "Product 1",
  "category": {
    "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
    "name": "Category 1"
  },
  "description": "Product 1 description",
  "average_rating": 4.5,
  "colors": [
    {
      "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
      "color1_name": "Red",
      "color1_value": "#FF0000",
      "color2_name": "Blue",
      "color2_value": "#0000FF",
      "image": "product1.jpg",
      "stocks": [
        {
          "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
          "size": {
            "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
            "name": "S"
          },
          "quantity": 10,
          "price": 100
        },
        {
          "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
          "size": {
            "id": 2,
            "name": "M"
          },
          "quantity": 10,
          "price": 100
        }
      ]
    }
  ],
  "feedbacks": [
    {
      "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
      "created_at": "2021-01-01T00:00:00Z",
      "customer": {
        "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
        "username": "user1",
        "avatar": "user1.jpg"
      },
      "rating": 4.5,
      "comment": "Product 1 feedback"
    },
    {
      "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
      "created_at": "2021-01-01T00:00:00Z",
      "customer": {
        "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
        "username": "user2",
        "avatar": "user2.jpg"
      },
      "rating": 4.5,
      "comment": "Product 1 feedback"
    }
  ]
}
```

### POST /api/products/<uuid>/feedbacks

- Description: Create a feedback for a product
- Request: `POST /api/products/<uuid>/feedbacks`
  - Body:
    - `rating` (float): rating of the product
    - `comment` (string): comment of the product
- Response: 201
- Response body: feedback

```json
{
  "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
  "created_at": "2021-01-01T00:00:00Z",
  "customer": {
    "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
    "username": "user1",
    "avatar": "user1.jpg"
  },
  "rating": 4.5,
  "comment": "Product 1 feedback"
}
```

### GET /api/products/<uuid>/feedbacks

- Description: List all feedbacks for a product
- Request: `GET /api/products/<uuid>/feedbacks`
  - Body: empty
  - Params: `uuid` - product id
  - Query: empty
- Response: 200
- Response body: list of feedbacks

```json
[
  {
    "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
    "created_at": "2021-01-01T00:00:00Z",
    "customer": {
      "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
      "username": "user1",
      "avatar": "user1.jpg"
    },
    "rating": 4.5,
    "comment": "Product 1 feedback"
  }
]
```

### POST /api/auth/register

- Description: Register a new user
- Request: `POST /api/auth/register`
  - Body:
    - `username` (string): username of the user
    - `email` (string): email of the user
    - `password` (string): password of the user
    - `first_name` (string): first name of the user
    - `last_name` (string): last name of the user
    - `avatar` (string): avatar of the user
    - `phone_number` (string): phone of the user
- Response: 201
- Response body: user

```json
{
  "detail": "User created successfully"
}
```

### POST /api/auth/login

- Description: Login a user
- Request: `POST /api/auth/login`
  - Body:
    - `username` (string): username of the user
    - `password` (string): password of the user
- Response: 200
- Response Headers:
  - `Set-Cookie: access_token=<string>; HttpOnly; Secure; SameSite=None; Max-Age=<int>`
  - `Set-Cookie: refresh_token=<string>; HttpOnly; Secure; SameSite=None; Max-Age=<int>`
- Response body: user

```json
{
  "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
  "username": "user1",
  "email": "[email protected]",
  "first_name": "User",
  "last_name": "One",
  "avatar": "user1.jpg",
  "phone_number": "1234567890"
}
```

### POST /api/auth/logout

- Description: Logout a user
- Request: `POST /api/auth/logout`
  - Body: empty
- Response: 200
- Response Headers:
  - `Set-Cookie: access_token=; HttpOnly; Secure; SameSite=None; Max-Age=0`
  - `Set-Cookie: refresh_token=; HttpOnly; Secure; SameSite=None; Max-Age=0`
- Response body: empty

```json
{}
```

### POST /api/auth/refresh

- Description: Refresh a user token
- Request: `POST /api/auth/refresh`
  - Body: empty
  - Cookies:
    - `refresh_token` (string): refresh token
- Response: 200
- Response Headers:
  - `Set-Cookie: access_token=<string>; HttpOnly; Secure; SameSite=None; Max-Age=<int>`
- Response body: empty

```json
{}
```

### GET /api/auth/me

- Description: Get the current user
- Request: `GET /api/auth/me`
  - Body: empty
  - Cookies:
    - `access_token` (string): access token
    - `refresh_token` (string): refresh token
- Response: 200
- Response body: user

```json
{
  "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
  "username": "user1",
  "email": "[email protected]",
  "first_name": "User",
  "last_name": "One",
  "avatar": "user1.jpg",
  "phone_number": "1234567890"
}
```

### PATCH /api/auth/me

- Description: Update the current user
- Request: `PATCH /api/auth/me`
  - Body:
    - `username` (string): username of the user
    - `email` (string): email of the user
    - `first_name` (string): first name of the user
    - `last_name` (string): last name of the user
    - `avatar` (string): avatar of the user
    - `phone_number` (string): phone of the user
  - Cookies:
    - `access_token` (string): access token
    - `refresh_token` (string): refresh token
- Response: 200
- Response body: user

```json
{
  "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
  "username": "user1",
  "email": "[email protected]",
  "first_name": "User",
  "last_name": "One",
  "avatar": "user1.jpg",
  "phone_number": "1234567890"
}
```

### PATCH /api/auth/me/password

- Description: Update the current user password
- Request: `PATCH /api/auth/me/password`
  - Body:
    - `old_password` (string): old password of the user
    - `new_password` (string): new password of the user
  - Cookies:
    - `access_token` (string): access token
    - `refresh_token` (string): refresh token
- Response: 200
- Response body: empty

```json
{}
```

### GET /api/cart

- Description: Get the current user active cart
- Request: `GET /api/cart`
  - Body: empty
  - Cookies:
    - `access_token` (string): access token
    - `refresh_token` (string): refresh token
- Response: 200
- Response body: cart

```json
{
  "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
  "created_at": "2021-01-01T00:00:00Z",
  "products": [
    {
      "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
      "name": "Product 1",
      "color": {
        "color1_name": "Red",
        "color1_value": "#FF0000",
        "color2_name": "Blue",
        "color2_value": "#0000FF",
        "image": "product1.jpg"
      },
      "size": {
        "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
        "name": "S"
      },
      "quantity": 1,
      "price": 100
    }
  ],
  "total_price": 100
}
```

### POST /api/cart

- Description: Add a product to the current user active cart
- Request: `POST /api/cart`
  - Body:
    - `product_id` (uuid): product id
    - `quantity` (int): quantity of the product
  - Cookies:
    - `access_token` (string): access token
    - `refresh_token` (string): refresh token
- Response: 201
- Response body: message

```json
{
  "detail": "Product added to cart successfully"
}
```

### PATCH /api/cart

- Description: Update a product in the current user active cart
- Request: `PATCH /api/cart`
  - Body:
    - `product_id` (uuid): product id
    - `quantity` (int): quantity of the product
  - Cookies:
    - `access_token` (string): access token
    - `refresh_token` (string): refresh token
- Response: 200
- Response body: cart

```json
{
  "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
  "created_at": "2021-01-01T00:00:00Z",
  "products": [
    {
      "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
      "name": "Product 1",
      "color": {
        "color1_name": "Red",
        "color1_value": "#FF0000",
        "color2_name": "Blue",
        "color2_value": "#0000FF",
        "image": "product1.jpg"
      },
      "size": {
        "id": "9a8fe99b-4e42-4f96-bcc5-f0cbb0e30c9f",
        "name": "S"
      },
      "quantity": 2,
      "price": 100
    }
  ],
  "total_price": 200
}
```

### DELETE /api/cart

- Description: Delete a product from the current user active cart
- Request: `DELETE /api/cart`
  - Body:
    - `product_id` (uuid): product id
  - Cookies:
    - `access_token` (string): access token
    - `refresh_token` (string): refresh token
- Response: 200
- Response body: message

```json
{
  "detail": "Product deleted from cart successfully"
}
```

### POST /api/checkout

- Description: Checkout the current user active cart
- Request: `POST /api/cart/checkout`
  - Body: empty
  - Cookies:
    - `access_token` (string): access token
    - `refresh_token` (string): refresh token
- Response: 200
- Response body: order
