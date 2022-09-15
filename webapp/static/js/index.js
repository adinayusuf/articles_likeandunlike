document.querySelectorAll('.like-form')
    .forEach(el => el.addEventListener("submit", likeArticle));


function likeArticle(e) {
    e.preventDefault();
    let url = e.target.action;
    let headers = new Headers();
    headers.append("X-CSRFToken", e.target.elements.csrfmiddlewaretoken.value);
    fetch(url, {"method": e.target.dataset.method, "headers": headers})
        .then(res => res.json())
        .then(res => {
            updateUI(res, e.target)
            let url = e.target.action;
            if (res.action === 'like') {
                url = `/article/${res.pk}/unlike/`;
                e.target.dataset.method = "DELETE";

            } else {
                url = `/article/${res.pk}/like/`;
                e.target.dataset.method = "POST";
            }
            e.target.action = url;
        })
        .catch(function (err) {
            console.warn('Something went wrong.', err);
        });
}


function updateUI(data, el) {

    let countDiv = el.querySelector('.like-counter');
    countDiv.innerText = data.count;
    let likeBtn = el.querySelector('.like-btn');
    if (data.action === "like") {
        likeBtn.innerText = "Unlike";
        likeBtn.classList.remove("btn-outline-danger");
        likeBtn.classList.add("btn-danger");

    } else {
        likeBtn.innerText = "Like";
        likeBtn.classList.remove("btn-danger");
        likeBtn.classList.add("btn-outline-danger");
    }


}