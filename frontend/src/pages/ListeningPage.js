import { useContext, useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import AuthContext from "../context/AuthContext"

export default function ListeningPage(){
    let [activeRoom, setActiveRoom] = useState([])
    let {authTokens} = useContext(AuthContext)
    let {id} = useParams()
    
    console.log(id)

    let getRoomInfo = async ()=>{

        let response = await fetch(`http://127.0.0.1:8000/api/${id}`,{
            method:'GET',
            headers:{
                'Content-Type':'application/json',
                'Authorization': 'Bearer ' + String(authTokens.access)
            },
        })

        let data = await response.json()
        if(response.ok){
            setActiveRoom(data)
        }
    }

    useEffect(()=>{
        getRoomInfo()
    },[activeRoom.name])

    return(
        <div>
            <h3>{activeRoom.name}</h3>
        </div>
    )
}