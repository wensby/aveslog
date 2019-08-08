import React, { Component } from 'react';

export default class SideMenu extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loggedIn: false
    };
  }

  renderItem = (item, index) => {
    return (
      <div className="nav-item" key={index}>
        {item}
      </div>
    );
  }

  render() {
    return (
      <div className="sidemenu">
        <nav className="sidebar nav flex-column border-left" id="sidebarList">
          {this.props.items.map(this.renderItem)}
        </nav>
      </div>
    );
  }
}