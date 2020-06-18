# RBMS
## Retail Bank Management System
# RBMS

Retail Bank Management System

- To run this code install all the dependencies into virtual environment by
  - pip install –r requirements.txt
- Then type following command to start the server
  - flask run
- Then go to following link
  - [https://127.0.0.1:5000](https://127.0.0.1:5000/)
  - Or
  - [https://localhost:5000](https://localhost:5000/)

# Login/Registration

- When you visit the above link,two default accounts for user and two roles will be created/inserted into database
  - [executive@gmail.com](mailto:executive@gmail.com) (Customer Account Executive)
    - Password:123456789
    - roleId:1111
    - roleName:CAE
  - [cashier@gmail.com](mailto:cashier@gmail.com)
    - Password:123456789(Cashier/Teller)
    - roleId:2222
    - roleName:C/T
- You can perform login by above credentials
- And different options will be provided according to login
- We have also provided option for registration, in case you want to add another CAE or C/T,but roleId should be either 1111 for executive or 2222 for cashier/teller.

# Create Customer

- Customer Id is randomly generated starting with 10……..
- SSN Id is provided by Executive

# Create Account

- Account Id is randomly generated starting with 30………
- Customer Id is provided by Executive

# Transactions

- Transaction Id is randomly generated starting with