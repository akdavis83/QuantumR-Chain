# Quantum-Resistant Blockchain Documentation

Overview
This application implements a quantum-safe blockchain system using Flask as the backend and a custom blockchain design. It incorporates quantum-resistant cryptographic techniques, such as Kyber1024, and traditional ECDSA for signing transactions.

Key Features
Quantum-Resistant Keys:

Implements Kyber1024 for quantum-safe public-private key generation.
Uses base58 encoding for generating unique blockchain addresses.

Blockchain:

Stores a chain of blocks with proof-of-work consensus.
Supports transactions with quantum-resistant digital signatures.
Endpoints:

Interact with the blockchain through RESTful APIs.
User Wallets:

Allows users to generate, retrieve, and export keys.
Provides secure handling of user wallets with optional password protection.
Mining:

Implements proof-of-work for adding new blocks.
Rewards miners with a fixed amount of cryptocurrency.
API Endpoints
1. /
Method: GET
Description: Returns the main HTML interface for interacting with the blockchain.

2. /chain
Method: GET
Description: Fetches the entire blockchain.
Response:

{
  "chain": [ ... ],
  "length": 3
}

3. /mine
Method: GET
Description: Mines a new block and adds it to the blockchain.
Response:

{
  "message": "New Block Mined",
  "block": { ... }
}

4. /transactions/sign
Method: POST
Description: Signs a transaction using the user's private key.
Request Body:

{
  "address": "sender_address",
  "recipient": "recipient_address",
  "amount": 100
}

Response:

{
  "signature": "transaction_signature"
}

5. /transactions/new
Method: POST
Description: Submits a new transaction to the blockchain.
Request Body:

{
  "sender": "sender_address",
  "recipient": "recipient_address",
  "amount": 100,
  "signature": "transaction_signature"
}
Response:

{
  "message": "Transaction will be added to Block 4"
}

6. /generate_keys
Method: POST
Description: Generates a quantum-resistant key pair for a user.
Request Body:

{
  "user_id": "unique_user_id",
  "password": "optional_password"
}
Response:

{
  "public_key": "hex_public_key",
  "private_key": "hex_private_key",
  "address": "blockchain_address"
}

7. /get_keys/<user_id>
Method: GET
Description: Retrieves the keys associated with a user ID.
Response:

{
  "keys": [
    {
      "public_key": "hex_public_key",
      "private_key": "hex_private_key",
      "address": "blockchain_address"
    }
  ]
}

8. /export_keys/<user_id>/<address>
Method: GET
Description: Exports the key pair for a specific address as a downloadable JSON file.
Response: Downloads a JSON file containing the key pair.

9. /balance/<address>
Method: GET
Description: Checks the balance of a specific blockchain address.
Response:

{
  "address": "blockchain_address",
  "balance": 1000
}

Key Derivation
Seed Generation:

If a password is provided, the seed is derived using the SHA3-256 hash of the concatenation of the user_id and password. This ensures deterministic key generation for the same user_id and password.
If no password is provided, a 32-byte random seed is generated using os.urandom. This provides non-deterministic key generation.

Kyber Key Pair Generation:

The Kyber1024 cryptographic scheme is used to generate the key pair:
Public Key (pk): Encodes the polynomial matrix and parameters used for encryption.
Secret Key (sk): Encodes the private parameters used for decryption.
The Kyber scheme is resistant to quantum attacks, making it suitable for long-term security.
Address Generation
The public key is hashed using SHA3-256, and the first 20 bytes of the hash are encoded with Base58Check to generate a unique address. This mimics how cryptocurrency addresses are often derived.
Wallet Initialization and Storage

A user wallet is initialized or updated in the self.user_wallets dictionary:
Passwords are stored as SHA3-256 hashes for security.
Keys and addresses are stored in a list, allowing multiple key pairs per user.
Balance Initialization
A new balance entry is created for the generated address in self.balances, initialized to 0.
Key Entry Return
The function returns a dictionary containing:
The public key (pk) in hexadecimal format.
The private key (sk) in hexadecimal format.
The generated address.
Security Considerations

Password Hashing:

The password is hashed before storage, which is a good practice.
However, adding a salt to the password hash would enhance security by mitigating rainbow table attacks.

Random Seed:

Using os.urandom ensures strong entropy for non-deterministic key generation.
Kyber1024:

Kyber1024 offers high security (analogous to AES-256) and is suitable for applications requiring quantum resistance.
Address Uniqueness:

Address generation using the public key hash ensures uniqueness and prevents collisions.
Analysis of the Generated Key Components

Private Key:

The Kyber secret key is used for decryption and is highly sensitive. It must be securely stored and protected against unauthorized access.

Public Key:

The public key is used for encryption and can be shared freely. Its derivation from the Kyber scheme ensures compatibility with post-quantum cryptography.

Address:

The address is a compact representation derived from the public key, suitable for user identification in applications like wallets.

Example of a derived key pair:

{
    "public_key": "fef61007e1c9bd116904f0285d0a93c5693e03b05e16f477f8866e2431b525d5b93d212c643b30ccfc94d2b2469477991e07b10e282b2bb035c93ac4839b60ab58539674bf3fd523576a45dbe1809fd2238cd975f0c031e21456c160799be93c69d233a15b7d59e177aca13502a4536c420054f14687dc25f2eb2b9274c1ef6773c4e94a9532b9a106bdc63aaa1ed2ad929042b298bda44325f629b5537bc5e18387bd0ba2dab75eb0514fbaba5bf6aa1400a63172359da6ba6dd0c83d56214100f892a42c779e4408aa204ad03a3e492611290a812861912249c5bdf2bd7354526f768ca79b52abf5bc2f99af2e0754ff6a28c6c0a92eda5219658da88791e31ca84a81be805b23724c521085a165e77fbd30b3e51a587b91abbfd8b94045b9028142ff8b9b5cda6c5f44105b446c22873b24095395eb61bc417398b290aac55e3e75717e5651c5aa38ebc3a44317ae89770a37c991b7547401a7c3c6a69fde5234c7f10c426785d2073f15d4ae988889a8a2620d2569269745b86a407c0b454eeb4562e2ab43ba1fdd03931c04b480c96a3b0581a6ca8413681632478c61998663003acfb04c56b74e4aa05adb2c6745f6343dcc55fec803f5acba6125bc993c9349994989e6171d8873a7c25edd15cf62fcbe64b0b504c405b905c2efb1246732524567739622500c954791b40f02050a8133bb70f545c3a833f287af846101f1013f38f8a73de03a5c04d063528111dacb29dc16bebc474f6a856b88798ff61aa94b068d5a93ac9b3aa7c741c5bba8b6395483c6a1bd6803e0754d1f304674648fce7268fb4166294b50d37413ea4561a4c66a561a71d780a9db9369868c839765af65d89fb62c97b341754900b3b886736eb3035bf27666c019708027e16329559a3047494c74376271573c3d224c7de69b5811ad8fbc684bebc28bc490a83842bc630851095ef140c9bed924342941dbf48687e7c6c50c55d051852f9c5ccac4784ae95cf7aa34c549b468263c19752d20a1867f77c4a01b546312bcdbe54ef2e541cbc658f2fc07714c42f2db6d6eb5a3213bc60ce4be28d1a39372a68e95579ae61a3351a655f18fc9b31cc04562c656910a6ab46e22ac57116cb2f155a90805ca1277813946ee76ae1e5221ddda1ac142abcaeb4c05c58b797705003499adca397c15ca7266284cab44b5d944ca73b4d7f21400b744a3208856a7a8f402192172a0ba30274067ad688b98e1017ee4a90cc237122f61513f80a1810a1ddcb8c4ed73a88af52cafe516dc20946276ca8aeb06d6036c436684e0181142f04d33a23620aa7bb133642404c20aa816373149b0f049c8f1150ab111337306cceac9574479d683bec59389a741227bc0976e025b8f76af1928207bda56c890a13b02471f041954266820b454347cbe18ea8923d6261a96bf14688048a5aa75a13db1d80649454b75734d7eb212ebc35333c4a728314bb81bbabc24845a631ad5ecc1fb778d8d2ab497f3933f09833fd0bc85a2b7157c1dfc1325c8a988995b95229b4291e9105fc161fe146c143687b2d58c56118531d92156e75e80ea440a347aa0e10ca2cc8510386a904b01d4d155d2abc05be3852f15064e4c7eb4a34b1e183c20486c05999eaecc6508038cc0e853689195f9954ae35b6d4a31a087fc087b643aa3fb29c77b9e247424db1c203b29abec8a9a50898555c392ff133bfae9b282068d73cacff62687e4b40584932907b18f965c02ffa51c83159049a8269d008b5c15c863d10394275725b901f92281f9522f3fca9ed6d29ef4e80d970ca948564b9c803b18630c6dfccb44b0804f863f803a580e85098f68c6dfb9423942185b2827f4e1c56f9151fcb41283185eab0348fe0283e5f21678906b4c6365ad688aa44146664a8bdc9824a05a99a0a625b56415a0a7464bbc41d591274fd12647d51570f2a984e7bc2e4907641260d836c4b8bac993aa0512308270ea7a2d45b0d098cb8a4b15758098cd87316e95680b297fe562477f3ab80a507c479a3ac8fc5dd743bdd4db02ea36128bf22fd4abcedb1ba03a24127d64b2b8eb94462330eb72c36daa6155a238ba300a89427b0f818b5d8c78a9288a4f627178ec1c72c7bb971b4868d0120004b169fac7a0f537b935cd99fca207812223205a6f432d888797070a44f568e712cae959d0aa92301080b94cb55bddc0dc620c5a931e18",

    "private_key": "004c6cfaf94486b8ae153ccd280a0ae2988bdce123ca35a10b06be172c064c7626188c69f5bc251a253d1dcaac37b300ce208db2147a4211cb99fc9525ea912f0cbe0d47ab7ff5bed7b1c79d3378e3c39feb9074ab1502c50851359442c19a2ef946277be4b6363c6757da61758079f1e544451ca3ca204556cccd3acb9572b28a12d9bdbe0374219400b58068dca84b14d4aa19299d1b804a17642f62536b0272a920844b170489a4b91020b3248529ce8943c4fd123e315575656a14b6b3bc8e02c160307ac904572ff4920c3622ac30a916f36ae162b0172703d443b7eec583411389939a7f5c6147614240d6f03e9e2cc44e18782e7036d907a25477cc7046895c70b5dd181c57b4a04a3c2f489852383c4594d334ac487c276a9bf2027667472c22246c4166a3fa161da1836b7fec45d009a64efb904bea46d594463b5327b5c2b33091243c92a37fa978141b62161801eab210aa62a5f83871a5c2623d3565ac088f816a1165931b16d98d21427d666557e6ea823e2c1fcb455a2caa5d61ca80decb61658877bc707b6e1c2bac7c28749788e4597c8aa464f595b318124737906a364244c1d85a573029c32a0d59d6689c57632848c3d9180064115d9a710f9cc06d964699194623e04b97c769b51da53979f722b89160c99040c96c2307714face22602538d95250a64965717197315d84ea3284325d48e18ca078b50241ee653a62a75828606f99289d242bd7652b65a4a5d85025053e4c4d6a8c662d9c998608ceb750e0699cfe0f398b8183401f8699d2445ed62bedac4b5eb29825d275b328cb531e4b1c13c14342592bc40cfc9d5664f9453a66520aab2a93a5663a5cc59f4a554dfe7a2b98a5cb516170fcc858bb63e55d444e1335ccf73b67c4280be0b488e535858d1ae6ed60cbdcb6166fc0c0fd1005840ba1440ba4c5a4064e4cec9c21b88f930f467647e8879edd13076e793138905a280ac9478815f963a7348c4074b3e87461e44dabac8fb0eafa01d41eac8dfbb9334931be0e3394d2839913c2fe054190c4ab8fc4710b867334c478cfba772d37328cb511a8c88bbd5317d7d268d6a24715f59b898fb59e6757c0e60a41b9bc6e0562bff735708fc64d0b20b77015a0d338ffd79b7ef49a60177b2af766bd152b0e3619e86f030c9653ad15b78c0949a8b24bb3944092825439ee467c236a3a840c8772c1a4fc93ab2b721442a86b5d94a75b66f162a637acb5d893952e3564acb99caf260c355f422b58a364fac00d10bbb4a2c481431b844007cbe50ce08cb446369946ef3ac365c81d171220a59cb699ac59015bea6883e48e9cc3c0088bc6022fd5c749188c665c1618497232745aae54b81bd967571b68c47e5113260cc178212c8112a91abb570b8b4992a0a9032925c28a1e3b78e11c23c4e5b723f3c11f0826f11f41b37662ac644bd504287d032522a082c4ddb237053113e7609cb485f512c97075696aa00b45e60ab07548f76161c06167c1a653a1e45623c5c2f48927009631bca5a5e626c357e553e30e97aa75641c1fc29fb27597a5b37d0827e753c17bb22b1f8286fec18b94de07692e8618dfa55ff621be659992b6660fa269a9b53bfbc1658e7b10fe2115b3d3214afeca84cbb2852c428dd7386cc17847e1011c2e59c2697ac14e97898c0ca5ae71195f93e002794c6993cb8483de6c85c222185c9c2184f1497bac1556ec9752335027ba6c33d973852e588cd0c2e34f603765098ff252a81f01fa08b72c4e36d61958d090cc34d65cb582a49e50a60646609f1478621d44ffb3874fe8606c47188010842e0a46748b692ae7271f6da93098ab062e5981a890e6a616fe527853b4952cfe60118690e4d4b56dd73095b8b2076a03ed148af0e90c0a060c76c82627f68365a0c94f3ec2a9e019206519e18cb495c445519539d1ff67f0d8c81ec6055124364b57824a83c974acab226d0a299967fbbf41027b865971c963d6c2bf6ca107a051ce3e83fd4d06ee841bfdeea1a967a86d9571fb33c559e53bf5ff93553364af68a848e82bfa52293f64cb2bff0282f46b369786675592377e95480444cc0ecccfeb3152c9a6ab4a55b60c806dc0567d7ba617746557b72c47cdc43e0689a6e5a9afa957c0823c76b54207231479b25a9bccc54fef61007e1c9bd116904f0285d0a93c5693e03b05e16f477f8866e2431b525d5b93d212c643b30ccfc94d2b2469477991e07b10e282b2bb035c93ac4839b60ab58539674bf3fd523576a45dbe1809fd2238cd975f0c031e21456c160799be93c69d233a15b7d59e177aca13502a4536c420054f14687dc25f2eb2b9274c1ef6773c4e94a9532b9a106bdc63aaa1ed2ad929042b298bda44325f629b5537bc5e18387bd0ba2dab75eb0514fbaba5bf6aa1400a63172359da6ba6dd0c83d56214100f892a42c779e4408aa204ad03a3e492611290a812861912249c5bdf2bd7354526f768ca79b52abf5bc2f99af2e0754ff6a28c6c0a92eda5219658da88791e31ca84a81be805b23724c521085a165e77fbd30b3e51a587b91abbfd8b94045b9028142ff8b9b5cda6c5f44105b446c22873b24095395eb61bc417398b290aac55e3e75717e5651c5aa38ebc3a44317ae89770a37c991b7547401a7c3c6a69fde5234c7f10c426785d2073f15d4ae988889a8a2620d2569269745b86a407c0b454eeb4562e2ab43ba1fdd03931c04b480c96a3b0581a6ca8413681632478c61998663003acfb04c56b74e4aa05adb2c6745f6343dcc55fec803f5acba6125bc993c9349994989e6171d8873a7c25edd15cf62fcbe64b0b504c405b905c2efb1246732524567739622500c954791b40f02050a8133bb70f545c3a833f287af846101f1013f38f8a73de03a5c04d063528111dacb29dc16bebc474f6a856b88798ff61aa94b068d5a93ac9b3aa7c741c5bba8b6395483c6a1bd6803e0754d1f304674648fce7268fb4166294b50d37413ea4561a4c66a561a71d780a9db9369868c839765af65d89fb62c97b341754900b3b886736eb3035bf27666c019708027e16329559a3047494c74376271573c3d224c7de69b5811ad8fbc684bebc28bc490a83842bc630851095ef140c9bed924342941dbf48687e7c6c50c55d051852f9c5ccac4784ae95cf7aa34c549b468263c19752d20a1867f77c4a01b546312bcdbe54ef2e541cbc658f2fc07714c42f2db6d6eb5a3213bc60ce4be28d1a39372a68e95579ae61a3351a655f18fc9b31cc04562c656910a6ab46e22ac57116cb2f155a90805ca1277813946ee76ae1e5221ddda1ac142abcaeb4c05c58b797705003499adca397c15ca7266284cab44b5d944ca73b4d7f21400b744a3208856a7a8f402192172a0ba30274067ad688b98e1017ee4a90cc237122f61513f80a1810a1ddcb8c4ed73a88af52cafe516dc20946276ca8aeb06d6036c436684e0181142f04d33a23620aa7bb133642404c20aa816373149b0f049c8f1150ab111337306cceac9574479d683bec59389a741227bc0976e025b8f76af1928207bda56c890a13b02471f041954266820b454347cbe18ea8923d6261a96bf14688048a5aa75a13db1d80649454b75734d7eb212ebc35333c4a728314bb81bbabc24845a631ad5ecc1fb778d8d2ab497f3933f09833fd0bc85a2b7157c1dfc1325c8a988995b95229b4291e9105fc161fe146c143687b2d58c56118531d92156e75e80ea440a347aa0e10ca2cc8510386a904b01d4d155d2abc05be3852f15064e4c7eb4a34b1e183c20486c05999eaecc6508038cc0e853689195f9954ae35b6d4a31a087fc087b643aa3fb29c77b9e247424db1c203b29abec8a9a50898555c392ff133bfae9b282068d73cacff62687e4b40584932907b18f965c02ffa51c83159049a8269d008b5c15c863d10394275725b901f92281f9522f3fca9ed6d29ef4e80d970ca948564b9c803b18630c6dfccb44b0804f863f803a580e85098f68c6dfb9423942185b2827f4e1c56f9151fcb41283185eab0348fe0283e5f21678906b4c6365ad688aa44146664a8bdc9824a05a99a0a625b56415a0a7464bbc41d591274fd12647d51570f2a984e7bc2e4907641260d836c4b8bac993aa0512308270ea7a2d45b0d098cb8a4b15758098cd87316e95680b297fe562477f3ab80a507c479a3ac8fc5dd743bdd4db02ea36128bf22fd4abcedb1ba03a24127d64b2b8eb94462330eb72c36daa6155a238ba300a89427b0f818b5d8c78a9288a4f627178ec1c72c7bb971b4868d0120004b169fac7a0f537b935cd99fca207812223205a6f432d888797070a44f568e712cae959d0aa92301080b94cb55bddc0dc620c5a931e184809b91d5216c5934d931131da261bb3d841a27a8a52cc7577d288e741fd4e5e0629894b5e8733d95aa7023570008b31fa4ac8ca8b6e3906327b3880ab6dd284",

    "address": "7ZuJPKinFgDDhyRXEVeWihdApvVvvGBKf"
}

Potential Enhancements
Key Backup and Recovery:
Provide a secure way for users to back up and recover their keys, especially for deterministic keys generated with a password.
Audit Logging:
Log key generation events to detect potential misuse or unauthorized access.
Salting Passwords:
Use a unique salt for each password before hashing to improve resistance against precomputed attacks.

Dependencies
Python Libraries:

Flask: Web framework.
ecdsa: For ECDSA key generation and signing.
kyber: For quantum-resistant cryptography.
base58: For encoding blockchain addresses.
hashlib: For hashing and proof-of-work.

Frontend:

HTML and JavaScript (jQuery).
How to Run
Install Dependencies:

pip install flask ecdsa kyber base58

Start the Flask Server:

python app.py
Access the Application: Open a browser and navigate to http://localhost:5000.

Notes
This application is a proof of concept and not intended for production use.
Ensure that kyber is installed and configured properly.
Mining rewards are hardcoded as 10 units.
Passwords are hashed using sha3_256 for security.