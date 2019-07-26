import 'bootstrap/dist/css/bootstrap.css';
import './index.css';

import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Navbar from './navbar/navbar.js';
import SideMenu from './sidemenu.js';
import Login from './authentication.js'
import './App.css';


class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      menuItems: [
        {
          href: '/authentication/login',
          text: 'Login'
        },
        {
          href: '/settings/',
          text: 'Settings'
        }
      ],
    };
  }

  render() {
    return (
      <Router>
        <Container>
          <Navbar items={this.state.menuItems}/>
          <div className="container-fluid navbar-pushed">
            <Row>
              <SideMenu items={this.state.menuItems} />
              <main role="main" className="col-12 col-md-9 col-lg-8">
                <Route path="/authentication/login" exact component={Login} />
              </main>
              <div className="d-none d-lg-block col-lg-2"></div>
            </Row>
          </div>
        </Container>
      </Router>
    );
  }
}

export default App;
