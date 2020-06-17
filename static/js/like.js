'use strict';

function like(type, pk) {
    $.ajax({
        url : "/AskMe/js/" + type +"/" + pk + "/like/",
        type : 'POST',
        data : { 'obj' : pk },
        success : function (json) {
            document.getElementById("rating_"+pk).innerText = json.rating;
            var image_like = document.getElementById("like_img_"+pk);
            var image_dislike = document.getElementById("dislike_img_"+pk);
            if (json.result)
            {
                image_like.src = '/static/img/like_active.png';
                image_dislike.src = '/static/img/dislike.png';
            }
            else
            {
                image_like.src = '/static/img/like.png';
            }
            //like.find("[data-count='like']").text(json.like_count);
            //dislike.find("[data-count='dislike']").text(json.dislike_count);
        }
    });
    return false;
}

function dislike(type, pk) {
    $.ajax({
        url: "/AskMe/js/" + type + "/" + pk + "/dislike/",
        type: 'POST',
        data: {'obj': pk},

        success: function (json) {
            document.getElementById("rating_"+pk).innerText = json.rating;
            //like.find("[data-count='like']").text(json.like_count);
            //dislike.find("[data-count='dislike']").text(json.dislike_count);
            var image_like = document.getElementById("like_img_"+pk);
            var image_dislike = document.getElementById("dislike_img_"+pk);
            if (json.result)
            {
                image_dislike.src = '/static/img/dislike_active.png';
                image_like.src = '/static/img/like.png';
            }
            else
            {
                image_dislike.src = '/static/img/dislike.png';
            }
        }
    });

    return false;
}


function correct(pk) {
    $.ajax({
        url : "/AskMe/js/answer/" + pk + "/correct/",
        type : 'POST',
        data : { 'obj' : pk },
        success : function (json) {
            if (json.prev_answer_id !== -1) {
                document.getElementById(json.prev_answer_id).checked = false;
            }
        }
    });
    return false;
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Настройка токена
$(function () {
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});

// Подключение обработчиков
// $(function() {
//     $('[data-action="like"]').click(like);
//     $('[data-action="dislike"]').click(dislike);
// });