(function($){
    var localVideo = document.querySelector('#localVideo');
var remoteVideo;
const startButton = document.getElementById('startButton');
console.log("video open");

var rpc;
var remoteStream;
var localStream;
var roomName = "webrtc";
var isStarted = true;
var isInitiator = false;



const videoRoomName = JSON.parse(document.getElementById('room-name').textContent);

const videoRoomSocket = new WebSocket(
                'wss://'
                + window.location.host
                + '/ws/rooms/'
                + videoRoomName
                + roomName
                + '/'
            );

videoRoomSocket.onopen = function(e) {
  videoRoomSocket.send(JSON.stringify({
  "type": "create or join"
}));
}

window.onbeforeunload = function(event){
  videoRoomSocket.send(JSON.stringify({
  "type": "bye"
}));
}



navigator.mediaDevices.getUserMedia({
  audio: false,
  video: true
}).then(gotStream)
.catch(function(e) {
  alert('getUserMedia() error: ' + e.name);
});

function gotStream(stream) {
  console.log('Adding local stream.');

  localStream = stream;
  localVideo.srcObject = stream;
}

// startButton.addEventListener('click', startAction);

videoRoomSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  console.log('Client received message:', data.message);
  console.log("data type: ", data.type);
  if (data.type === 'bye' && isStarted) {
    handleRemoteHangup();
    changeInitiator(data.number)
    console.log("pertitipants number: ", data.number);
    console.log("initiator: ", isInitiator);
    return
  }
  if (data.message == "create") {
    console.log("pertitipants number: ", data.number);
      isInitiator = true;
      return
    }
  if (data.message == "join" && !isInitiator) {
    console.log("pertitipants number: ", data.number);
    startAction();
    return
  }
  if (data.message === 'got user media') {
      console.log('got user media');
    maybeStart();
  } else if (data.message.type === 'offer' && isInitiator) {
      console.log('offer');
    if (isInitiator) {
      maybeStart();
    }
    console.log('remote description', data.message);
    pc.setRemoteDescription(new RTCSessionDescription(data.message));
    doAnswer();
  } else if (data.message.type === 'answer' && isStarted && !isInitiator) {
    pc.setRemoteDescription(new RTCSessionDescription(data.message));
  } else if (data.message.type === 'candidate' && isStarted && pc !== data.message.target) {
    console.log("candidate", data.message.candidate);
    var candidate = new RTCIceCandidate({
      sdpMLineIndex: data.message.label,
      candidate: data.message.candidate
    });
    pc.addIceCandidate(candidate);
  }
};

function startAction() {
  maybeStart();
}

function maybeStart() {
    console.log('>>>>>>> maybeStart() ');
    isStarted = true;
    console.log('>>>>>> creating peer connection');
    createPeerConnection();
    pc.addStream(localStream);
    if (!isInitiator) {
      doCall();
    }
}

function createPeerConnection() {
  try {
    pc = new RTCPeerConnection(null);
    pc.onicecandidate = handleIceCandidate;
    pc.onaddstream = handleRemoteStreamAdded;
    // rpc.onremovestream = handleRemoteStreamRemoved;
    console.log('Created RTCPeerConnnection');
  } catch (e) {
    console.log('Failed to create PeerConnection, exception: ' + e.message);
    alert('Cannot create RTCPeerConnection object.');
    return;
  }
}

function handleIceCandidate(event) {
  console.log('icecandidate event: ', event);
  if (event.candidate) {
    sendMessage({
      type: 'candidate',
      label: event.candidate.sdpMLineIndex,
      id: event.candidate.sdpMid,
      candidate: event.candidate.candidate,
      target: event.target,
    });
  } else {
    console.log('End of candidates.');
  }
}

function doCall() {
  console.log('Sending offer to peer');
  pc.createOffer(setLocalAndSendMessage, handleCreateOfferError);
}

function doAnswer() {
  console.log('Sending answer to peer.');
  pc.createAnswer().then(
    setLocalAndSendMessage,
    onCreateSessionDescriptionError
  );
}

function setLocalAndSendMessage(sessionDescription) {
  pc.setLocalDescription(sessionDescription);
  sendMessage(sessionDescription);
}

function onCreateSessionDescriptionError(error) {
  console.log('Failed to create session description: ' + error.toString());
}

function handleRemoteStreamAdded(event) {
  console.log('Remote stream added.');
  remoteVideo = document.createElement("video"); 
  remoteVideo.autoplay = true;
  remoteVideo.playsinline = true;
  remoteVideo.setAttribute("id", "remoteVideo")
  var videos = document.getElementById("videos");
  videos.appendChild(remoteVideo);
  remoteStream = event.stream;
  remoteVideo.srcObject = remoteStream;
}

function handleCreateOfferError(event) {
  console.log('createOffer() error: ', event);
}

function sendMessage(message) {
  console.log('Client sending message: ', message);
  var content = {
      "type" : "message",
      "message" : message,
  }
  videoRoomSocket.send(JSON.stringify(content));
}

function hangup() {
  console.log('Hanging up.');
  stop();
  sendMessage('bye');
}

function handleRemoteHangup() {
  console.log('Session terminated.');
  stop();
  isInitiator = false;
}

function changeInitiator(num) {
  if (num === 1) {
    isInitiator = true
  }
}

function stop() {
  isStarted = false;
  remoteVideo.remove();
  pc.close();
  pc = null;
}
})(jQuery);