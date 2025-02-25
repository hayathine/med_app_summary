const fs = require('fs');
const path = require('path');

console.log("issueJson:", process.argv); 
const issueJson = JSON.parse(process.argv);
const fileName = `issue-${issueJson.number}.json`;
const filePath = path.join('assets', fileName); // assetsフォルダへのパス

fs.writeFileSync(filePath, JSON.stringify(issueJson, null, 2));