const searchForm = document.querySelector('#search-form');
const searchInput = document.querySelector('#search-input');
const searchResult = document.querySelector('#search-result');

const API_URL = 'https://alpes-transport-sandbox.wikibase.cloud/w/api.php';
const API_TOKEN = "add708d9d5efa211ffbdca82d5ee115363ff81a7+\\"//'a1e85833b3f6939d490d08ee38b5a4cfafb4c0c3';

const endpoint = "https://alpes-transport-sandbox.wikibase.cloud/w/api.php"
const username = "william"
const password = "william-bot@88hd7lft423pdnt5f95ijnoq8lccliae"

// CONNECTION
var request = require( 'request' ).defaults( { jar: true } ),
	url = endpoint;

// Step 1: GET request to fetch login token
function getLoginToken() {
	var params = {
		action: 'query',
		meta: 'tokens',
		type: 'login',
		format: 'json'
	};

	request.get( { url: url, qs: params }, function ( error, res, body ) {
		var data;
		if ( error ) {
			return;
		}
		data = JSON.parse( body );
		loginRequest( data.query.tokens.logintoken );
	} );
}

// Step 2: POST request to log in.
// Use of main account for login is not
// supported. Obtain credentials via Special:BotPasswords
// (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
function loginRequest( loginToken ) {
	var params = {
		action: 'login',
		lgname: username,
    lgpassword: password,
		lgtoken: loginToken,
		format: 'json'
	};

	request.post( { url: url, form: params }, function ( error, res, body ) {
		if ( error ) {
			return;
		}
		console.log( body );
	} );
}

// Start From Step 1
getLoginToken();





searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const searchValue = searchInput.value.trim();
  searchFeed(searchValue);
});

function searchFeed(searchValue) {
  searchResult.innerHTML = '';
  const url = `${API_URL}?action=wbsearchentities&language=fr&format=json&search=${searchValue}`;
  fetch(url, {
    headers: {
      //'Authorization': `Token ${API_TOKEN}`,
      //'Access-Control-Allow-Origin': '*',
      //'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      credentials: 'include',
    }
  })
    .then(response => response.json())
    .then(data => {
      const results = data.items;
      if (results.length) {
        results.forEach(result => {
          const li = document.createElement('li');
          li.innerHTML = `
            <div class="result-info">
              <h3>${result.title}</h3>
              <p>${result.description}</p>
            </div>
            <a href="${result.link}" target="_blank">Voir sur le site</a>
          `;
          searchResult.appendChild(li);
        });
      } else {
        searchResult.innerHTML = '<li>Aucun résultat trouvé</li>';
      }
    })
    .catch(error => console.error(error));
}



// Get a login token:
// token_response = fetch("https://alpes-transport-sandbox.wikibase.cloud/w/api.php?action=query&meta=tokens&origin=*")
// token_response.then(
//   console.log(token_response)
// )