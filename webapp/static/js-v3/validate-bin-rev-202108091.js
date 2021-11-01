function trim(e){return e.replace(/^\s+|\s+$/,"")}function validateFormOnSubmit(e){var a
return a=validateSelect(document.getElementById("category")),a+=validateEmpty(document.getElementById("headline")),a+=validateEmptyEditor(),""!=(a+=validateSubmitionAjaxCaptcha())?(alert("Some items need correction:\n"+a),!1):(document.getElementById("submit_story").disabled=!0,filterStoryContent(),!0)}function validateFeedOnSubmit(e){var a=""
return a+=validateSelect(document.getElementById("category")),a+=validateEmpty(document.getElementById("name")),a+=validateEmpty(document.getElementById("url")),a+=validateEmpty(document.getElementById("homepage")),a+=validateUrl(document.getElementById("url")),""==(a+=validateUrl(document.getElementById("homepage")))||(alert("Some items need correction:\n"+a),!1)}function validateEmpty(e){var a=""
return 0==e.value.length?(e.style.background="Yellow",a="You didn't enter '"+e.name+"'.\n"):e.style.background="White",a}function validateEmptyEditor(){var e=""
return $("#filtered_story_content_html").html(CKEDITOR.instances.editor1.getData()),""==trim($("#filtered_story_content_html").html())&&(e="The required field 'story content' has not been filled.\n"),e}function validateEmptyTextarea(e){var a=""
return"editor1"==e.name?fldname="story":fldname=e.name,0==e.value.length?(e.style.background="Yellow",a="The required field '"+fldname+"' has not been filled in.\n"):e.style.background="White",a}function validateSelect(e){var a=""
return 0==e.value.length?(e.style.background="Yellow",a="The required item '"+e.name+"' must be selected.\n"):e.style.background="White",a}function validateUsername(e){var a="",t=/\W/
return""==e.value?(e.style.background="Yellow",a="You didn't enter a username.\n"):e.value.length<5||e.value.length>15?(e.style.background="Yellow",a="The username is the wrong length.\n"):t.test(e.value)?(e.style.background="Yellow",a="The username contains illegal characters.\n"):e.style.background="White",a}function validatePasswordIllegalChars(e){var a="",t=/[\W_]/
return""==e.value?(e.style.background="Yellow",a="You didn't enter a password.\n"):e.value.length<6||e.value.length>15?(a="The password is the wrong length (at least six characters long). \n",e.style.background="Yellow"):t.test(e.value)?(a="The password contains illegal characters.\n",e.style.background="Yellow"):e.value.search(/(a-z)+/)&&e.value.search(/(0-9)+/)?e.style.background="White":(a="The password must contain at least one numeral.\n",e.style.background="Yellow"),a}function validatePassword(e){var a=""
return""==e.value?(e.style.background="Yellow",a="You didn't enter a password.\n"):e.value.length<6||e.value.length>128?(a="The password is the wrong length (at least six characters long). \n",e.style.background="Yellow"):e.value.search(/(a-z)+/)&&e.value.search(/(0-9)+/)?e.style.background="White":(a="The password must contain at least one numeral.\n",e.style.background="Yellow"),a}function validateEmail(e){var a="",t=trim(e.value),l=/^[^@]+@[^@.]+\.[^@]*\w\w$/
return""==e.value?(e.style.background="Yellow",a="You didn't enter an email address.\n"):l.test(t)?e.value.match(/[\(\)\<\>\,\;\:\\\"\[\]]/)?(e.style.background="Yellow",a="The email address contains illegal characters.\n"):e.style.background="White":(e.style.background="Yellow",a="Please enter a valid email address.\n"),a}function validatePhone(e){var a="",t=e.value.replace(/[\(\)\.\-\ ]/g,"")
return""==e.value?(a="You didn't enter a phone number.\n",e.style.background="Yellow"):isNaN(parseInt(t))?(a="The phone number contains illegal characters.\n",e.style.background="Yellow"):10!=t.length&&(a="The phone number is the wrong length. Make sure you included an area code.\n",e.style.background="Yellow"),a}function validateCaptcha(){challengeField=$("input#recaptcha_challenge_field").val(),responseField=$("input#recaptcha_response_field").val()
var e=$.ajax({type:"POST",url:"/recaptcha/ajax.recaptcha.php",data:"recaptcha_challenge_field="+challengeField+"&recaptcha_response_field="+responseField,async:!1}).responseText,a=""
return"success"!=e&&(a="The security code you entered did not match. Please try again.\n",Recaptcha.reload()),a}function validateSubmitionAjaxCaptcha(){var e=$("input#txtCaptcha").val(),a=$.ajax({type:"POST",url:"/captcha/ajax.captcha.php",data:"txtCaptcha="+e,async:!1}).responseText,t=""
return"success"!=a?($("input#txtCaptcha").css("backgroundColor","Yellow"),t="The security code you entered did not match. Please try again.\n",refreshCaptcha()):$("input#txtCaptcha").css("backgroundColor","White"),t}function validateUrl(e){var a=new RegExp("^(http|https|ftp|feed)://([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&amp;%$-]+)*@)*((25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]).(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0).(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0).(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])|([a-zA-Z0-9-]+.)*[a-zA-Z0-9-]+.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(/($|[a-zA-Z0-9.,?'\\+&amp;%$#=~_-]+))*$"),t=""
return a.test(e.value)?e.style.background="White":(e.style.background="Yellow",t="The URL of '"+e.name+"' is not valid.\n"),t}function checkUserEmail(e){var a
a=validateEmpty(document.getElementById(e.id)),""==a&&(a=validateEmail(document.getElementById(e.id))),""!=a?$("#check_user_email_result").html('<img src="/img/dashboard/fail.png" /> <small>'+a+"</small>"):$.get("/core/ajax/login/check_user.php",{email:e.value},function(e){"1"==e?$("#check_user_email_result").html('<img src="/img/dashboard/fail.png" /> <small>Email existed, please use another!</small>'):$("#check_user_email_result").html('<img src="/img/dashboard/success.png" />')})}function checkUserPassword(e){var a
a=validatePassword(document.getElementById(e.id)),""!=a?$("#check_user_password_result").html('<img src="/img/dashboard/fail.png" /> <small>'+a+"</small>"):$("#check_user_password_result").html('<img src="/img/dashboard/success.png" />')}function checkUserPasswordRetype(e,a){var t
t=e.value!=a.value?"Your password and confirmation password do not match!":"",""==e.value&&(t="You didn't enter a password. "),""!=t?$("#check_user_password_retype_result").html('<img src="/img/dashboard/fail.png" /> <small>'+t+"</small>"):$("#check_user_password_retype_result").html('<img src="/img/dashboard/success.png" />')}function checkUserPenname(e){var a
a=validateEmpty(document.getElementById(e.id)),""!=a?$("#check_user_penname_result").html('<img src="/img/dashboard/fail.png" /> <small>'+a+"</small>"):$("#check_user_penname_result").html('<img src="/img/dashboard/success.png" />')}