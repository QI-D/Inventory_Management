import React, { useEffect, useState } from 'react'
import '../App.css';

export default function EndpointHealth() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [status, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStatus = () => {
	
        fetch(`http://ec2-34-234-41-89.compute-1.amazonaws.com:8120/health`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Health Check")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }

    useEffect(() => {
		const interval = setInterval(() => getStatus(), 10000); // Update every 10 seconds
		return() => clearInterval(interval);
    }, [getStatus]);


    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        let last_updated = new Date(status['last_updated'].replace("T", " ").replace("Z", " "));
        last_updated.setHours(last_updated.getHours() - 8) // fix time zone
        let curr_time = new Date()
        let time = Math.round((curr_time - last_updated) / 1000)
        return(
            <div>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
                            <td>Receiver:</td>
							<td>{status['receiver']}</td>
						</tr>
                        <tr>
                            <td>Storage:</td>
                            <td>{status['storage']}</td>
                        </tr>
                        <tr>
                            <td>Processing:</td>
                            <td>{status['processing']}</td>
                        </tr>
                        <tr>
                            <td>Audit Log:</td>
                            <td>{status['audit']}</td>
                        </tr>
                        <tr>
                            <td>Last Updated:</td>
                            <td>{time}s ago</td>
                        </tr>
					</tbody>
                </table>

            </div>
        )
    }
}
