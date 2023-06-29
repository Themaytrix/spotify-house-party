import { useContext} from "react"
import AuthContext from "../context/AuthContext"
import { useNavigate } from "react-router-dom"

export default function RoomItem(props){
    let {authTokens} =useContext(AuthContext)

    let navigate = useNavigate()
    let joinRoom = async (e)=>{
        e.preventDefault()
        let response = await fetch(`http://127.0.0.1:8000/api/${props.room.id_session}/`,{
            method: 'POST',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
            body:JSON.stringify({'id_session': String(props.room.id_session)})
        })

        let data = await response.json()
        if(response.ok){
            localStorage.setItem('room_key',data.id_session)
            navigate(`/:${data.id_session}`)
        }
    }

    return(
        <div>
        
            <h4>{props.room.name}</h4>
            <button onClick={joinRoom}>Join Room</button>
        
        </div>
    )
}