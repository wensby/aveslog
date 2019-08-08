import React, { Component } from 'react';
import { Link } from "react-router-dom";
import Nav from 'react-bootstrap/Nav';
import './navbar.css';

export default class Menu extends Component {

  renderItems() {
    let result = [];
    for (let item of this.props.items) {
      result.push(
        <div className="nav-item" key={item.text}>
          <Link
              className="nav-link"
              to={item.href}
              onClick={() => {
                this.props.onLinkClick();
              }}>
            {item.text}
          </Link>
        </div>
      );
    }
    return result;
  }

  render() {
    return (
        <Nav className='navbar-nav mr-auto' id='collapsableMenuList'>
          {this.renderItems()}
        </Nav>
    );
  }
}