// import React from "react";

// const Navbar = () => {
//   return (
//     <div className="nav">
//       <img
//         src={require("../../static/assets/logo.png")}
//         alt="Logo"
//         className="logo"
//       />
//     </div>
//   );
// };

// export default Navbar;

import React from "react";
import logo from "../../static/assets/logo.png"

const Navbar = () => (
  <div className="nav">
    <img src={logo} alt="Bottega's Logo" className="logo"/>
  </div>
);

export default Navbar;