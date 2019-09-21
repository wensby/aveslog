'use strict';

export default class SideMenu extends React.Component {

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
          <a
            className="nav-link"
            href={item.href}
          >
            {item.text}
          </a>
        </div>
      );
    }
    return result;
  }

  render() {
    return (
      <div>
        <nav className="sidebar nav flex-column border-left" id="sidebarList">
          {this.renderItems()}
        </nav>
      </div>
    );
  }
}