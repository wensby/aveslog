'use strict';

import Navbar from './navbar.js';
import SideMenu from './sidemenu.js'

ReactDOM.render(<Navbar items={window.menuItems}/>, document.querySelector('#navbar'));
ReactDOM.render(<SideMenu items={window.menuItems}/>, document.querySelector('#sidemenu'));