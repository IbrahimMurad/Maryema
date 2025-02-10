# Maryema

A clothes and accessories store web application.

## Description

This is a web application for a clothes & accessories store. It allows users to:

- View the available clothes.
- View the details of a specific product.
- Add it to their cart.
- View their cart, edit the quantity or remove items from it.
- Add a discount code.
- Proceed to checkout.
- View their profile and update their information.
- Track their orders.

For the admin, they can:

- Add new products.
- Edit the details of a product.
- Delete a product.
- Add details related to products, such as sizes and colors.
- View the list of orders and their details.
- Change the status of an order.
- View the list of users and their details.
- Change the role of a user.
- View an analytics dashboard.
- Create discount rules and codes.
- View the list of discount codes and their details.

## Features

- User authentication and authorization using JWT.
- Product catalog with filtering and searching.
- Redis for caching.
- Shopping cart management.
- Order processing and tracking.
- Admin panel for managing products, orders, users, and discounts.
- Analytics dashboard for admins.
- Feedback and rating system.
- Responsive design for mobile and desktop.
- SEO optimization.
- Swagger documentation for the API.
- Unit tests for models and views.

## Technologies

1. Backend:

<div style="display: flex; justify-content: center; gap: 1.5rem;">

[![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)

[![DRF](https://img.shields.io/badge/-Django%20REST%20Framework-red?style=flat&logo=django)](https://www.django-rest-framework.org/)

[![JWT](https://img.shields.io/badge/-SimpleJWT-000000?style=flat&logo=json-web-tokens)](https://django-rest-framework-simplejwt.readthedocs.io/)

[![Django Filter](https://img.shields.io/badge/-Django%20Filter-blue?style=flat&logo=django)](https://django-filter.readthedocs.io/)

[![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)

[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

</div>

1. Frontend:

<div style="display: flex; justify-content: center; gap: 1.5rem;">

[![React](https://img.shields.io/badge/-React-61DAFB?style=flat&logo=react&logoColor=white)](https://reactjs.org/)

[![Material-UI](https://img.shields.io/badge/-Material%20UI-0081CB?style=flat&logo=material-ui&logoColor=white)](https://material-ui.com/)

[![Tailwind CSS](https://img.shields.io/badge/-Tailwind%20CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

[![styled-components](https://img.shields.io/badge/-styled%20components-DB7093?style=flat&logo=styled-components&logoColor=white)](https://styled-components.com/)

[![Next.js](https://img.shields.io/badge/-Next.js-000000?style=flat&logo=next.js&logoColor=white)](https://nextjs.org/)

</div>

## Installation

1. Clone the repository.

```bash
git clone git@github.com:IbrahimMurad/Maryema.git
```

2. Create a virtual environment and activate it.

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Change the directory to maryema_api (the backend).

```bash
cd Maryema/maryema_api
```

4. Install the requirements.

```bash
pip3 install -r requirements.txt
```

5. Change the name of .env.dist file to .env and fill in the required information.
6. Make sure to create the databse you specifies in the .env file.
7. Run the migrations.

```bash
python3 manage.py migrate
```

8. Create a superuser.

```bash
python3 manage.py createsuperuser
```

9. Run the server.

```bash
python3 manage.py runserver
```

> **Note:** Now, you can check the browsable API by visiting `/api/` and explore the API documentation at `/swagger/`

1.  Change the directory to frontend (the frontend).

```bash
cd ../frontend
```

11. Install the requirements.

```bash
npm install
```

12. Run the server.

```bash
npm start
```

13. Open your browser and go to http://localhost:3000.

## Usage

1. Register a new user.
2. Login with the new user.
3. Explore the available products.
4. Add a product to the cart.
5. Proceed to checkout.
6. View your profile and update your information.
7. Track your orders.
8. Logout.
9. Login with the superuser you created.
10. Explore the admin panel.
11. Add new products.
12. Edit the details of a product.
13. Delete a product.
14. Add details related to products, such as sizes and colors.
15. View the list of orders and their details.
16. Change the status of an order.
17. View the list of users and their details.
18. Change the role of a user.
19. View an analytics dashboard.
20. Create discount rules and codes.
21. View the list of discount codes and their details.
22. Logout.

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Commit your changes.
5. Push the changes to your branch.
6. Create a pull request.
7. Wait for the maintainers to review your pull request.
8. If it's approved, it will be merged.
9. If it needs changes, you will be asked to make them.
10. Once everything is done, your pull request will be merged.
11. Congratulations! You've successfully contributed to this project.

## Roadmap

- [x] design the database.
- [x] create the models.
- [x] Test the models.
- [ ] Create users views.
  - [x] Create the required serializers.
  - [x] Create users views for both admin and normal users.
  - [x] Add filters and search for list view for admins.
  - [x] Create auth views.
    - [x] Use simpleJWT for JWT authentication.
    - [x] Return the tokens in a secure HttpOnly cookie.
    - [x] Remove the tokens from the response body.
    - [x] Add the refresh token view.
    - [x] Add the logout view.
  - [ ] Test the views.
- [x] Create urls for the users.
- [ ] Create products views.
  - [x] Create the required serializers.
  - [x] Create products views (create and update for admin and list and retrieve for users).
  - [x] Add filters for the list view.
  - [ ] Test the views.
- [x] Create urls for the products.
- [ ] Create feedback views.
  - [x] Create the required serializers.
  - [x] Create feedback views.
  - [ ] Test the views.
- [x] Create urls for the feedback.
- [ ] Create Cart views.
  - [x] Create the required serializers.
  - [x] Create Cart views.
  - [ ] Test the views.
- [x] Create urls for the carts.
- [ ] Create Order views.
  - [x] Create the required serializers.
  - [x] Create Order views.
  - [ ] Test the views.
- [x] Create urls for the orders.
- [ ] Create Discount views.
  - [ ] Create the required serializers.
  - [ ] Create Discount views.
  - [ ] Test the views.
- [ ] Create urls for the discounts.
- [ ] Create Analytics views.
  - [ ] Create the required serializers.
  - [ ] Create Analytics views.
  - [ ] Test the views.
- [ ] Create urls for the analytics.

- [ ] Create the frontend.
  - [ ] Create the home/products page.
  - [ ] Create the product details page.
  - [ ] Create the login page.
  - [ ] Create the register page.
  - [ ] Create the profile page.
  - [ ] Create the checkout page.
  - [ ] Create the orders page.
  - [ ] Create the admin panel.
  - [ ] Create the analytics page.
  - [ ] Create the discount codes page.
  - [ ] Create the discount rules page.
  - [ ] Create the users page.
  - [ ] Create the products page.
  - [ ] Create the product creation page.
  - [ ] Create the orders page.
  - [ ] Create the feedback page.
  - [ ] Create the cart page.
  - [ ] Create the 404 page.
  - [ ] Create the 500 page.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact me

- [Ibrahim Murad](mailto:ibrahimmorad31@gmail.com)

## Social

- [LinkedIn](https://www.linkedin.com/in/ibrahim-morad-228410209/)
- [GitHub](https://github.com/IbrahimMurad)
- [Frontend Mentor](https://www.frontendmentor.io/profile/IbrahimMurad)
