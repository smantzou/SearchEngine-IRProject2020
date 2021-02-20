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
    feedbackArray = new Array(index)
    for(i=0;i<index;i++){
        btn = document.getElementById(i+1)
        if(btn.classList.contains('active')){
            feedbackArray[i] = 1
        }
        else{
            feedbackArray[i] = 0
        }
    }
    console.log(feedbackArray)
    eel.receiveFeedback(feedbackArray)
}

eel.expose(receiveResults)
function receiveResults(results) {
    k = Object.keys(results).length
    while (resultsContainer.firstChild) {
        resultsContainer.removeChild(resultsContainer.firstChild)
    }
    for (let i = 1; i <= k; i++) {
        const newRow = document.createElement('div')
        const newTitle = document.createElement('div')
        const newDescription = document.createElement('div')
        const newLikeButton = document.createElement('button')

        newRow.classList.add = "container-fluid"

        const aTag = document.createElement('a')
        aTag.innerHTML = "This is where the title should be"

        aTag.href = results[i]
        aTag.target = "_blank"
        const aSpan = document.createElement('span')
        aSpan.innerHTML = "This is where the description should be"

        newLikeButton.innerHTML = '&#10003;'
        newLikeButton.id = i
        newLikeButton.addEventListener("click",toggle)

        newTitle.appendChild(aTag)
        newDescription.appendChild(aSpan)
        newRow.appendChild(newTitle)
        newRow.appendChild(newDescription)
        newRow.appendChild(newLikeButton)


        resultsContainer.appendChild(newRow)

    }
}










