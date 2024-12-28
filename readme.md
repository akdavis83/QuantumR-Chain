# Quantum-Resistant Blockchain

## Overview
This application implements a quantum-safe blockchain system using Flask as the backend and a custom blockchain design. It integrates quantum-resistant cryptographic techniques, such as **Kyber1024**, alongside traditional **ECDSA** for signing transactions.

---

## Key Features

### Quantum-Resistant Keys
- Implements **Kyber1024** for quantum-safe public-private key generation.
- Utilizes **Base58 encoding** for generating unique blockchain addresses.

### Blockchain
- Stores a chain of blocks with **proof-of-work consensus**.
- Supports transactions with **quantum-resistant digital signatures**.

### Endpoints
- Interact with the blockchain through **RESTful APIs**.

### User Wallets
- Allows users to **generate, retrieve, and export keys**.
- Provides secure handling of user wallets with optional password protection.

### Mining
- Implements **proof-of-work** for adding new blocks.
- Rewards miners with a fixed amount of cryptocurrency.

---

## API Endpoints

### General
1. **`GET /`**
   - Returns the main HTML interface for interacting with the blockchain.

2. **`GET /chain`**
   - Fetches the entire blockchain.
   - **Response**:
     ```json
     {
       "chain": [...],
       "length": 3
     }
     ```

3. **`GET /mine`**
   - Mines a new block and adds it to the blockchain.
   - **Response**:
     ```json
     {
       "message": "New Block Mined",
       "block": { ... }
     }
     ```

---

### Transactions
4. **`POST /transactions/sign`**
   - Signs a transaction using the user's private key.
   - **Request Body**:
     ```json
     {
       "address": "sender_address",
       "recipient": "recipient_address",
       "amount": 100
     }
     ```
   - **Response**:
     ```json
     {
       "signature": "transaction_signature"
     }
     ```

5. **`POST /transactions/new`**
   - Submits a new transaction to the blockchain.
   - **Request Body**:
     ```json
     {
       "sender": "sender_address",
       "recipient": "recipient_address",
       "amount": 100,
       "signature": "transaction_signature"
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Transaction will be added to Block 4"
     }
     ```

---

### Keys
6. **`POST /generate_keys`**
   - Generates a quantum-resistant key pair for a user.
   - **Request Body**:
     ```json
     {
       "user_id": "unique_user_id",
       "password": "optional_password"
     }
     ```
   - **Response**:
     ```json
     {
       "public_key": "hex_public_key",
       "private_key": "hex_private_key",
       "address": "blockchain_address"
     }
     ```

7. **`GET /get_keys/<user_id>`**
   - Retrieves the keys associated with a user ID.
   - **Response**:
     ```json
     {
       "keys": [
         {
           "public_key": "hex_public_key",
           "private_key": "hex_private_key",
           "address": "blockchain_address"
         }
       ]
     }
     ```

8. **`GET /export_keys/<user_id>/<address>`**
   - Exports the key pair for a specific address as a downloadable JSON file.

---

### Wallets and Balances
9. **`GET /balance/<address>`**
   - Checks the balance of a specific blockchain address.
   - **Response**:
     ```json
     {
       "address": "blockchain_address",
       "balance": 1000
     }
     ```

---

## Key Derivation

### Seed Generation
- **With Password**: The seed is derived using the **SHA3-256** hash of the concatenation of `user_id` and `password` for deterministic key generation.
- **Without Password**: A 32-byte random seed is generated using `os.urandom` for non-deterministic key generation.

### Kyber Key Pair Generation
- **Public Key (pk)**: Encodes the polynomial matrix and parameters for encryption.
- **Secret Key (sk)**: Encodes private parameters for decryption.
- Resistant to quantum attacks, ensuring long-term security.

### Address Generation
- The public key is hashed using **SHA3-256**.
- The first 20 bytes of the hash are encoded with **Base58Check** to generate a unique blockchain address.

---

## Wallet Initialization and Storage
- Wallets are initialized in `self.user_wallets`:
  - Passwords are hashed using **SHA3-256**.
  - Keys and addresses are stored in a list, allowing multiple key pairs per user.
- Balances are initialized to `0` in `self.balances`.

---

## Security Considerations
- **Password Hashing**: Passwords are hashed, but adding a salt enhances security.
- **Entropy**: `os.urandom` ensures strong randomness for non-deterministic key generation.
- **Kyber1024**: Provides AES-256 equivalent security, suitable for quantum resistance.
- **Address Uniqueness**: Public key hashing ensures unique addresses.

---

## Example Key Pair
```json
{
  "public_key": "hex_public_key",
  "private_key": "hex_private_key",
  "address": "blockchain_address"
}
