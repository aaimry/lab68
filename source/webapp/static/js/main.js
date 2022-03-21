async function makeRequest(url, method = 'GET') {
    let response = await fetch(url, {method});

    if (response.ok) {
        return await response.json();
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}

async function onLike(event) {
    event.preventDefault();
    let likeBtn = event.target;
    let url = likeBtn.href;

    try {
        let response = await makeRequest(url);
        let unLikeBtn = document.getElementById(`${likeBtn.id}`)
        const like_count = document.getElementById(`counter${likeBtn.id}`);
        like_count.innerText = response.likes;
        likeBtn.hidden = true;
        unLikeBtn.hidden = false;

    } catch (error) {
        console.log(error);
    }
}


async function onUnlike(event) {
    event.preventDefault();
    let unlikeBtn = event.target;
    let url = unlikeBtn.href;

    try {
        let response = await makeRequest(url);
        let likeBtn = document.getElementById(`${unlikeBtn.id}`)
        const like_count = document.getElementById(`counter${unlikeBtn.id}`);
        like_count.innerText = response.likes;
        unlikeBtn.hidden = true;
        likeBtn.hidden = false;
    } catch (error) {
        console.log(error);
    }
}


window.addEventListener('load', function () {
    const likeButtons = document.getElementsByClassName('like');
    const unlikeButtons = document.getElementsByClassName('unlike');
    let counters = document.getElementsByClassName('like_count');

    for (let btn in likeButtons) {
        likeButtons[btn].onclick = onLike;
        likeButtons[btn].id = `${btn}`;
        counters[btn].id = `counter${btn}`;
        unlikeButtons[btn].onclick = onUnlike;
        unlikeButtons[btn].id = `${btn}`;
    }
});
