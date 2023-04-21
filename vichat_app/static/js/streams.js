const APP_ID = '799d41afa2fc4509910c57a9579fad27'
const CHANNEL = sessionStorage.getItem('room')
const TOKEN = sessionStorage.getItem('token')
let UID = Number(sessionStorage.getItem('UID'))

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' })

let localTracks = []
let remoteUsers = {}

async function joinAndDisplayLocalStream() {

  //handling someone joining the room
  client.on('user-published', handleUserJoined)

  //removing the AV tracks and DOM element when someone leaves
  client.on('user-left', handleUserLeaving)

  await client.join(APP_ID, CHANNEL, TOKEN, UID)

  localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

  //HTML of the player with unique id for each user to check if they're already here
  let player = `<div class="video-container" id="user-container-${UID}">
                    <div class="username-wrapper"><span class="user-name"></span></div>
                    <div class="video-player" id="user-${UID}"></div>
                  </div>`

  document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)


  localTracks[1].play(`user-${UID}`)

  await client.publish([localTracks[0], localTracks[1]])
}

async function handleUserJoined(user, mediaType) {
  remoteUsers[user.uid] = user
  await client.subscribe(user, mediaType)

  if (mediaType == 'video') {
    let player = document.getElementById(`user-container-${user.uid}`)
    if (player != null) {
      player.remove()
    }

    player = `<div class="video-container" id="user-container-${user.uid}">
                    <div class="username-wrapper"><span class="user-name"></span></div>
                    <div class="video-player" id="user-${user.uid}"></div>
                  </div>`

    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
    user.videoTrack.play(`user-${user.uid}`)
  }

  if (mediaType == 'audio') {
    user.audioTrack.play()
  }
}


//callback function for when someone leaves
async function handleUserLeaving(user) {
  delete remoteUsers[user.uid]
  document.getElementById(`user-container-${user.uid}`).remove()

}

async function toggleVideo(e){
  if(localTracks[1].muted){
    await localTracks[1].setMuted(false)
    e.target.style.backgroundColor = '#3b82f6'
  } else{
    await localTracks[1].setMuted(true)
    e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
   
  }
}
async function toggleAudio(e){
  if(localTracks[0].muted){
    await localTracks[0].setMuted(false)
    e.target.style.backgroundColor = '#3b82f6'
    
  } else{
    await localTracks[0].setMuted(true)
    e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
  }
}

document.getElementById('camera-btn').addEventListener('click', toggleVideo)
document.getElementById('mic-btn').addEventListener('click', toggleAudio)


joinAndDisplayLocalStream()
