import React, { useEffect, useState } from "react";
import axios from "axios";
import ActivityChart from "./ActivityChart";
  
// Nos lo llevamos a secrets. Any es lo más feo que se le puede hacer a TS pero no atino modo de determinar que el contenido esperado es String
const API_TOKEN: string = (window as any).API_TOKEN;

const NAME = "Alexandr Gomez";
const ENDPOINT = "https://devcamp.com/api/metrics/code_editor_grouped_by_day";

interface IActivityElement {
  duration: number;
  date: string;
}

const App = () => {
  const [series, setSeries] = useState(null);
  const [dates, setDates] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getData();
  }, []);

  const getData = () => {
    axios
      .get(ENDPOINT, {
        headers: {
          "content-type": "application/json",
          Authorization: `Bearer ${API_TOKEN}`,
        },
      })
      .then((response: { data: IActivityElement[] }) => {
        if (response?.data) {
          const durations = response.data.map((stat: IActivityElement) =>
            stat.duration && stat.duration > 0
              ? (stat.duration / 3600).toFixed(2)
              : 0
          );
          setSeries([
            { name: "Coding activity", type: "area", data: durations },
          ]);
          setDates(response.data.map((stat: IActivityElement) => stat.date));
        }
        setIsLoading(false);
      })
      .catch((error) => {
        console.log("ERROR GETTING DATA", error);
      });
  };

  const content = isLoading ? (
    <div>Loading ...</div>
  ) : (
    <div>
      <div className="content__chart">
        <ActivityChart labels={dates} name={`hours`} series={series} />
      </div>
      <div className="content__title">VSCode Analytics for {NAME}</div>
    </div>
  );

  const laInfoBox = isLoading ? (
    <div>Loading ...</div>
  ) : (
    <div className="monospace">
      <div className="title">VSCode Student Analytics Dashboard</div>
      <div className="subtitle">
        <h3>Originally developed by Jordan Hudgens/Bottega, this <strong>Analytics Dashboard</strong> was a learning-focused React application.</h3>
        
        <p>The legacy version (built with <strong>React 14</strong>, <strong>Flask</strong>, and older <strong>Python 3.x</strong>) became non-functional due to:</p>
        <ul>
          <li>Compatibility issues with modern dependencies</li>
          <li>Deprecated ES5/ES6 syntax</li>
          <li>Security vulnerabilities (CVEs) in outdated packages</li>
        </ul>
        
        <p>To ensure usability and security, the app has been:</p>
        <ul>
          <li><strong>Upgraded to React 18+</strong> (fully compatible with React 19)</li>
          <li><strong>Refactored to modern ES6+/ES7+ standards</strong></li>
          <li><strong>Updated with secure, maintained dependencies</strong></li>
        </ul>
        
        <p>The migration process of this <strong>production-ready React project </strong> provided my first practical experience with React develop/deployments and some other modernization techniques.</p>
        
        <p><em>(Original reference: <a href="https://github.com/jordanhudgens/analytics-dashboard" target="_blank" rel="noopener noreferrer">Bottega Analytics Dashboard</a>)</em></p>
      </div>
    </div>
  );

  return (
    <div className="container">
      <div className="content">{content}</div>
      <div className="infoBox">{laInfoBox}</div>
    </div>
  );
};

export default App;
