
let maxArrayLength = 20;

// Given an array of URLs, build a DOM list of those URLs in the
// browser action popup.
function buildPopupDom(divName, data) {
  maxArrayLength = data.length > maxArrayLength ? maxArrayLength : data.length;
  data = data.slice(0,maxArrayLength);
  console.log(data);
  var links = data;
  var request_json = { "request_links": links };
  const xhr = new XMLHttpRequest();
  const url = 'http://127.0.0.1:5000/recommendation';
  xhr.open("POST", url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify({
    value: request_json
  }));

  xhr.onload = function () {
    console.log(this.status);
    var data = JSON.parse(this.responseText);
    console.log(data);
    var response = data;
    var mainContainer = document.getElementById("myData");

    var ul = document.createElement('ul');
    mainContainer.appendChild(ul);
    for (var key in response) {
      var result = key + ' : ' + response[key];
      console.log(key);
      console.log(response[key]);
  
      var li = document.createElement('li');
      li.innerHTML = result;
      ul.appendChild(li);
    }

  };

  // var response = { 'City': ['Isa Town', 'Dora', 'Tirat Carmel'], 'Board Game': ['Games played with Mahjong equipment', 'Tiger game', 'tafl games'], 'Building': ['Lindenstraße 62', 'Werderstraße 157', 'Südstraße 80 und 82'], 'Musical Work': ['Earth Dances', 'The Creation structure', 'Four Last Songs'], 'Anime': ['Jankenman', 'Nekomonogatari', 'Akū Daisakusen Srungle'] };

  // // console.log(msg);
  // var mainContainer = document.getElementById("myData");

  // var ul = document.createElement('ul');
  // mainContainer.appendChild(ul);
  // for (var key in response) {
  //   var result = key + ' : ' + response[key];
  //   console.log(key);
  //   console.log(response[key]);

  //   var li = document.createElement('li');
  //   li.innerHTML = result;
  //   ul.appendChild(li);
  // }
}

// Search history to find up to ten links that a user has typed in,
// and show those links in a popup.
function buildTypedUrlList(divName) {
  // To look for history items visited in the last week,
  // subtract a week of microseconds from the current time.
  var microsecondsPerWeek = 1000 * 60 * 60 * 24 * 7;
  var oneWeekAgo = (new Date).getTime() - microsecondsPerWeek;

  // Track the number of callbacks from chrome.history.getVisits()
  // that we expect to get.  When it reaches zero, we have all results.
  var numRequestsOutstanding = 0;

  chrome.history.search({
    'text': '',              // Return every history item....
    'startTime': oneWeekAgo  // that was accessed less than one week ago.
  },
    function (historyItems) {
      // For each history item, get details on all visits.
      for (var i = 0; i < historyItems.length; ++i) {
        var url = historyItems[i].url;
        var processVisitsWithUrl = function (url) {
          // We need the url of the visited item to process the visit.
          // Use a closure to bind the  url into the callback's args.
          return function (visitItems) {
            processVisits(url, visitItems);
          };
        };
        chrome.history.getVisits({ url: url }, processVisitsWithUrl(url));
        numRequestsOutstanding++;
      }
      if (!numRequestsOutstanding) {
        onAllVisitsProcessed();
      }
    });


  // Maps URLs to a count of the number of times the user typed that URL into
  // the omnibox.
  var urlToCount = {};

  // Callback for chrome.history.getVisits().  Counts the number of
  // times a user visited a URL by typing the address.
  var processVisits = function (url, visitItems) {
    for (var i = 0, ie = visitItems.length; i < ie; ++i) {
      // Ignore items unless the user typed the URL.
      // if (visitItems[i].transition != 'typed') {
      //   continue;
      // }

      if (!urlToCount[url]) {
        urlToCount[url] = 0;
      }

      urlToCount[url]++;
    }

    // If this is the final outstanding call to processVisits(),
    // then we have the final results.  Use them to build the list
    // of URLs to show in the popup.
    if (!--numRequestsOutstanding) {
      onAllVisitsProcessed();
    }
  };

  // This function is called when we have the final list of URls to display.
  var onAllVisitsProcessed = function () {
    // Get the top scorring urls.
    urlArray = [];
    for (var url in urlToCount) {
      urlArray.push(url);
    }

    // Sort the URLs by the number of times the user typed them.
    urlArray.sort(function (a, b) {
      return urlToCount[b] - urlToCount[a];
    });

    buildPopupDom(divName, urlArray);
  };
}

// document.addEventListener('DOMContentLoaded', function () {
//   buildTypedUrlList("typedUrl_div");
// });

// 1. Create the button
var button = document.createElement("button");
button.innerHTML = "Fetch Recommendations";

// 2. Append somewhere
var body = document.getElementsByTagName("body")[0];
body.appendChild(button);

// 3. Add event handler
button.addEventListener("click", function () {
  // alert("did something");
  button.style.display = 'none';
  buildTypedUrlList("typedUrl_div");
});


