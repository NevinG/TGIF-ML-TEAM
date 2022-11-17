import './App.css';
import { useState } from 'react';
import { queryAllByDisplayValue } from '@testing-library/react';

function App() {
  const [prediction, setPrediction] = useState();
  const [legSess, setLegSess] = useState('781');
  const [billType, setBillType] = useState('house_bill');
  const [billNumber, setBillNumber] = useState(1);

  const legislative_sessions = ['781', '782', '783', '784', '78R', '791', '792', '793', '79R', '80R', '811', '81R', '821', '82R', '831', '832', '833', '83R', '84R', '851', '85R', '86R', '871', '872', '873', '87R'];
  return (
    <div>
      <h1 style={{textAlign: "center"}}>ARE THESE NUMBERS UP THE STANDARD OF THE MIGHT TEXAS LEGISLATURE</h1>
      <div style={{display: "flex", justifyContent: "center", alignItems: "center"}}>
        <p>Legislative Session: </p>
        <select value={legSess} onChange={changeLegSess}>
          {legislative_sessions.map((sess, i) => <option key={i} value={sess}>{sess}</option>)}
        </select>
        <p>House or Senate Bill: </p>
        <select value={billType} onChange={changeBillType}>
          <option value="house_bill">House Bill</option>
          <option value="senate_bill">Senate Bill</option>
        </select>
        <p>Bill Number: </p><input value={billNumber} onChange={changeBillNumber} type="number"></input>
        <button onClick={()=> makePrediction(legSess, billType, billNumber)}>Make Prediction</button>
      </div>
      <h4 style={{textAlign: "center"}}>{prediction && `This bill has a ${prediction} chance to pass`}</h4>
    </div>
  );

  async function makePrediction(legSess, billType, billNumber){
    if(!legSess || !queryAllByDisplayValue || !billNumber)
      return

    let response = await fetch(`http://localhost:5000/predict_bill?leg_sess=${legSess}&bill_type=${billType}&bill_num=${billNumber}`)
    if(response.ok){
      response = await response.json();
      setPrediction(response.prediction);
    }
  }

  function changeLegSess(e){
    setLegSess(e.target.value);
  }

  function changeBillType(e){
    setBillType(e.target.value);
  }

  function changeBillNumber(e){
    setBillNumber(e.target.value);
  }
}

export default App;
