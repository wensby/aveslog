import React, { Component } from 'react';
import { Link } from "react-router-dom";

export default class SideMenu extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loggedIn: false
    };
  }

  renderItems() {
    let result = []
    for (let item of this.props.items) {
      result.push(
        <div className="nav-item" key={item.text}>
          <Link className="nav-link" to={item.href}>{item.text}</Link>
        </div>
      );
    }
    return result;
  }

  render() {
    return (
      <div className="d-none d-md-block col-md-3 col-lg-2 pr-0">
        <nav className="sidebar nav flex-column border-left" id="sidebarList">
          {this.renderItems()}
        </nav>
      </div>
    );
  }
}