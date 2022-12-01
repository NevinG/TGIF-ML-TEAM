export function BillLookup(props){
    const legislative_sessions = ['781', '782', '783', '784', '78R', '791', '792', '793', '79R', '80R', '811', '81R', '821', '82R', '831', '832', '833', '83R', '84R', '851', '85R', '86R', '871', '872', '873', '87R'];
    return(
    <div>
      <div style={{display: "flex", justifyContent: "center", alignItems: "center"}}>
          <p>Legislative Session: </p>
          <select value={props.legSess} onChange={changeLegSess}>
            {legislative_sessions.map((sess, i) => <option key={i} value={sess}>{sess}</option>)}
          </select>
          <p>House or Senate Bill: </p>
          <select value={props.billType} onChange={changeBillType}>
            <option value="house_bill">House Bill</option>
            <option value="senate_bill">Senate Bill</option>
          </select>
          <p>Bill Number: </p><input value={props.billNumber} onChange={changeBillNumber} type="number"></input>
      </div>
      <div style={{display: "flex", justifyContent: "center", alignItems: "center"}}>
        <button onClick={()=> makePrediction(props.legSess, props.billType, props.billNumber)}>Make Prediction</button>
      </div>
    </div>
    
    );

    function changeLegSess(e){
        props.setLegSess(e.target.value);
    }

    function changeBillType(e){
        props.setBillType(e.target.value);
    }

    function changeBillNumber(e){
        props.setBillNumber(e.target.value);
    }

    async function makePrediction(legSess, billType, billNumber){
        if(!legSess || !billType || !billNumber)
          return

        props.setPrediction(undefined)
        let response = await fetch(`http://localhost:5000/predict_bill?leg_sess=${legSess}&bill_type=${billType}&bill_num=${billNumber}`)
        if(response.ok){
          response = await response.json();
          props.setPrediction(response.prediction);
        }
      }
}