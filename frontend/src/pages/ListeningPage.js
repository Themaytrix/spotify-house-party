import { useContext, useEffect, useState } from "react"
import { useParams,useNavigate } from "react-router-dom"
import AuthContext from "../context/AuthContext"
import Player from "../components/Player"

export default function ListeningPage(){
    let [activeRoom, setActiveRoom] = useState([])
    let [spotifyAuthenticated,setSpotifyAuthenticated] = useState(()=>(Boolean(localStorage.getItem('spotify_authenticated'))))
    let {authTokens,user} = useContext(AuthContext)
    let {id} = useParams()
    let roomCalled = false
    
    let isHost = activeRoom.host === user.user_id ? true : false
    let navigate = useNavigate()

    let getOptions = {
        method:'GET',
        headers:{
            'Content-Type':'application/json',
            'Authorization': 'Bearer ' + String(authTokens.access)
        },
    }

    let getRoomInfo = async ()=>{

        let response = await fetch(`http://127.0.0.1:8000/api/${id}/`,getOptions)

        let data = await response.json()
        if(response.ok){
            setActiveRoom(data)
            if(isHost){

                spotifyAuthenticate()
                if(spotifyAuthenticated){
                    streamSong()
                }
            
                if(!spotifyAuthenticated){
                    // get auth url
                    getAuthUrl()
    
                }
            }else{
                streamSong()
            }
            

        }
    }

    let getAuthUrl = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/spotify/get-auth-url/',getOptions)
        
        let data = await response.json()
        if(response.ok){
            console.log(data.url)
            window.location.replace(`${data.url}`)
            
        }
    }

    let spotifyAuthenticate = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/spotify/is-authenticated/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
            body: JSON.stringify({'id_session':localStorage.getItem('room_key')})

        })

        let data = await response.json()
        if(response.ok){
            console.log(data.status)
            localStorage.setItem('spotify_authenticated',data.status)
            
        }
    }


    let leaveRoom = async (e)=>{
        e.preventDefault()
        let response = await fetch('http://127.0.0.1:8000/api/leave-room/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })

        let data = await response.json()
        if(response.ok){
            localStorage.removeItem('room_key')
            navigate('/')
        }
    }

    let endRoom = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/api/delete-room/',{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
            body:JSON.stringify({"id_session":id})
        })
        
        let data = await response.json()
        if(response.ok){
            localStorage.removeItem('room_key')
            navigate('/')
        }
    }


    let streamSong = ()=>{
        const streamSocket = new WebSocket(`ws://127.0.0.1:8000/ws/spotify/${id}/`)

        streamSocket.onopen = (e) =>{
            console.log('hmmm')
            streamSocket.send(JSON.stringify({
                'message': true
            }))
            
        }
        streamSocket.onmessage = (e) =>{
            console.log("receiving...")
            const data = JSON.parse(e.data)
            console.log(data)

        }
        streamSocket.onclose = (e) =>{
            
            console.log("close...")
    
        }

    }



    // getting room info
    useEffect(()=>{

        getRoomInfo()
        
        return ()=> roomCalled = true
    },[activeRoom.name])

 
    //spotify api 
    // useEffect(()=>{
    //     getPlaying()
    // },[roomCalled])
    return(
        <div>
            <h3>{activeRoom.name}</h3>

            { isHost ? 
            <div>
                <button onClick={endRoom}>End Room</button>
            </div> : <div>
                <button onClick={leaveRoom}>Leave Room</button>
            </div>
            }

            {/* <div>
                <Player roomId={id}
                />
            </div> */}
        </div>
    )
}