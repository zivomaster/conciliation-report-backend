## OpenAPI Specification - CONCILIATION-REPORT

### API Paths

#### /api/v1/login/access-token

#### POST /api/v1/login/access-token
- **Summary**: Login Access Token
- **Description**: OAuth2 compatible token login, get an access token for future requests
- **Operation ID**: login_access_token_api_v1_login_access_token_post
- **Request**:
  - **Content Type**: application/x-www-form-urlencoded
  - **Schema**: Body_login_access_token_api_v1_login_access_token_post
  - **Required**: true
- **Responses**:
  - **200**: Successful Response
    - **Content Type**: application/json
    - **Schema**: Token
  - **422**: Validation Error
    - **Content Type**: application/json
    - **Schema**: HTTPValidationError

#### /api/v1/login/test-token

#### POST /api/v1/login/test-token
- **Summary**: Test Token
- **Description**: Test access token
- **Operation ID**: test_token_api_v1_login_test_token_post
- **Responses**:
  - **200**: Successful Response
    - **Content Type**: application/json
    - **Schema**: User
  - **Security**: OAuth2PasswordBearer

#### /api/v1/reset-password/

#### POST /api/v1/reset-password/
- **Summary**: Reset Password
- **Description**: Reset password
- **Operation ID**: reset_password_api_v1_reset_password__post
- **Request**:
  - **Content Type**: application/json
  - **Schema**: Body_reset_password_api_v1_reset_password__post
  - **Required**: true
- **Responses**:
  - **200**: Successful Response
    - **Content Type**: application/json
    - **Schema**: Msg
  - **422**: Validation Error
    - **Content Type**: application/json
    - **Schema**: HTTPValidationError

#### /api/v1/users/

#### GET /api/v1/users/
- **Summary**: List Users
- **Description**: Retrieve users.
- **Operation ID**: list_users_api_v1_users__get
- **Parameters**:
  - Skip (query, integer, default: 0)
  - Limit (query, integer, default: 100)
- **Responses**:
  - **200**: Successful Response
    - **Content Type**: application/json
    - **Schema**: array of User
  - **422**: Validation Error
    - **Content Type**: application/json
    - **Schema**: HTTPValidationError
- **Security**: OAuth2PasswordBearer

#### POST /api/v1/users/
- **Summary**: Create User
- **Description**: Create new user.
- **Operation ID**: create_user_api_v1_users__post
- **Request**:
  - **Content Type**: application/json
  - **Schema**: UserCreate
  - **Required**: true
- **Responses**:
  - **200**: Successful Response
    - **Content Type**: application/json
    - **Schema**: User
  - **422**: Validation Error
    - **Content Type**: application/json
    - **Schema**: HTTPValidationError

#### /api/v1/users/{user_id}

#### PUT /api/v1/users/{user_id}
- **Summary**: Update User
- **Description**: Update a user.
- **Operation ID**: update_user_api_v1_users__user_id__put
- **Parameters**:
  - User ID (path, string)
- **Request**:
  - **Content Type**: application/json
  - **Schema**: UserUpdate
  - **Required**: true
- **Responses**:
  - **200**: Successful Response
    - **Content Type**: application/json
    - **Schema**: User
  - **422**: Validation Error
    - **Content Type**: application/json
    - **Schema**: HTTPValidationError

#### /api/v1/connectors-types/

#### GET /api/v1/connectors-types/
- **Summary**: List Connectors Types
- **Description**: Retrieve connectors types.
- **Operation ID**: list_connectors_types_api_v1_connectors_types__get
- **Parameters**:
  - Skip (query, integer, default: 0)
  - Limit (query, integer, default: 100)
- **Responses**:
  - **200**: Successful Response
    - **Content Type**: application/json
    - **Schema**: object
  - **422**: Validation Error
    - **Content Type**: application/json
    - **Schema**: HTTPValidationError
- **Security**: OAuth2PasswordBearer

#### /api/v1/save-connection/

#### POST /api/v1/save-connection/
- **Summary**: Save Connection
- **Description**: Save and Update connections
- **Operation ID**: save_connection_api_v1_save_connection__post
- **Request**:
  - **Content Type**: application/json
  - **Schema**: DatabaseConnectionCreate
  - **Required**: true
- **Responses**:
  - **200**: Successful Response
    - **Content Type**: application/json
    - **Schema**: object
  - **422**: Validation Error
    - **Content Type**: application/json
    - **Schema**: HTTPValidationError

#### /api/v1/generate-keys/

#### GET /api/v1/generate-keys/
- **Summary**: Generate Keys
- **Description**: Generate public and private keys
