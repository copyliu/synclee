/* 此为巨坑，日后再填 */
module.provide(['pageload', 'jQuery'], function(req){
	var $ = req('jQuery').$;
	
	$('#btnUploadFile').live("click", function(){
		$('#pChangeImageDesc').show();
		return false;
	});
	
	$('#vform2').live("submit", function(){
		//alert($(":file").val());
		var filename = $(":file").val();
		var regex=/(.*)\.(jpg|jpeg|gif|png|bmp)$/i;
		if (filename == "") {
			return true;
		}
  		if(!regex.test(filename)){
			alert("文件格式不正确,请选择图像文件");
			return false;
		}
		return true;
	});
	
	$('#upload_cover').live("submit", function(){
		//alert($(":file").val());
		var filename = $(":file").val();
		var regex=/(.*)\.(jpg|jpeg|gif|png|bmp)$/i;
		if (filename == "") {
			return true;
		}
  		if(!regex.test(filename)){
			alert("文件格式不正确,请选择图像文件");
			return false;
		}
		return true;
	});
	
	$('#pUploadedContents > .gallery a').live("click", function(){
		$.getJSON("/work/" + $('#gallery_id').attr("work") + "/gallery_section/?section_id=" + $(this).attr("name"),
			function(data) {
				$("#title").val(data['title']);
				$("#content").val(data['content']);
			}
		);
		$("#section_id").val($(this).attr("name"));
		$('#pChangeImageDesc').show();
		return false;
	});
	
	$('#btnCancelPictureMeta').live("click", function(){
		$("#section_id").val("0");
		$("#title").val("");
		$("#content").val("");
		$("#picture").val("");
		$('#pChangeImageDesc').hide();
		return false;
	});
	
	
	$('#btnAddText').live("click", function(){
		$('#pUploadTextContent').show();
		return false;
	});
	$('#btnCancelText').live("click", function(){
		$("#title").val("");
		$("#text_content").val("");
		nicEditors.findEditor('text_content').setContent("");
		$('#sid').val("");
		$('#pUploadTextContent').hide();
		return false;
	});
	
	$("#timeline-update").live("submit", function(){
		if ($('#tweet_content').val() == "") {
			return false;
		}
		var json_obj = {
			status: $('#tweet_content').val()
		};
		var json_str = JSON.stringify(json_obj); 
		$.ajax({
			type: "POST",
			url: "/tweet/add_tweet/",
			data: json_str,	
			success: function(msg){
			  $("#tweet_list").load("/tweet/refresh_tweet/");
			  //window.location.reload();
			}
		});
		return false;
	});
	

	$("#timeline-form").live("submit", function(){
		if ($(this).children("#reply_tweet").val() == "") {
			return false;
		}
		var json_obj = {
			status: $(this).children("#reply_tweet").val()
		};
		var json_str = JSON.stringify(json_obj); 
		var the_url = $(this).find(":hidden").val();
		$.ajax({
			type: "POST",
			url: $(this).children("#the_id").val(),
			data: json_str,	
			success: function(msg){
			  $("#tweet_list").load("/tweet/refresh_tweet/");
			  //$("#person_tweet_list").load("/tweet/refresh_tweet/"+$("#person_tweet_list").attr("name"));
			}
		});
		return false;
	});
	
	$("#person-timeline-form").live("submit", function(){
		var json_obj = {
			status: $(this).children("#reply_tweet").val()
		};
		var json_str = JSON.stringify(json_obj); 
		var the_url = $(this).find(":hidden").val();
		$.ajax({
			type: "POST",
			url: $(this).children("#the_id").val(),
			data: json_str,	
			success: function(msg){
			  //$("#tweet_list").load("/tweet/refresh_tweet/");
			  $("#person_tweet_list").load("/tweet/refresh_tweet/"+$("#person_tweet_list").attr("name"));
			}
		});
		return false;
	});
	
	//$("#form-post-comment").live("submit", function(){
	$(document).delegate("#form-post-comment", "submit", function(){
	//$("#form-post-comment").live("submit", function(){
		if ($(this).children("#status").val() == "") {
		    return false;
		}
		var json_obj = {
			status: $(this).children("#status").val()
		};
		var refresh_url = $("#form-post-comment").attr("refresh_url")
		var urls = $(this).attr("url")
		var json_str = JSON.stringify(json_obj); 
		$.ajax({
			type: "POST",
			url: urls,
			data: json_str,	
			success: function(msg){
			   $('#comments_timeline').load(refresh_url);
			}
		});
		//$("#form-post-comment").attr("refresh_url", refresh_url);
		//$("#form-post-comment").attr("url", urls);
		$(this).children("#status").val("");
		return false;
	});
	
	$('#btnCommitText').live("click", function(){
		var json_obj = {
			title: $('#title').val(), 
			//content: $('#content').val()
			content: nicEditors.findEditor('text_content').getContent()
		};
		var json_str = JSON.stringify(json_obj);    //将JSON对象转变成JSON格式的字符串
		if (!$('#title').val()) {
			$('#title').val("请在这里填写标题哦！");
			return false;
		}
		$.ajax({
			type: "POST",
			url: "/work/" + $('#wid').val() + "/text/section/?text_id=" + $('#tid').val() + "&section_id=" + $('#sid').val(),
			data: json_str,	
			success: function(msg){
			  $("#pUploadedContents").load("/work/" + $('#wid').val() + "/refresh_text/?text_id=" + $('#tid').val());
			}
		});
		$('#pUploadTextContent').hide();
		nicEditors.findEditor('text_content').setContent("");
		$('#title').val("");
		$('#sid').val("");
		return false;
	});
	
	
	$(".show_reply").live("click", function(){
		var form = $(this).parent().parent().children(".timeline-reply");
		form.toggle('slow');
		return false;
	});
	
	$(".all").live("click", function(){
		var form = $(this).parent().parent().children("#reply_sheet");
		form.toggle('slow');
		return false;
	});
	
	$("#pUploadedContents .chapter h3 a").live("click", function(){
		$.getJSON("/work/" + $(this).attr("work") + "/text_section/?section_id=" + $(this).attr("name"),
			function(data) {
				$("#title").val(data['title']);
				$("#text_content").val(data['content']);
				nicEditors.findEditor('text_content').setContent(data['content']);
				
			}
		);
		$("#sid").val($(this).attr("name"));
		if ($("#sid").val() != "") {
			$('#pUploadTextContent').show();
		}
		
		return false;
	});
	
	$(".btnLoadPreText").live("click", function(){
		var pre_section = $("#pre");
		var pre_id = pre_section.attr("pre_id");
		$("#section_general").load("/work/" + pre_section.attr("work") + "/refresh_text_section/?text_id=" + pre_section.attr("chapter") + "&section_id=" + pre_id);
		//$("#pre-01").load("/work/" + pre_section.attr("work") + "/refresh_pre/?text_id=" + pre_section.attr("chapter") + "&section_id=" + pre_id);
		//$("#sec-01").load("/work/" + pre_section.attr("work") + "/refresh_section/?text_id=" + pre_section.attr("chapter") + "&section_id=" + pre_id);
		//$("#next-01").load("/work/" + pre_section.attr("work") + "/refresh_next/?text_id=" + pre_section.attr("chapter") + "&section_id=" + pre_id);
		$('html,body').animate({scrollTop: '0px'}, 800);
		return false;
	});
	
	$(".btnLoadNextText").live("click", function(){
		var pre_section = $("#next");
		var next_id = pre_section.attr("next_id")
		var pre_id = pre_section.attr("pre_id");
		$("#section_general").load("/work/" + pre_section.attr("work") + "/refresh_text_section/?text_id=" + pre_section.attr("chapter") + "&section_id=" + next_id);
		//$("#pre-01").load("/work/" + pre_section.attr("work") + "/refresh_pre/?text_id=" + pre_section.attr("chapter") + "&section_id=" + next_id);
		//$("#sec-01").load("/work/" + pre_section.attr("work") + "/refresh_section/?text_id=" + pre_section.attr("chapter") + "&section_id=" + next_id);
		//$("#next-01").load("/work/" + pre_section.attr("work") + "/refresh_next/?text_id=" + pre_section.attr("chapter") + "&section_id=" + next_id);
		$('html,body').animate({scrollTop: '0px'}, 800);
		return false;
	});


	$('[name=asClub]').live("click", function(){
		$('[name=clubName]').attr('disabled', !($(this).attr('checked')))
	});
	
	$('#next_page').live("click", function(){
		$("#tweet_list").load("/tweet/refresh_tweet/" + $(this).attr("url"));
		return false;
	});
	
	$('#pre_page').live("click", function(){
		$("#tweet_list").load("/tweet/refresh_tweet/" + $(this).attr("url"));
		return false;
	});
	
	$('#next_page_person').live("click", function(){
		$("#person_tweet_list").load("/tweet/refresh_tweet/"+$("#person_tweet_list").attr("name") + $(this).attr("url"));
		return false;
	});
	
	$('#pre_page_person').live("click", function(){
		$("#person_tweet_list").load("/tweet/refresh_tweet/"+$("#person_tweet_list").attr("name") + $(this).attr("url"));
		return false;
	});
	
	$('#next_page_comment').live("click", function(){
		$('#comments_timeline').load("/work/" + $("#form-post-comment").attr("work") + "/refresh_comment/" + $(this).attr("url"));
		return false;
	});
	
	$('#pre_page_comment').live("click", function(){
		$('#comments_timeline').load("/work/" + $("#form-post-comment").attr("work") + "/refresh_comment/" + $(this).attr("url"));
		return false;
	});
	
	$('#next_page_relations').live("click", function(){
		$('#relationship-list').load($('#relationship-list').attr("url") + $(this).attr("url"));
		return false;
	});
	
	$('#pre_page_relations').live("click", function(){
		$('#relationship-list').load($('#relationship-list').attr("url") + $(this).attr("url"));
		return false;
	});
	
	$('#next_page_note').live("click", function(){
		$("#dm_old").load("/notes/refresh/" + $('#next_page_note').attr("url"));
		//$("#note_pager").load("/notes/refresh_pager/" + $('#pre_page_note').attr("url"));
		return false;
	});
	
	$('#pre_page_note').live("click", function(){
		$("#dm_old").load("/notes/refresh/" + $('#pre_page_note').attr("url"));
		//$("#note_pager").load("/notes/refresh_pager/" + $('#pre_page_note').attr("url"));
		return false;
	});
	
	$('#next_page_history').live("click", function(){
		$("#history-timeline").load($("#history-timeline").attr("url") + $(this).attr("url"));
		return false;
	});
	
	$('#pre_page_history').live("click", function(){
		$("#history-timeline").load($("#history-timeline").attr("url") + $(this).attr("url"));
		return false;
	});
	
	$('#next_page_search').live("click", function(){
		$("#search-list").load($("#search-list").attr("url") + $(this).attr("url"));
		return false;
	});
	
	$('#pre_page_search').live("click", function(){
		$("#search-list").load($("#search-list").attr("url") + $(this).attr("url"));
		return false;
	});
	
	$('.pages').live("click", function(){
		$('#comments_timeline').load("/work/" + $("#form-post-comment").attr("work") + "/refresh_comment/" + $(this).attr("url"));
		$("#person_tweet_list").load("/tweet/refresh_tweet/"+$("#person_tweet_list").attr("name") + $(this).attr("url"));
		$("#tweet_list").load("/tweet/refresh_tweet/" + $(this).attr("url"));
		$("#dm_old").load("/notes/refresh/" + $(this).attr("url"));
		$('#relationship-list').load($('#relationship-list').attr("url") + $(this).attr("url"));
		$("#history-timeline").load($("#history-timeline").attr("url") + $(this).attr("url"));
		$("#search-list").load($("#search-list").attr("url") + $(this).attr("url"));
		return false;
	});
	
	$('#box_hasten').live("click", function(){
		$('#project-info-01').load("/work/" + $(this).attr("work") + "/refresh_info/");
		alert("感谢您的支持");
		return false;
	});
	
	$('#box_watch').live("click", function(){
		$('#project-info-01').load($(this).attr("url"));
		$(this).hide();
		alert("感谢您的支持");
		return false;
	});
	
	
	$('#delete_work').live("click", function(){
		$.confirm({
			'title'		: '确认删除作品',
			'message'	: '你正准备要删除这个作品<br>所有该作品的信息和评论都将消失，你确定要继续吗?',
			'buttons'	: {
				'Yes'	: {
					'class'	: 'blue',
					'action': function(){
						window.location.href="/work/" + $('#delete_work').attr("work") + "/del/";
					}
				},
				'No'	: {
					'class'	: 'gray',
					'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
				}
			}
		});
	});
	
	$('#del_gallery_section').live("click", function(){
		if ($('#section_id').val() == "0") {
			return false;
		}
		$.confirm({
			'title'		: '确认删除图片',
			'message'	: '你正准备要删除这个图片<br>你确定要继续吗?',
			'buttons'	: {
				'Yes'	: {
					'class'	: 'blue',
					'action': function(){
						window.location.href="/work/" + $('#gallery_id').attr("work") + "/del_gallery_section/?" + "section_id=" + $('#section_id').val();
					}
				},
				'No'	: {
					'class'	: 'gray',
					'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
				}
			}
		});
	});
	
	$('#del_text_section').live("click", function(){
		if ($("#sid").val() == "") {
			return false;
		}
		$.confirm({
			'title'		: '确认删除段落',
			'message'	: '你正准备要删除这个段落<br>你确定要继续吗?',
			'buttons'	: {
				'Yes'	: {
					'class'	: 'blue',
					'action': function(){
						if ($('#sid').val() != "") {
							window.location.href="/work/" + $('#wid').val() + "/del_text_section/?" + "section_id=" + $('#sid').val();
						}
						else {
							window.location.href=$('#del_text_section').attr("the_url");
						}
						
					}
				},
				'No'	: {
					'class'	: 'gray',
					'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
				}
			}
		});
	});
	
	$('#del_text').live("click", function(){
		$.confirm({
			'title'		: '确认删除章节',
			'message'	: '你正准备要删除这个章节<br>你确定要继续吗?',
			'buttons'	: {
				'Yes'	: {
					'class'	: 'blue',
					'action': function(){
						window.location.href="/work/" + $('#wid').val() + "/edit/text/?action=del&" + "text_id=" + $('#tid').val();
					}
				},
				'No'	: {
					'class'	: 'gray',
					'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
				}
			}
		});
	});
	
	$('#del_gallery').live("click", function(){
		$.confirm({
			'title'		: '确认删除图集',
			'message'	: '你正准备要删除这个图集<br>你确定要继续吗?',
			'buttons'	: {
				'Yes'	: {
					'class'	: 'blue',
					'action': function(){
						window.location.href="/work/" + $('#gallery_id').attr("work") + "/edit/gallery/?action=del&" + "gallery_id=" + $('#gallery_id').attr("gid");
					}
				},
				'No'	: {
					'class'	: 'gray',
					'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
				}
			}
		});
	});
	
	$('#del_tweet').live("click", function(){
		$.confirm({
			'title'		: '确认删除状态',
			'message'	: '你正准备要删除这个状态<br>你确定要继续吗?',
			'buttons'	: {
				'Yes'	: {
					'class'	: 'blue',
					'action': function(){
						$.ajax({
								type: "GET",
								url: $('#del_tweet').attr("del_url"),
								success: function(msg){
								  $("#tweet_list").load("/tweet/refresh_tweet/");
								  $("#person_tweet_list").load("/tweet/refresh_tweet/"+$("#person_tweet_list").attr("name"));
								}
							});
					}
				},
				'No'	: {
					'class'	: 'gray',
					'action': function(){}	// Nothing to do in this case. You can as well omit the action property.
				}
			}
		});
	});
});
