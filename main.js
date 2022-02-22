require('dotenv').config()

function readFile(filename) {
    const fs = require('fs');
    const content = fs.readFileSync(filename, 'utf8');
    return content;
}

async function runQuery(query) {
    const { got } = await import('got')

    try {
        const { body } = await got.post('https://api.github.com/graphql', {
            headers: {
                'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
                'Content-Type': 'application/json',
            },
            json: { query },
        })
        return body
    } catch (error) {
        console.error(error.message);
    }
}

const query = readFile('graphql_tag_query.txt');
runQuery(query).then((response) => console.log(response));
