const fs = require('fs');
const path = require('path');

const urlPattern = /^(https?:\/\/)?([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})(:[0-9]{1,5})?(\/.*)?$/;
const body = process.argv[2].split('\n');
console.log(body);
const id = process.argv[3];
console.log(id);
const name = body[0].match(/name : '(.*)'/)[0];
const url = body[1].match(/url : '(.*)'/)[0];
// name のバリデーション
if (name.length > 100) {
    console.error("Error: name must be 100 characters or less.");
    process.exit(1);
}
const arr = [name, url];
console.log(url);
// url のバリデーション
if (!urlPattern.test(url) || url.length > 200) {
    console.error("Error: url must be a valid http(s) URL and 200 characters or less.");
    process.exit(1);
}

const fileName = `add-new-data-${id}.txt`;
const filePath = path.join('assets', fileName); // assetsフォルダへのパス
const str = JSON.stringify(arr);
fs.writeFileSync(filePath, str);
