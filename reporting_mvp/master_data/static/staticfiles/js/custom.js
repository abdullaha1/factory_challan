
const hostName = 'http:localhost:8000';


function ajaxCall(url,method,dataType,success=null,error=null){
      $.ajax({
                url: 'http://localhost:8000/backend/'+url,
                method: method,
                dataType:dataType,
                success:success,
                error:error
      });
}

function ajaxCallPost(url,method,dataType,data,success=null,error=null){

      $.ajax({
                url: 'http://localhost:8000/backend/'+url,
                method: method,
                dataType:dataType,
                data:data,
                contentType:"application/json; charset=utf-8",
                beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                 }
                },
                success:success,
                error:error
      });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}



function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


