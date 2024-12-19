if (localStorage.getItem("quizarray") === null) {
    localStorage.setItem("quizarray", JSON.stringify([]));
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

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$('#quizdetail').click(function () {
  
        var quizarray = JSON.parse(localStorage.getItem("quizarray"));
    var csrftoken = getCookie('csrftoken');
    var lim =quizarray.length;
    if(lim!=0)
    {
    $.ajax({
        type: "POST",
        contentType: "application/json",
        url : "/quizdetail/",
        data : JSON.stringify(quizarray),
        dataType: "json",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) { 
            
            var test_id = $("#test_id").attr("value");
            
            var str1 = "/daily_mcq_answer/";
            var str2 = test_id;
            var res = str1.concat(str2);
            localStorage.clear();
            location.href=res;
  
        }
        }); 
    }
    else{
        alert('No Questions Answered!!!');
    }

    
    
});



$('.clear_option').click(function(){
    event.preventDefault();
    ques_id = $(this).attr('ques_no');

    valueid = $('#ques_window input[question=' + ques_id +']:checked').attr('value');
    radios = $('#ques_window input[question=' + ques_id +']:checked').prop('checked', false);
    
    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
    var lim = quizarray.length;
    
    for (var i = 0; i < lim; i++) {
            
            if ( quizarray[i].valueid == valueid){
                $("a[questionid="+ quizarray[i].questionid +"]").css({"background":"#FFFFFF"});
                quizarray.splice(i, 1);
            }
    }
    localStorage.setItem("quizarray", JSON.stringify(quizarray));

  });


$('input:radio').click(function () {

    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
   
    var lim = quizarray.length;

    var flag = 0;
  
        for (var i = 0; i < lim; i++) {
            if ( quizarray[i].valueid == $(this).attr("value")){
                flag=1;
                break;
            }
            if (quizarray[i].questionid == $(this).attr("question")) {
                $('input:radio[value=' + quizarray[i].valueid + ']').prop('checked', false);
                quizarray[i].optionid = $(this).attr("option");
                quizarray[i].valueid = $(this).attr("value");
                flag = 1;
                break;
            }
    
        }
    
    

    if (flag == 0 ) {
        
        quizarray.push({
            testid: $(this).attr("test"),            
            questionid: $(this).attr("question"),
            optionid: $(this).attr("option"),
            valueid: $(this).attr("value"),
        });


    }
    localStorage.setItem("quizarray", JSON.stringify(quizarray));   
   



});



$('input:checkbox').click(function () {
    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
     var lim = quizarray.length;
 
     var flag = 0;
   
         for (var i = 0; i < lim; i++) {
             if ( quizarray[i].valueid == $(this).attr("value")){
                 flag=1;
                 break;
             }
     
     
         }
     
     if ( flag == 0 ) {
         
         quizarray.push({
             quizid: $(this).attr("quiz"),
             assignmentid: $(this).attr("assignment"),
             questionid: $(this).attr("question"),
             optionid: $(this).attr("option"),
             valueid: $(this).attr("value"),
         });
 
 
     }
     localStorage.setItem("quizarray", JSON.stringify(quizarray));   
    
 
 
 
 });



$(function () {

    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
    
    var lim = quizarray.length;
    for (var i = 0; i < lim; i++) {
        
        $('input:radio[value=' + quizarray[i].valueid + ']').prop('checked', true);
        
    }

});



$('input:checkbox').click(function () {
    var json = JSON.parse(localStorage["quizarray"]);
    $('input:checkbox').not(':checked').each(function()
    {
      uncheckedvalue=$(this).attr("value");
        for (i=0;i<json.length;i++)
           if (json[i]. valueid ==  uncheckedvalue)
             json.splice(i,1);
              localStorage["quizarray"] = JSON.stringify(json);

    });               
       
});