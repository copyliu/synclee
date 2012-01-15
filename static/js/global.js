

var Model = {
    'topmenu' : [
        {"name":"News", "url" : "news.htm"},
        {"name":"About", "url" : "about.htm"},
        {"name":"Contact", "url" : "2"},
        {"name":"Projects", "url" : "2"}
    ]
}

var mainViewModel = function(){
    this.getArticle = function(name){
        return $.ajax({url: '/article/'+name+'.txt',success: function(data){
           return data;
        }});
    }
};

var Controller = {};
Controller.getArticle = function(name){
    $.ajax({url: '/data/'+name+'.txt',success: function(data){
        $('article p').text(data);
    }});
}
Controller.editArticle = function(name){
    $.ajax({
        type : 'POST',
        url : '/main.php',
        data : {'name': name, 'content': $('article p').text()},
        success : function(data){
            console.log(data);
            location.reload();
        }
    })
}
$(document).ready(function(){
    $.ajax({
        type: 'GET',
        url: '/views/header.htm',
        success: function(data){
           $('header').html(data)
        }
    })

if (document.cookie == 'username=admin'){
    $('.content article p').attr('contentEditable','true');
    $('.content article p').after('<button class="btn success" onclick="Controller.editArticle(\'about\')">Submit</button>');
}
});
