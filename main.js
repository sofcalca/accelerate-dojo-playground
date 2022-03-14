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

function parse_response_for_tags(response) {
    console.error('not implemented yet');
}

function parse_response_for_commits(response){
    console.error('not implemented yet');
}

function compute_deployment_frequency() {
    console.error('not implemented yet');
}

function compute_change_failure_rate() {
    console.error('not implemented yet');
}

function compute_mean_time_to_repair() {
    console.error('not implemented yet');
}

function compute_lead_time() {
    console.error('not implemented yet');
}

async function main() {
    const tagsQuery = readFile('graphql_tag_query.txt');
    const tagsResponse = await runQuery(tagsQuery);
    console.log(tagsResponse);

    const commitsQuery = readFile('graphql_commits_query.txt');
    const commitsResponse = await runQuery(commitsQuery);
    console.log(commitsResponse);
}

main()
