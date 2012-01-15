module.provide(['switcher', 'pageload', 'jQuery', 'selectionH'], function(require){
	var $ = require('jQuery').$;
	var quoteAction = new (require('switcher').Switch);
	quoteAction.onswitchon = function(){
		$('#quoteFloatBox').show();
		var hash = $(window.location.hash).get(0);
		if(hash) hash.scrollIntoView();
	};
	quoteAction.onswitchoff = function(){
		$('#quoteFloatBox').hide(); 
	};
	$('#lCommentQuote').live("click", function(){
		quoteAction.turn(true);
		return false;
	});
	$('#lActQuote').live("click", function(){
		var text = require('selectionH').getSelected().replace(/^/gm, '> ') + '\n';
		$('#form-post-comment > textarea').focus().append(text);
		quoteAction.turn(false);
		return false;
	});
	$('#lCancelQuote').live("click", function(){
		quoteAction.turn(false);
		return false;
	});
});
