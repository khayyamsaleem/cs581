const fs = require('fs');
const readline = require('readline');
const {google} = require('googleapis');
const OAuth2 = google.auth.OAuth2;
const prompt = require('prompt')
const SCOPES = [
    'https://www.googleapis.com/auth/youtubepartner',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
];
const TOKEN_DIR = (process.env.HOME || process.env.HOMEPATH ||
    process.env.USERPROFILE) + '/.credentials/';
const TOKEN_PATH = TOKEN_DIR + 'cs581-a3-youtube-nodejs.json';
const util = require('util')

fs.readFile('client_secret.json', function processClientSecrets(err, content) {
    if (err) {
        console.log('Error loading client secret file: ' + err);
        return;
    }
    authorize(JSON.parse(content), search);
});

function authorize(credentials, callback) {
    var clientSecret = credentials.installed.client_secret;
    var clientId = credentials.installed.client_id;
    var redirectUrl = credentials.installed.redirect_uris[0];
    var oauth2Client = new OAuth2(clientId, clientSecret, redirectUrl);

    // Check if we have previously stored a token.
    fs.readFile(TOKEN_PATH, function(err, token) {
        if (err) {
            getNewToken(oauth2Client, callback);
        } else {
            oauth2Client.credentials = JSON.parse(token);
            callback(oauth2Client);
        }
    });
}

function getNewToken(oauth2Client, callback) {
    var authUrl = oauth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: SCOPES
    });
    console.log('Authorize this app by visiting this url: ', authUrl);
    var rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    rl.question('Enter the code from that page here: ', function(code) {
        rl.close();
        oauth2Client.getToken(code, function(err, token) {
            if (err) {
                console.log('Error while trying to retrieve access token', err);
                return;
            }
            oauth2Client.credentials = token;
            storeToken(token);
            callback(oauth2Client);
        });
    });
}

function storeToken(token) {
    try {
        fs.mkdirSync(TOKEN_DIR);
    } catch (err) {
        if (err.code != 'EEXIST') {
            throw err;
        }
    }
    fs.writeFile(TOKEN_PATH, JSON.stringify(token), (err) => {
        if (err) throw err;
        console.log('Token stored to ' + TOKEN_PATH);
    });
    console.log('Token stored to ' + TOKEN_PATH);
}

async function search(auth) {
    var service = google.youtube('v3')
    prompt.start()
    prompt.get(['search_string', 'max_results'], (err, res) => {
        if (err) {
            console.log(err)
            return
        }
        service.search.list({
            auth: auth,
            part: 'id,snippet',
            maxResults: res.max_results || 25,
            q: res.search_string || 'cheese'
        }, async function(err, response) {
            if (err) {
                console.log('The API returned an error: ' + err);
                return;
            }
            //console.log(util.inspect(response.data.items, false, null, true))
            let stats = await Promise.all(response.data.items.map(async (obj) => {
                return await service.videos.list({
                    'auth':auth,
                    'part':'id,snippet,statistics,topicDetails',
                    'id': obj.id.videoId
                })
            }))
            const out = stats.map(statObj => ({
                "searchQuery": res.search_string,
                "id": statObj.data.items[0].id,
                "title": statObj.data.items[0].snippet.title,
                "stats": statObj.data.items[0].statistics,
                "topicCategories": statObj.data.items[0].topicDetails.topicCategories.map(link => link.slice(30))
            }))
            console.log(out)
            let topic_freqs = {}
            let flat_topics = out.map(o => o.topicCategories).reduce((acc, val) => acc.concat(val), [])
            for(let o of flat_topics){
                if (topic_freqs[o])
                    topic_freqs[o] += 1
                else
                    topic_freqs[o] = 1
            }
            console.log(topic_freqs)
        });
    })
}

