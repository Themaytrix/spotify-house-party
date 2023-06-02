import { useState, useEffect,useContext } from "react"
import RoomItem from "./RoomItem"
import AuthContext from "../context/AuthContext"
export default function Room(){
    // setting states for rooms
    let [rooms,setRooms] = useState([])
    let {authTokens} = useContext(AuthContext) 
    // console.log(authTokens)
    let getRooms = async ()=>{
        let response = await fetch('http://127.0.0.1:8000/api/',{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
        })
        let data = await response.json()
        if (response.status === 200){
            setRooms(data)
        }
    }

    
// use effect to render rooms. dependency to be number of rooms available
    useEffect(()=>{
        getRooms()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    },[rooms.length])

    return(
        <div>
            {rooms.map((room)=>(
                <RoomItem room = {room}/>
            ))}
        </div>
    )
}