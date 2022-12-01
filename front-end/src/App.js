import './App.css';
import { useState } from 'react';
import {BillLookup} from './Components/BillLookup.js'
import {CreateBill} from './Components/CreateBill.js'

function App() {
  const [prediction, setPrediction] = useState();
  const [legSess, setLegSess] = useState('781');
  const [billType, setBillType] = useState('house_bill');
  const [billNumber, setBillNumber] = useState(1);
  const [inputToggle, setInputToggle] = useState('lookup');


  function onInputToggleChange(e){
    setInputToggle(e.target.value);
  }

  return (
    <div>
      <h1 style={{textAlign: "center"}}>Bill Data Prediction</h1>
      <div id="group1" onChange={onInputToggleChange} style={{display: 'flex', textAlign: 'center', justifyContent: 'center'}}>
        <input type="radio" value="lookup" name="inputToggle" checked={inputToggle === 'lookup'}/> Bill Lookup
        <input type="radio" value="createOwn" name="inputToggle" checked={inputToggle === 'createOwn'}/> Create Own Bill
      </div>
      {
        inputToggle === "lookup" &&
        <BillLookup 
          legSess={legSess} 
          billType={billType} 
          billNumber = {billNumber} 
          prediction={prediction} 
          setLegSess={setLegSess} 
          setBillType={setBillType} 
          setBillNumber={setBillNumber} 
          setPrediction={setPrediction}
        />
      }
      {
        inputToggle === "createOwn" &&
        <CreateBill
          legSess={legSess} 
          billType={billType} 
          prediction={prediction} 
          setLegSess={setLegSess} 
          setBillType={setBillType} 
          setPrediction={setPrediction}
        />
      }

      <p style={{textAlign: "center"}}>{prediction && `This bill has a ${prediction} chance to pass`}</p>
    </div>
  );
}

export default App;
