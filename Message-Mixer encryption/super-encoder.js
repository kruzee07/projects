// Import the encryptors functions here.
const encryptors = require('./encryptors')

const {caesarCipher, symbolCipher, reverseCipher} = encryptors;
///////

const encodeMessage = (str) => {
  // Use the encryptor functions here.
  return symbolCipher(reverseCipher(caesarCipher(str, 26)));
}

const decodeMessage = (str) => {
  // Use the encryptor functions here.
  return caesarCipher(reverseCipher(symbolCipher(str)), -26);
}

// User input / output.

const handleInput = (userInput) => {
  const str = userInput.toString().trim();
  let output;
  if (process.argv[2] === 'encode') {
    output = encodeMessage(str);
  } 
  if (process.argv[2] === 'decode') {
    output = decodeMessage(str);
  } 
  
  process.stdout.write(output + '\n');
  process.exit();
}

// Run the program.
process.stdout.write('Enter the message you would like to encrypt...\n> ');
process.stdin.on('data', handleInput);
