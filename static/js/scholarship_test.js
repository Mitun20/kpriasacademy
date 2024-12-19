if (localStorage.getItem("quizarray") === null) {
    localStorage.setItem("quizarray", JSON.stringify([]));
}

$(function(){
    retrive_answer();
});

function retrive_answer() {

    var quizarray = JSON.parse(localStorage.getItem("quizarray"));
    
    var lim = quizarray.length;
    for (var i = 0; i < lim; i++) {
        $('input:radio[value=' + quizarray[i].valueid + ']').prop('checked', true);
        
    }
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
            var res = "/scholarship_test_submission";
            localStorage.clear();
            location.href=res;
  
        }
        }); 
    }
    else{
        alert('No Questions Answered!!!');
    }

    
    
});



$('#clear_option').click(function(){
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



$('#ques_window').on('click','input:radio',function () {
 
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

$(document).ready(function()
{
    
    $('#prev_ques').hide();
    $('.ques_nav').click(function()
    {
        event.preventDefault();
        no = $(this).attr('ques_no');
        test = $('#test_id').attr('data');
        
        $.ajax({
            url : '/course_load_question/',
            data:{'question_no':no,'test':test},
            method:'get',
            success:function(data){

                $('#clear_option').attr( 'ques_no',data.question_id);
                $('#ques_window').html(data.question);
                $('#prev_ques').attr('ques_no',data.question_no-1);
                $('#next_ques').attr('ques_no',data.question_no+1);

                if(data.question_no==data.question_count-1)
                {
                    $('#next_ques').hide();
                }
                else{
                    $('#next_ques').show();
                }

                if(data.question_no==0)
                {
                    $('#prev_ques').hide();
                }
                else{
                    $('#prev_ques').show();
                }

               retrive_answer();
                
            }
        });

    });

});