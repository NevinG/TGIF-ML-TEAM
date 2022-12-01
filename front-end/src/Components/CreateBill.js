import { useState } from 'react';

export function CreateBill(props){
    const house_committees = [
"Agriculture & Livestock",
"Appropriations",
"Appropriations - S/C on Article II",
"Appropriations - S/C on Article III",
"Appropriations - S/C on Articles I, IV & V",
"Appropriations - S/C on Articles VI, VII & VIII",
"Approps. - S/C on Strategic Fiscal Rev. & Fed. Relief Funds",
"Business & Industry",
"Calendars",
"Constitutional Rights & Remedies, Select",
"Corrections",
"County Affairs",
"Criminal Jurisprudence",
"Criminal Justice Reform, Interim Study",
"Culture, Recreation & Tourism",
"Defense & Veterans' Affairs",
"Elections",
"Energy Resources",
"Environmental Regulation",
"General Investigating",
"Health Care Reform, Select",
"Higher Education",
"Homeland Security & Public Safety",
"House Administration",
"Human Services",
"Insurance",
"International Relations & Economic Development",
"Judiciary & Civil Jurisprudence",
"Juvenile Justice & Family Issues",
"Land & Resource Management",
"Licensing & Administrative Procedures",
"Local & Consent Calendars",
"Natural Resources",
"Pensions, Investments & Financial Services",
"Public Education",
"Public Health",
"Redistricting",
"Resolutions Calendars",
"State Affairs",
"The Robb Elementary Shooting, Investigative",
"Transportation",
"Urban Affairs",
"Ways & Means",
"Youth Health & Safety, Select"
    ];

const senate_committees =[
    "Administration",
    "Border Security",
    "Business & Commerce",
    "Child Protective Services, Special",
    "Committee of the Whole Senate",
    "Constitutional Issues, Special",
    "Criminal Justice",
    "Education",
    "Finance",
    "Future of College Sports in Texas, Select",
    "Health & Human Services",
    "Higher Education",
    "Jurisprudence",
    "Local Government",
    "Natural Resources & Economic Development",
    "Nominations",
    "Ports, Select",
    "Redistricting, Special",
    "State Affairs",
    "To Protect All Texans, Special",
    "Transportation",
    "Veteran Affairs",
    "Water, Agriculture & Rural Affairs",
       
];

    const [jointAuthors, setjointAuthors] = useState(0);
    const [coAuthors, setCoAuthors] = useState(0);
    const [numOfSubjects, setnumOfSubjects] = useState(0);
    const [committee, setCommittee] = useState('Agriculture & Livestock');

    return(
        <div>
            <div style={{display: "flex", justifyContent: "center", alignItems: "center"}}>
                <p>House or Senate Bill: </p>
                <select value={props.billType} onChange={changeBillType}>
                    <option value="house_bill">House Bill</option>
                    <option value="senate_bill">Senate Bill</option>
                </select>
                <p>Number of joint authors: </p><input value={jointAuthors} onChange={changejointAuthors} style={{width: 50 }} type="number"></input>
                <p>Number of co authors: </p><input value={coAuthors} onChange={changeCoAuthors} style={{width: 50 }} type="number"></input>
                <p>Number of subjects: </p><input value={numOfSubjects} onChange={changenumOfSubjects} style={{width: 50 }} type="number"></input>
                <p>Committee: </p>
                <select value={committee} onChange={changeCommittee} style={{width: "200px"}}>
                {
                    props.billType == "senate_bill" ? 
                    senate_committees.map((sess, i) => <option key={i} value={sess}>{sess}</option>)
                    :
                    house_committees.map((sess, i) => <option key={i} value={sess}>{sess}</option>)
                }
                </select>
            </div>
            <div style={{display: "flex", justifyContent: "center", alignItems: "center"}}>
                <button onClick={()=> makePrediction(committee, props.billType, jointAuthors, coAuthors, numOfSubjects)}>Make Prediction</button>
            </div>
        </div>
    )

    async function makePrediction(committee, billType, jointAuthors, coAuthors, numOfSubjects){
        props.setPrediction(undefined)
        let response = await fetch(`http://localhost:5000/predict_bill_create?committee=${committee}&bill_type=${billType}&joint_authors=${jointAuthors}&co_authors=${coAuthors}&num_of_subjects=${numOfSubjects}`)
        if(response.ok){
          response = await response.json();
          props.setPrediction(response.prediction);
        }
    }
    
    function changeCommittee(e){
        setCommittee(e.target.value);
    }

    function changeBillType(e){
        props.setBillType(e.target.value);
    }

    function changejointAuthors(e){
        setjointAuthors(e.target.value);
    }
    function changeCoAuthors(e){
        setCoAuthors(e.target.value);
    }
    function changenumOfSubjects(e){
        setnumOfSubjects(e.target.value);
    }

}