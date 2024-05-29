Files for a simple encryption project

Notes about the Files
1. message-mixer.js
The file contains logic for running the encryption methods -> caesarCipher, symbolCipher, and reverseCipher.
caesarCipher: in which the characters of the input message are shifted alphabetically by a given amount.
symbolCipher: in which select characters from the input message are replaced with visually similar symbols.
reverseCipher: in which each word of the input message is reversed in place.

2. encryptors.js
Contains logic for each of the Cipher functions.

3. super-encoder.js
Shorthand encoder and decoder which use the Cipher functions.
Encodes in pre-defined order using a string and performing caesarCipher first, then reverseCipher, and finally symbolCipher on it.
It also can decode the encrypted word using the opposite of the above algorithm.