(function($){
    var localVideo = document.querySelector('#localVideo');
var remoteVideo;
const startButton = document.getElementById('startButton');
console.log("video open");

var remoteStream;
var localStream;
var isInitiator = false;
var user_name = Math.random().toString(36).substr(2)
var pc_list = {};



const videoRoomName = JSON.parse(document.getElementById('room-name').textContent);

  var ws_or_wss;
  if (location.protocol == 'http:') {
    ws_or_wss = 'ws://'
  } else if (location.protocol == 'https:') {
    ws_or_wss = 'wss://'
  }

const videoRoomSocket = new WebSocket(
                 ws_or_wss
                + window.location.host
                + '/ws/webrtc/'
                + videoRoomName
                + '/'
            );

videoRoomSocket.onopen = function(e) {
  videoRoomSocket.send(JSON.stringify({
  "type": "join",
  "user_name": user_name
}));
}

window.onbeforeunload = function(event){
  videoRoomSocket.send(JSON.stringify({
  "type": "bye",
  "from": user_name,
  "to": "all"
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
  if (data.type === 'bye') {
    if (data.from !== user_name) {
      stop(data.from);
    }
    return;
  }
  if (data.message == "create") {
    console.log("pertitipants number: ", data.number);
    console.log("room_name: ", data.room_name);
      isInitiator = true;
      return
    }
  if (data.message == "join" && !isInitiator) {
    console.log("user_name: ", data.user_name);
    if (data.user_name !== user_name) {
      videoRoomSocket.send(JSON.stringify({
        "type": "hello",
        "to": data.user_name,
        "from": user_name
      }));
      return;
    }
    return
  }
  if (data.message == "hello") {
  if (data.to == user_name) {
    createPeerConnection(data.from);
    doCall(data.from, data.to, pc_list[data.from]);
    console.log("start from: ", user_name);
  } else {
    if (data.from == user_name) {
      createPeerConnection(data.to);
      console.log("recieve :", user_name);
    }
  }
  return
  }
  if (data.message === 'got user media') {
      console.log('got user media');
    maybeStart();
  } else if (data.message.type === 'offer') {
    console.log("offer data: ", data);
    if (data.to == user_name) {
      console.log('remote description', data.message);
      pc_list[data.from].setRemoteDescription(new RTCSessionDescription(data.message));
      doAnswer(data.from, data.to, pc_list[data.from]);
    }
  } else if (data.message.type === 'answer') {
    if (data.to == user_name) {
      console.log("recieved answer");
      pc_list[data.from].setRemoteDescription(new RTCSessionDescription(data.message));
    }
  } else if (data.message.type === 'candidate') {
    if (data.to === user_name || data.from === user_name) {
      var name = data.to === user_name ? data.from : data.to;
      if (pc_list[name] !== data.message.target) {
        console.log("candidate", data.message.candidate);
        var candidate = new RTCIceCandidate({
          sdpMLineIndex: data.message.label,
          candidate: data.message.candidate
        });
        pc.addIceCandidate(candidate);
      }
    }
  }
};

function createPeerConnection(name) {
  try {
    pc = new RTCPeerConnection(null);
    pc.addEventListener('addstream', function(event) {
      handleRemoteStreamAdded(event, name);
    })
    
    pc.addEventListener('isolationchange', function(event) {
      console.log(event);
    })
    pc.addEventListener('icecandidate', function(event) {
      console.log('icecandidate event: ', event);
      if (event.candidate) {
        sendMessage({
          type: 'candidate',
          label: event.candidate.sdpMLineIndex,
          id: event.candidate.sdpMid,
          candidate: event.candidate.candidate,
          target: event.target,
        }, 
        name,
        user_name
        );
      } else {
        console.log('End of candidates.');
      }
    })
    // pc.onicecandidate = handleIceCandidate;
    // rpc.onremovestream = handleRemoteStreamRemoved;
    pc.addEventListener('iceconnectionstatechange', () => {
      pc.iceConnectionState;
      if (pc.iceConnectionState == "disconnected" || pc.iceConnectionState == "failed") {
        console.log(`${name} connection: `, pc.iceConnectionState);
        stop(name);
      }
      console.log(`${name} connection: `, pc.iceConnectionState);
    });
    console.log('signalingstate: ', pc.signalingState);
    pc.addEventListener('signalingstatechange', () => {
      console.log('signalingstate: ', pc.signalingState);
      signalingState = pc.signalingState;
    });
    pc.addStream(localStream);
    pc_list[name] = pc;
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

function doCall(to, from, pc) {
  console.log('Sending offer to peer');
  pc.createOffer().then(function(sessionDescription) {
    pc.setLocalDescription(sessionDescription);
    sendMessage(sessionDescription, to, from);
    return;
  });
}

function doAnswer(to, from, pc) {
  console.log('Sending answer to peer.');
  pc.createAnswer().then(function(sessionDescription) {
    pc.setLocalDescription(sessionDescription);
    sendMessage(sessionDescription, to, from);
    return;
  });
}

function onCreateSessionDescriptionError(error) {
  console.log('Failed to create session description: ' + error.toString());
}

function handleRemoteStreamAdded(event, name) {
  console.log('Remote stream added.');
  remoteVideo = document.createElement("video"); 
  remoteVideo.autoplay = true;
  remoteVideo.playsinline = true;
  remoteVideo.setAttribute("id", name)
  var videos = document.getElementById("videos");
  videos.appendChild(remoteVideo);
  remoteStream = event.stream;
  remoteVideo.srcObject = remoteStream;
}

function handleCreateOfferError(event) {
  console.log('createOffer() error: ', event);
}

function sendMessage(message, to, from) {
  console.log('Client sending message: ', message);
  var content = {
      "type" : "message",
      "message" : message,
      "to": to,
      "from": from,
  }
  videoRoomSocket.send(JSON.stringify(content));
}

function stop(name) {
  console.log(`Connection with ${name} was over`);
  document.getElementById(name).remove();
  pc_list[name].close();
  delete pc_list[name];
}
})(jQuery);