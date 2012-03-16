window.SL = SL;
SL.Controller = {};

SL.Controller.alert = {
    noLogin : function(){
        $('#alertModal .modal-body p').text('您还没有登录，请先登录');
        $('#alertModal .modal-footer a').attr("href", "/login/?next={%url profile profile.user.username%}");
        $('#alertModal .modal-footer a').text(">>跳转到登录页面");
        $('#alertModal').modal({'show': true});
    }
}
