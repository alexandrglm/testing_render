import * as React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./components/App"

const root = ReactDOM.createRoot(

    document.getElementById('root') as HTMLElement

);

root.render(
<BrowserRouter>
    <div className="container-app">
        <App />
    </div>
</BrowserRouter>
);