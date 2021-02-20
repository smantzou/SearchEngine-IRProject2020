const queryInput = document.getElementById('queryInput')
const queryButton = document.getElementById('queryButton')
const resultsContainer = document.getElementById('resultsContainer')
const feedbackButton = document.getElementById('feedbackButton')
feedbackButton.addEventListener('click',sendFeedback)
queryButton.addEventListener("click", getQuery)
var query = ''

var numbers = document.getElementById('box')

for (i = 1; i < 100; i++) {
    var span = document.createElement('span')
    span.textContent = i;
    numbers.appendChild(span)
}
var num = numbers.getElementsByTagName('span')
var index = 0;

function nextNum() {
    num[index].style.display = 'none';
    index = (index + 1) % num.length;
    num[index].style.display = 'initial';
}
function prevNum() {
    num[index].style.display = 'none';
    index = (index - 1 + num.length) % num.length;
    num[index].style.display = 'initial';
}
function getIndex() {
    return index
}

function getQuery() {
    query = queryInput.value
    let index = getIndex()
    if (index != 0) {
        eel.getQueryInfo(index, query)
    }

}
function toggle(){
    let btn = document.getElementById(event.target.id)
    console.log(btn.id)
    if(btn.classList.contains('active')){
        btn.classList.remove('active')
        btn.classList.add('inactive')
    }
    else{
        if(btn.classList.contains('inactive')){
            btn.classList.remove('inactive')
        }
        btn.classList.add('active')
    }
    
}

function sendFeedback(){
    feedbackDict = []
    for(i=1;i<=index;i++){
        let btn = document.getElementById(i)
        let tag = document.getElementById(i+100)
        if(btn.classList.contains('active')){
            feedbackDict.push({
                key : tag.href,
                value : 1
            })
        }
        else{
           feedbackDict.push({
                key : tag.href,
                value : 0 
           })
        }
    }
    console.log(feedbackDict)
    eel.receiveFeedback(feedbackDict)
}

eel.expose(receiveResults)
function receiveResults(results,titles,query_time) {
    const time_span = document.getElementById('timeSpan')
    time_span.innerHTML = ''
    k = Object.keys(results).length
    while (resultsContainer.firstChild) {
        resultsContainer.removeChild(resultsContainer.firstChild)
    }
    for (let i = 1; i <= k; i++) {
        const newRow = document.createElement('div')
        const newTitle = document.createElement('div')
        const newLikeButton = document.createElement('button')

        newRow.classList.add = "container-fluid"

        const aTag = document.createElement('a')
        aTag.innerHTML = titles[i]

        aTag.href = results[i]
        aTag.id = i+100
        aTag.target = "_blank"
        

        newLikeButton.innerHTML = '&#10003;'
        newLikeButton.id = i
        newLikeButton.addEventListener("click",toggle)

        newTitle.appendChild(aTag)
        newRow.appendChild(newTitle)
        newRow.appendChild(newLikeButton)


        resultsContainer.appendChild(newRow)

        
    }
    
    time_span.innerHTML = 'This query took: '
    time_span.innerHTML = time_span.innerHTML.concat(String(query_time)+ " seconds")
    time_span.style.removeProperty('display')
    time_span.style.display = 'initial'

}










