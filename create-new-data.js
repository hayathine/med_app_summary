const fs = require('fs');
const path = require('path');

const body = process.argv[2];
const id = process.argv[3];

const fileName = `add-new-data-${id}.txt`;
const filePath = path.join('assets', fileName); // assetsフォルダへのパス
fs.writeFileSync(filePath, body);
