function escapeHTML(s){return s.toString().split('&').join('&amp;').split('<').join('&lt;').split('"').join('&quot;');} 

$(document).ready(function(){
	$('input[type=text]').on('keyup', function(e) {
		if (e.which == 13) {
			e.preventDefault();
			$('#sendtext').click();
		}
	});
	$('#sendtext').click(function(){
		var input = escapeHTML($('#chatinput').val());
		if (input !== "") {
			$('#chatwindow').prepend("<div><b>You</b>: "+input+"</div>");
			$('#chatinput').val('');
		}

		$.get("/chat/", {"text": $('#chatinput').val()}, function(data){
			if (escapeHTML(data.text) !== "") {
				$('#chatwindow').prepend("<div><b>Markoff</b>: "+escapeHTML(data.text)+"</div>");
			}
		});
	});
});
