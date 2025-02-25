const fs = require('fs');
const path = require('path');


console.log("issueJson:", process.argv[2]);
console.log('typeof ' + (typeof issueJson));
const body = process.argv[2];
const id = process.argv[2];

const fileName = `add-new-data-${id}.txt`;
const filePath = path.join('assets', fileName); // assetsフォルダへのパス
console(process.argv);
fs.writeFileSync(filePath, body);
