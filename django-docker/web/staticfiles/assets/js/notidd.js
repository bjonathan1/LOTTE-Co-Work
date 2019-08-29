$(document).ready(function(){
	var count = 0;
	$("#notification-dropdown").hide();
	$("#bellClick").click(function(){
				  $("#notification-dropdown").toggle();
					var count = 0;
					$("#notifications-count").html(count);
					$("#dd-notifications-count").html(count);
	});
	$(".body-image").click(function(){
		  $("#notification-dropdown").hide();
	})
	$(".searchbox-wrapper").click(function() {
		$("#notification-dropdown").hide();
	})

	var data = [
    {"image":"../../../staticfiles/assets/img/hj.jpg", "name":"박형준님","status" :"이 회의신청을 했습니다."},
    {"image":"../../../staticfiles/assets/img/ij.jpg", "name":"김익준님","status" :"이 보고신청을 수락했습니다."},
    {"image":"../../../staticfiles/assets/img/ye.jpg", "name":"박예은님","status" :"이 자료요청을 했습니다."},
];
console.log(data);
	var notification = '';
		for(var i=0;i<data.length;i++){
			var cnt = document.getElementById("notifications-count").innerHTML;
		console.log(cnt);
			if(cnt==0){
				count = 0;
			}
			count +=3;
			if(data.length > 0){
				notification += "<div class='notification new' style='display:flex;'><div class='notification-image-wrapper'><div class='notification-image'><img src='" + data[i].image + "' width='32'></div></div><div class='notification-text'><span class='highlight'>"+" "+data[i].name+"</span>"+data[i].status+"</div></div>";
			}
		}
		 $(".dropdown-body").prepend(notification);
		 $("#notifications-count").html(count);
		 $("#dd-notifications-count").html(count);
});

