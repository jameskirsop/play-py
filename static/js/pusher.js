Pusher.log = function(message) {
if (window.console && window.console.log) {
		window.console.log(message);
	}
};

var pusher = new Pusher('***REMOVED***', {
  cluster: 'ap1',
  encrypted: true
});

var channel = pusher.subscribe('play-py');
channel.bind('now-playing', function(data) {
  Array.prototype.forEach.call(document.querySelectorAll('.info-title'),function(el,i){
  	console.log(el);
  	el.innerHTML = data.title;
  });
  Array.prototype.forEach.call(document.querySelectorAll('.info-artist'),function(el,i){
  	console.log(el);
  	el.innerHTML = data.artist;
  });

	  Array.prototype.forEach.call(document.querySelectorAll('.album-artwork'),function(el,i){
	if(el.src.indexOf('?')>-1){
		address = el.src.split('?')[0];
	} else {
		address = el.src;
	}
	el.src = address+"?time="+new Date().getTime();
	});
});

var trackListTemplate = _.template('<%= title %> by <%= artist %>')
channel.bind('upcoming-track-list', function(data){
	Array.prototype.forEach.call(document.querySelectorAll('.data_total-tracks'),function(el,i){
		el.innerHTML == data.iTotalTracks;
	});
	playlistContainer = document.querySelector('.upcoming-track-list');
	playlistContainer.innerHTML = '';
	Array.prototype.forEach.call(data.tracks,function(el,i){
		console.log(data.tracks[i]);
		data.tracks[i].artist = (typeof data.tracks[i].artist === "undefined" ? '' :  data.tracks[i].artist)
		liEl = document.createElement('li');
		liEl.innerHTML = trackListTemplate(data.tracks[i])
		playlistContainer.appendChild(liEl);
	});
});