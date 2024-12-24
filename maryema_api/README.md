# **Maryema**

## **Models**

- [x] [User](#user)
- [x] [Profile](#profile)
- [x] [Division](#division)
- [x] [Category](#category)
- [x] [Product](#product)
- [x] [Collection](#collection)
- [x] [Size](#size)
- [x] [Color](#color)
- [x] [Img](#image)
- [x] [ProductVariant](#productvariant)
- [x] [Feedback](#feedback)
- [ ] [Cart](#cart)
- [ ] [CartItem](#cartitem)
- [ ] [Order](#order)
- [ ] [OrderItem](#orderitem)
- [ ] [DiscountRole](#discountrole)
- [ ] [DiscountCode](#discountcode)

### **[User](#models)**

The `User` model is the default user model provided by Django. It is used to store information about the users of the application.

| Field        | Type     | Description                  |
| ------------ | -------- | ---------------------------- |
| id           | int      | The user's ID                |
| created_at   | datetime | when the user was created    |
| last_login   | datetime | when the user last logged in |
| username     | string   | unique username              |
| email        | string   | unique email                 |
| password     | string   | hashed password              |
| first_name   | string   | the user's first name        |
| last_name    | string   | the user's last name         |
| is_active    | boolean  | is the user active           |
| is_superuser | boolean  | is the user a superuser      |
| is_staff     | boolean  | is the user staff            |

### **[Profile](#models)**

The `Profile` model is used to store additional information about the users of the application.

| Field      | Type          | Description                                 |
| ---------- | ------------- | ------------------------------------------- |
| id         | uuid          | The profile's ID                            |
| created_at | date          | when the profile was created                |
| updated_at | date          | when the profile was last updated           |
| user       | OneToOneField | The user associated with the profile        |
| phone      | string        | The user's phone number                     |
| avatar     | image         | The user's avatar                           |
| role       | string        | The user's role (customer - vendor - admin) |
| note       | text          | A note about the user                       |

### **[Division](#models)**

The `Division` model is used to store information about the divisions available in the application.

| Field      | Type   | Description                        |
| ---------- | ------ | ---------------------------------- |
| id         | uuid   | The division's ID                  |
| created_at | date   | when the division was created      |
| updated_at | date   | when the division was last updated |
| name       | string | The division's name                |
| code       | string | The division's code                |

### **[Category](#models)**

The `Category` model is used to store information about the categories available in the application (e.g. Dress, hijab, ...).

| Field       | Type                 | Description                        |
| ----------- | -------------------- | ---------------------------------- |
| id          | uuid                 | The category's ID                  |
| created_at  | date                 | when the category was created      |
| updated_at  | date                 | when the category was last updated |
| division_id | ForeignKey(Division) | The category's division ID         |
| name        | string               | The category's name                |
| description | text                 | The category's description         |

### **[Product](#models)**

The `Product` model is used to store information about the products available in the application.

| Field       | Type                 | Description                                     |
| ----------- | -------------------- | ----------------------------------------------- |
| id          | uuid                 | The product's ID                                |
| created_at  | datetime             | when the product was created                    |
| updated_at  | datetime             | when the product was last updated               |
| category_id | ForeignKey(Category) | The product's category ID                       |
| name        | string               | The product's name                              |
| description | text                 | The product's description                       |
| tags        | string               | list of tags separated by comma used for search |
| vendor_id   | uuid                 | The product's vendor ID (profile_id)            |

### **[Color](#models)**

The `Color` model is used to store information about the colors available in the application.

| Field      | Type   | Description                                 |
| ---------- | ------ | ------------------------------------------- |
| id         | uuid   | The color's ID                              |
| created_at | date   | when the color was created                  |
| updated_at | date   | when the color was last updated             |
| name       | string | The color's name                            |
| value      | string | The color's value (hex code, e.g., #ffffff) |

### **[Size](#models)**

The `Size` model is used to store information about the sizes available in the application.

| Field      | Type   | Description                    |
| ---------- | ------ | ------------------------------ |
| id         | uuid   | The size's ID                  |
| created_at | date   | when the size was created      |
| updated_at | date   | when the size was last updated |
| name       | string | The size's name                |

### **[Img](#models)**

The `Img` model is used to store information about the images available in the application.

| Field      | Type | Description                     |
| ---------- | ---- | ------------------------------- |
| id         | uuid | The image's ID                  |
| created_at | date | when the image was created      |
| updated_at | date | when the image was last updated |
| src        | file | The image file                  |
| alt        | text | The image's alt text            |
| width      | int  | The image's width               |
| height     | int  | The image's height              |

### **[ProductVariant](#models)**

The `ProductVariant` model is used to store information about the product variants available in the application.

| Field      | Type                | Description                          |
| ---------- | ------------------- | ------------------------------------ |
| id         | uuid                | The product variant's ID             |
| created_at | datetime            | when the product variant was created |
| updated_at | datetime            | when the product variant was updated |
| product_id | ForeignKey(Product) | product ID                           |
| color_id   | ForeignKey(Color)   | color ID                             |
| size_id    | ForeignKey(Size)    | size ID                              |
| image_id   | ForeignKey(Image)   | image ID                             |
| cost       | decimal             | cost price from vendor               |
| price      | decimal             | price for customers                  |
| quantity   | int                 | quantity in stock                    |
| sort_order | int                 | number to be sorted with             |

### **[Collection](#models)**

The `Collection` model is used to store information about collections of products in the application.

| Field       | Type                     | Description                              |
| ----------- | ------------------------ | ---------------------------------------- |
| id          | uuid                     | The collection's ID                      |
| created_at  | datetime                 | when the product variant was created     |
| updated_at  | datetime                 | when the product variant was updated     |
| name        | string                   | The name of the collection               |
| description | text                     | The description of the collection        |
| products    | ManyToManyField(Product) | many-to-many relation with Product model |

### **[Feedback](#models)**

The `Feedback` model is used tos tore the feedback (rate and comment) of a customer on a product.

| Field      | Type                | Description                                               |
| ---------- | ------------------- | --------------------------------------------------------- |
| id         | uuid                | The feedback's ID                                         |
| created_at | datetime            | when the product variant was created                      |
| updated_at | datetime            | when the product variant was updated                      |
| customer   | ForeignKey(Profile) | the id of the customer (profile_id)                       |
| product    | ForeignKey(Product) | the id of the product                                     |
| rate       | int                 | the rate of the product given by the customer (1-5 stars) |
| comment    | text                | the comment of the customer on the product                |

### **[DiscountRule](#models)**

The `DiscountRule` model is used to store information about the discount rules available in the application.

| Field                                      | Type                             | Description                                                                     |
| ------------------------------------------ | -------------------------------- | ------------------------------------------------------------------------------- |
| id                                         | uuid                             | The discount rule's ID                                                          |
| created_at                                 | datetime                         | when the discount rule was created                                              |
| updated_at                                 | datetime                         | when the discount rule was updated                                              |
| starts_at                                  | datetime                         | when the discount rule starts                                                   |
| ends_at                                    | datetime                         | when the discount rule ends                                                     |
| title                                      | string                           | The title of the discount rule                                                  |
| value_type                                 | string                           | The type of the discount value (fixed_amount, percentage)                       |
| value                                      | decimal                          | The value of the discount                                                       |
| customer_selection                         | string                           | The customer selection method (prerequisite, all)                               |
| prerequisite_customer_ids                  | list[ForeignKey(Profile)]        | The customers that must have the discount                                       |
| target_selection                           | string                           | The target selection method (entitled, all)                                     |
| entitled_collection_ids                    | list[ForeignKey(Collection)]     | The collections to which the discount is applied                                |
| entitled_product_ids                       | list[ForeignKey(Product)]        | The products to which the discount is applied                                   |
| entitled_variant_ids                       | list[ForeignKey(ProductVariant)] | The variants to which the discount is applied                                   |
| prerequisite_collection_ids                | list[ForeignKey(Collection)]     | The collections required for the discount                                       |
| prerequisite_product_ids                   | list[ForeignKey(Product)]        | The products required for the discount                                          |
| prerequisite_variant_ids                   | list[ForeignKey(ProductVariant)] | The variants required for the discount                                          |
| prerequisite_subtotal_range                | int                              | The subtotal range required for the discount (less than or equal to this value) |
| prerequisite_quantity_range                | int                              | The quantity range required for the discount (less than or equal to this value) |
| prerequisite_to_entitlement_quantity_ratio | dict                             | The prerequisite to entitlement quantity ratio                                  |
| prerequisite_to_entitlement_purchase       | dict                             | The prerequisite to entitlement purchase amount                                 |
| once_per_customer                          | boolean                          | Is the discount once per customer                                               |
| usage_limit                                | int                              | The maximum number of times the price rule can be used, per discount code.      |
| allocation_method                          | string                           | The allocation method (each, across)                                            |
| allocation_limit                           | int                              | The allocation limit of the discount                                            |

### **[DiscountCode](#models)**

The `DiscountCode` model is used to store information about the discount codes available in the application.

| Field         | Type                     | Description                                |
| ------------- | ------------------------ | ------------------------------------------ |
| id            | uuid                     | The discount code's ID                     |
| created_at    | datetime                 | when the discount code was created         |
| updated_at    | datetime                 | when the discount code was updated         |
| code          | string                   | The discount code                          |
| starts_at     | datetime                 | when the discount code starts              |
| ends_at       | datetime                 | when the discount code ends                |
| usage_count   | int                      | The number of times this code is used      |
| discount_rule | ForeignKey(DiscountRule) | The discount rule associated with the code |

### **[Cart](#models)**

The `Cart` model is used to store information about the cart of a customer.

| Field         | Type                | Description                                                        |
| ------------- | ------------------- | ------------------------------------------------------------------ |
| id            | uuid                | The cart's id                                                      |
| created_at    | datetime            | when the product variant was created                               |
| updated_at    | datetime            | when the product variant was updated                               |
| customer      | ForeignKey(Profile) | the id of the customer (profile_id)                                |
| total         | decimal             | the total price of the cart                                        |
| is_active     | boolean             | is the cart active                                                 |
| last_updated  | datetime            | to track cart activity (e.g. the time at which last item is added) |
| discount_code | uuid                | the id of the discount code                                        |

### **[CartItem](#models)**

The `CartItem` model is used to store the product variants and its quantity in specific cart.

| Field           | Type                       | Description                          |
| --------------- | -------------------------- | ------------------------------------ |
| id              | uuid                       | The cart's id                        |
| created_at      | datetime                   | when the product variant was created |
| updated_at      | datetime                   | when the product variant was updated |
| cart            | ForeignKey(Cart)           | the id of the cart                   |
| product_variant | ForeignKey(ProductVariant) | the id of the product variant        |
| quantity        | int                        | the quantity of the product variant  |
| subtotal        | decimal                    | the subtotal price of the item       |

### **[Order](#models)**

The `Order` model is used to store information about the orders of the customers.

| Field         | Type                | Description                         |
| ------------- | ------------------- | ----------------------------------- |
| id            | uuid                | The order's id                      |
| created_at    | datetime            | when the order was created          |
| updated_at    | datetime            | when the order was updated          |
| customer      | ForeignKey(Profile) | the id of the customer (profile_id) |
| total         | decimal             | the total price of the order        |
| status        | string              | the status of the order             |
| discount_code | uuid                | the id of the discount code         |

### **[OrderItem](#models)**

The `OrderItem` model is used to store the product variants and its quantity in specific order.

| Field           | Type                       | Description                          |
| --------------- | -------------------------- | ------------------------------------ |
| id              | uuid                       | The order's id                       |
| created_at      | datetime                   | when the product variant was created |
| updated_at      | datetime                   | when the product variant was updated |
| order           | ForeignKey(Order)          | the id of the order                  |
| product_variant | ForeignKey(ProductVariant) | the id of the product variant        |
| quantity        | int                        | the quantity of the product variant  |
| subtotal        | decimal                    | the subtotal price of the item       |

## **Views**

### **Customer**

The `Customer` view is used to display information about the customers of the application.

- #### **GET** `api/admin/customers/`

  This endpoint returns a list of all customers.

  **Response**

  ```json
  [
    {
      "id": 1,
      "created_at": "2013-06-27T08:48:27-04:00",
      "last_login": "2012-08-24T14:01:46-04:00",
      "username": "davem",
      "email": "bob.norman@mail.example.com",
      "first_name": "John",
      "last_name": "Norman",
      "is_active": true,
      "profile": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "created_at": "2024-12-21T08:48:27-04:00",
        "updated_at": "2024-12-21T08:48:27-04:00",
        "phone": "01152869950",
        "avatar": "http://example.com/avatar.jpg",
        "role": "customer",
        "note": "This is a note about the user."
      }
    }
  ]
  ```

- #### **GET** `api/admin/customers/{id}/`

  This endpoint returns information about a specific customer.

  **Response**

  ```json
  {
    "id": 1,
    "created_at": "2013-06-27T08:48:27-04:00",
    "last_login": "2012-08-24T14:01:46-04:00",
    "username": "davem",
    "email": "bob.norman@mail.example.com",
    "first_name": "John",
    "last_name": "Norman",
    "is_active": true,
    "profile": {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "created_at": "2024-12-21T08:48:27-04:00",
      "updated_at": "2024-12-21T08:48:27-04:00",
      "phone": "01152869950",
      "avatar": "http://example.com/avatar.jpg",
      "role": "customer",
      "note": "This is a note about the user."
    }
  }
  ```

- #### **POST** `api/admin/customers/`

  This endpoint creates a new customer.

  **Request**

  ```json
  {
    "username": "davem",
    "email": "bob.norman@mail.example.com",
    "first_name": "John",
    "last_name": "Norman",
    "is_active": true,
    "profile": {
      "phone": "01152869950",
      "avatar": "http://example.com/avatar.jpg",
      "role": "customer",
      "note": "This is a note about the user."
    }
  }
  ```

  **Response**

  - Status: `201 Created`
  - body:

    ```json
    {
      "id": 1,
      "created_at": "2013-06-27T08:48:27-04:00",
      "last_login": "2012-08-24T14:01:46-04:00",
      "username": "davem",
      "email": "bob.norman@mail.example.com",
      "first_name": "John",
      "last_name": "Norman",
      "is_active": true,
      "profile": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "created_at": "2024-12-21T08:48:27-04:00",
        "updated_at": "2024-12-21T08:48:27-04:00",
        "phone": "01152869950",
        "avatar": "http://example.com/avatar.jpg",
        "role": "customer",
        "note": "This is a note about the user."
      }
    }
    ```

- #### **PUT** `api/admin/customers/{id}/`

  This endpoint updates information about a specific customer.

  **Request**

  ```json
  {
    "username": "new.username",
    "email": "new_email@mail.example.com",
    "first_name": "New",
    "last_name": "Name",
    "is_active": false,
    "profile": {
      "phone": "01052869950",
      "avatar": "http://example.com/avatar2.jpg",
      "note": "This is a note about the user. Updated."
    }
  }
  ```

  **Response**

  - Status: `200 OK`
  - body:

    ```json
    {
      "id": 1,
      "created_at": "2013-06-27T08:48:27-04:00",
      "last_login": "2012-08-24T14:01:46-04:00",
      "username": "new.username",
      "email": "new_email@mail.example.com",
      "first_name": "New",
      "last_name": "Name",
      "is_active": false,
      "profile": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "created_at": "2024-12-21T08:48:27-04:00",
        "updated_at": "2024-12-21T09:51:27-04:00",
        "phone": "01052869950",
        "avatar": "http://example.com/avatar2.jpg",
        "role": "customer",
        "note": "This is a note about the user. Updated."
      }
    }
    ```

- #### **DELETE** `api/admin/customers/{id}/`

  This endpoint deletes a specific customer.

  **Response**

  - Status: `204 No Content`

### **Vendor**

The `Vendor` view is used to display information about the vendors of the application.

- #### **GET** `api/admin/vendors/`

  This endpoint returns a list of all vendors.

  **Response**

  ```json
  [
    {
      "id": 1,
      "created_at": "2013-06-27T08:48:27-04:00",
      "last_login": "2012-08-24T14:01:46-04:00",
      "username": "davem",
      "email": "davendor@mail.example.com",
      "first_name": "John",
      "last_name": "Norman",
      "is_active": false,
      "profile": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "created_at": "2024-12-21T08:48:27-04:00",
        "updated_at": "2024-12-21T08:48:27-04:00",
        "phone": "01152869950",
        "avatar": "http://example.com/avatar.jpg",
        "role": "vendor",
        "note": "This is a note about the user."
      }
    }
  ]
  ```

- #### **GET** `api/admin/vendors/{id}/`

  This endpoint returns information about a specific vendor.

  **Response**

  ```json
  {
    "id": 1,
    "created_at": "2013-06-27T08:48:27-04:00",
    "last_login": "2012-08-24T14:01:46-04:00",
    "username": "davem",
    "email": "davendor@mail.example.com",
    "first_name": "John",
    "last_name": "Norman",
    "is_active": false,
    "profile": {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "created_at": "2024-12-21T08:48:27-04:00",
      "updated_at": "2024-12-21T08:48:27-04:00",
      "phone": "01152869950",
      "avatar": "http://example.com/avatar.jpg",
      "role": "vendor",
      "note": "This is a note about the user."
    }
  }
  ```

- #### **POST** `api/admin/vendors/`

  This endpoint creates a new vendor.

  **Request**

  ```json
  {
    "username": "davem",
    "email": "davendor@mail.example.com",
    "first_name": "John",
    "last_name": "Norman",
    "is_active": false,
    "profile": {
      "phone": "01152869950",
      "avatar": "http://example.com/avatar.jpg",
      "note": "This is a note about the user."
    }
  }
  ```

- #### **PUT** `api/admin/vendors/{id}/`

  This endpoint updates information about a specific customer.

  **Request**

  ```json
  {
    "username": "new.username",
    "email": "davendor2@mail.example.com",
    "first_name": "New",
    "last_name": "Vendor",
    "is_active": true,
    "profile": {
      "phone": "01252869950",
      "avatar": "http://example.com/avatar2.jpg",
      "note": "This is a note about the user. Updated."
    }
  }
  ```

  **Response**

  - Status: `200 OK`
  - body:

    ```json
    {
      "id": 1,
      "created_at": "2013-06-27T08:48:27-04:00",
      "last_login": "2012-08-24T14:01:46-04:00",
      "username": "new.username",
      "email": "davendor2@mail.example.com",
      "first_name": "New",
      "last_name": "Vendor",
      "is_active": true,
      "profile": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "created_at": "2024-12-21T08:48:27-04:00",
        "updated_at": "2024-12-21T09:51:27-04:00",
        "phone": "01252869950",
        "avatar": "http://example.com/avatar2.jpg",
        "note": "This is a note about the user. Updated."
      }
    }
    ```

- #### **DELETE** `api/admin/vendors/{id}/`

  This endpoint deletes a specific vendor.

  **Response**

  - Status: `204 No Content`

### **Admin**

The `Admin` view is used to display information about the admins of the application.

- #### **GET** `api/admin/admins/`

  This endpoint returns a list of all admins.

  **Response**

  ```json
  [
    {
      "id": 1,
      "created_at": "2013-06-27T08:48:27-04:00",
      "last_login": "2012-08-24T14:01:46-04:00",
      "username": "davem",
      "email": "davendor@mail.example.com",
      "first_name": "John",
      "last_name": "Norman",
      "is_active": true,
      "profile": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "created_at": "2024-12-21T08:48:27-04:00",
        "updated_at": "2024-12-21T08:48:27-04:00",
        "phone": "01152869950",
        "avatar": "http://example.com/avatar.jpg",
        "role": "admin",
        "note": "This is a note about the user."
      }
    }
  ]
  ```

- #### **GET** `api/admin/admins/{id}/`

  This endpoint returns information about a specific admin.

  **Response**

  ```json
  {
    "id": 1,
    "created_at": "2013-06-27T08:48:27-04:00",
    "last_login": "2012-08-24T14:01:46-04:00",
    "username": "davem",
    "email": "davendor@mail.example.com",
    "first_name": "John",
    "last_name": "Norman",
    "is_active": true,
    "profile": {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "created_at": "2024-12-21T08:48:27-04:00",
      "updated_at": "2024-12-21T08:48:27-04:00",
      "phone": "01152869950",
      "avatar": "http://example.com/avatar.jpg",
      "role": "admin",
      "note": "This is a note about the user."
    }
  }
  ```

- #### **POST** `api/admin/admins/`

  This endpoint creates a new admin.

  **Request**

  ```json
  {
    "username": "davem",
    "email": "davendor@mail.example.com",
    "first_name": "John",
    "last_name": "Norman",
    "is_active": true,
    "profile": {
      "phone": "01152869950",
      "avatar": "http://example.com/avatar.jpg",
      "note": "This is a note about the user."
    }
  }
  ```

- #### **PUT** `api/admin/admins/{id}/`

  This endpoint updates information about a specific admin.

  **Request**

  ```json
  {
    "username": "new.username",
    "email": "davendor2@mail.example.com",
    "first_name": "New",
    "last_name": "Vendor",
    "is_active": false,
    "profile": {
      "phone": "01252869950",
      "avatar": "http://example.com/avatar2.jpg",
      "note": "This is a note about the user. Updated."
    }
  }
  ```

  **Response**

  - Status: `200 OK`
  - body:

    ```json
    {
      "id": 1,
      "created_at": "2013-06-27T08:48:27-04:00",
      "last_login": "2012-08-24T14:01:46-04:00",
      "username": "new.username",
      "email": "davendor2@mail.example.com",
      "first_name": "New",
      "last_name": "Vendor",
      "is_active": false,
      "profile": {
        "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
        "created_at": "2024-12-21T08:48:27-04:00",
        "updated_at": "2024-12-21T09:51:27-04:00",
        "phone": "01252869950",
        "avatar": "http://example.com/avatar2.jpg",
        "note": "This is a note about the user. Updated."
      }
    }
    ```

- #### **DELETE** `api/admin/admins/{id}/`

  This endpoint deletes a specific admin.

  **Response**

  - Status: `204 No Content`
