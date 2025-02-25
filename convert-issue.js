const fs = require('fs');
const path = require('path');

console.log("issueJson:", process.argv[2]);
console.log( 'typeof ' + (typeof issueJson) );
const commentBody = process.argv;
console.log("commentBody:", commentBody);
console.log( 'typeof ' + (typeof commentBody) );
const unescapedBody = commentBody.replace(/\\\\/g, '\\');

try {
    const commentData = {
        body: JSON.parse(unescapedBody),
    };

} catch (error) {
    console.error("JSON parse error:", error);
    // エラー処理
    process.exit(1);
}
console.log("commentData:", commentData);

const commentJson = JSON.stringify(commentData, null, 2);
const fileName = `comment-${Date.now()}.json`;
const filePath = path.join('assets', fileName); // assetsフォルダへのパス

fs.writeFileSync(filePath, commentJson);
