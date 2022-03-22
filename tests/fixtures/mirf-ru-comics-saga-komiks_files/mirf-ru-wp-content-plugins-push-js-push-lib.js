var $ = jQuery;

// google firebase initial
firebase.initializeApp({
	messagingSenderId: "614051842659"
});
const messaging = firebase.messaging();

function IMPush() {
	// event listener
	messaging.onMessage(function(payload) {
		console.log("onMessage: ",payload);
		const pushUrl = payload.data.click_action;
		payload.data.data = {
			click_action: pushUrl
		};
		var notify = new Notification(payload.data.title, payload.data);
		notify.onclick = function(event) {
			const pushUrl = event.target.data.click_action;			
		    event.target.close();
		    return window.open(pushUrl,"_blank");
		}
	});
}
IMPush.prototype.addSubscribe = function(subscribeID,refresh) {
	var thisObj = this;
	var refresh = refresh === undefined ? false : refresh;
	
	//window.localStorage.removeItem("push_"+subscribeID); // FIX FOR TEST!
	return new Promise(function(resolve,reject) {
		// check subscribe state
		if (!refresh && window.localStorage.getItem("push_state_"+subscribeID) == 0) {
			console.log("addSubscribe: subscribe unset by user");
			resolve();
			return;
		}
		// add new subscribe
		thisObj.askRequest().then(function(token) {
			if (!refresh && window.localStorage.getItem("push_token_"+subscribeID) == token) {
				console.log("addSubscribe: exists in local storage");
				resolve();
			}
			else {
				var urlParams = {
					action: "addSubscribe",
					token: token,
					subscribeID: subscribeID
				};
				$.ajax("/wp-content/plugins/push/actions/process.php",{
					data: $.param(urlParams),
					type: "POST",
					dataType: "JSON",
					success: function(data) {
						if (data['type'] == "success") {
							window.localStorage.setItem("push_token_"+subscribeID,token);
							window.localStorage.setItem("push_state_"+subscribeID,1);
							console.log("addSubscribe: added on server");
							//console.log("google response:",data['googleResponse']);
							resolve();
						}
						else {
							console.log("addSubscribe: error adding on server");
							reject();
						}
					}
				});
			}
		}).catch(function() {
			window.localStorage.setItem("push_state_"+subscribeID,0);
			reject();
		});;
	});
}
IMPush.prototype.deleteSubscribe = function(subscribeID) {
	var thisObj = this;
	return new Promise(function(resolve,reject) {
		thisObj.askRequest().then(function(token) {
			var urlParams = {
				action: "deleteSubscribe",
				token: token,
				subscribeID: subscribeID
			};
			$.ajax("/wp-content/plugins/push/actions/process.php",{
				data: $.param(urlParams),
				type: "POST",
				dataType: "JSON",
				success: function(data) {
					if (data['type'] == "success") {
						console.log("deleteSubscribe: deleted from server");
						window.localStorage.setItem("push_state_"+subscribeID,0);
						resolve();
					}
					else {
						console.log("deleteSubscribe: error delete from server");
						reject();
					}
				}
			});
		}).catch(function() {
			reject();
		});
	});
}
IMPush.prototype.askRequest = function() {
	return new Promise(function(resolve,reject) {
		// request permission
		messaging.requestPermission().then(function() {
			console.log("Have permission");
			// get token
			return messaging.getToken();
		}).then(function(token) {
			console.log("Have token");
			resolve(token);
		}).catch(function(error) {
			console.log("error ask request:", error);
			reject();
		});
	});
}


function IMPushSub() {
}
IMPushSub.prototype.action = function(pushLink) {
	var thisObj = this;
	var subscribeID = "hot";
	var storageKey = "push_state_"+subscribeID;
	var pushLink = $(pushLink);
	if (window.localStorage.getItem(storageKey) == 0) {
		push.addSubscribe(subscribeID,true).then(function(){
			thisObj.showLink(subscribeID);
		}).catch(function() {
		});
	}
	else {
		push.deleteSubscribe(subscribeID).then(function(){
			thisObj.showLink(subscribeID);
		}).catch(function() {
		});
	}
}
IMPushSub.prototype.showLink = function(subscribeID) {
	var thisObj = this;
	var subState = window.localStorage.getItem("push_state_"+subscribeID);
	var pushLink = $("#pushSubLink");
	if (subState == 1) {
		pushLink.html("Выключить Push-уведомления");
		pushLink.removeClass("on").addClass("off");
	}
	else {
		pushLink.html("Включить Push-уведомления");
		pushLink.removeClass("off").addClass("on");
	}
	pushLink.click(function(event) {
		thisObj.action(event.target);
	});
}

push = new IMPush();
pushSub = new IMPushSub();

// ask request and subscribe
$(document).ready(function() {
	var subscribeID = "hot";
	push.addSubscribe(subscribeID).then(function() {
		pushSub.showLink(subscribeID); // refresh link
	},function(error) {
	});
	
	// show sub link
	//pushSub.showLink();
});