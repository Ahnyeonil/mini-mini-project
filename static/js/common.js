window.onload=function(){
    /* 페이지 로딩시 실행 */
}

let goBack = function() {
    window.history.back();
};

function loginBtnOn() {
    $('#logoutBtn').css('display', 'none');
    $('#signUpBtn').css('display', 'inline-block');
    $('#loginBtn').css('display', 'inline-block');
}

function loginBtnOut() {
    $('#loginBtn').css('display', 'none');
    $('#signUpBtn').css('display', 'none');
    $('#logoutBtn').css('display', 'inline-block');
}

function login() {

    let login_id = $('#member_id').val()
    let login_pw = $('#member_pw').val()

    $.ajax({
        type: "POST",
        url: "/login",
        data: {member_id: login_id, member_pw: login_pw},
        success: function (response) {

            console.log(response)

            let membername = response['member']
            let html_temp = `<div id="visit-comment">${membername}님 환영합니다</div>`

            if (response['msg'] === '로그인 완료!') {
                loginBtnOut()
                $('.form-group').hide()
                alert(response['msg'])
                $('#loginMember').prepend(html_temp)
            }
            else {
                loginBtnOn()
                alert(response['msg'])
            }

        }
    })
}

function logout() {

    $.ajax({
        type: "GET",
        url: "/logout",
        data: {},
        success: function (response) {
            console.log(response)
            alert(response['msg'])
            loginBtnOn()
            $('.form-group').show()
            $('#visit-comment').remove()
        }
    })
}

function signup() {

    let user_id = $('#member_id').val()
    let user_pw = $('#member_pw').val()
    let pw_confirm = $('#member_pw_').val()
    let user_name = $('#member_name').val()
    let user_nickname = $('#member_nickname').val()

    // 유효성 검사 옵션
    if (user_id === "") {
        $('#member_id').focus()
        return alert("아이디를 입력하세요")
    }
    if(user_pw === ""){
        $('#member_pw').focus()
        return alert("비밀번호를 입력하세요")
    }
    if (user_pw !== pw_confirm) {
        $('#member_pw_').val('')
        $('#member_pw_').focus()
        return alert("비밀번호가 다릅니다")
    }
    let pwdCheck = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*\d).{8,25}$/;
    if (!pwdCheck.test(user_pw)) {
        $('#member_pw').val('')
        $('#member_pw_').val('')
        $('#member_pw').focus()
        return alert("비밀번호는 영문자+숫자+특수문자 조합으로 8~25자리 사용해야 합니다")
    }
    if (user_name === ""){
        $('#member_name').focus()
        return alert("이름을 입력하세요")
    }
    if (user_nickname === ""){
        $('#member_nickname').focus()
        return alert("닉네임을 입력하세요")
    }

    $.ajax({
        type: "POST",
        url: "/signup",
        data: {
            userid: user_id,
            userpw: user_pw,
            username: user_name,
            usernickname: user_nickname
        },
        success: function (response) {

            if (response['msg'] === '회원 가입 완료!'){
                alert(response['msg'])
                location.replace('/login')
            }
            else if (response['msg'] === '동일한 id가 존재합니다!') {
                alert(response['msg'])
                $('#member_id').val('')
            }
            else if (response['msg'] === '동일한 닉네임이 존재합니다!') {
                alert(response['msg'])
                $('#member_nickname').val('')
            }

        }
    })
}