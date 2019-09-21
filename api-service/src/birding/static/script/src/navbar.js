'use strict';

class NavbarLogo extends React.Component {

  render() {
    return (
      <a href="/">
        <img
          id='navbarLogoImage'
          className='navbar-brand'
          src='/static/birdlogo-50.png'
        />
      </a>
    );
  }
}

class CollapsibleMenu extends React.Component {

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
      <div
        className="col-12 d-md-none collapse navbar-collapse"
        id="navbarSupportedContent">
        <ul className="navbar-nav mr-auto" id="collapsableMenuList">
          {this.renderItems()}
        </ul>
      </div>
    );
  }
}

export default class Navbar extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      username: null
    };
  }

  componentDidMount() {
    if (window.username) {
      this.setState({
        username: window.username
      });
    }
  }

  renderNavbarHeader() {
    if (this.state.username) {
      return (
        <div className="flex-grow-1 align-self-center">
          <NavbarLogo />
          <a
            id="headerProfileLink"
            className="text-light"
            href={`/profile/${this.state.username}`}>
            {this.state.username}
          </a>
        </div>
      );
    }
    else {
      return (
        <div className="flex-grow-1 align-self-center"><NavbarLogo /></div>
      );
    }
  }

  render() {
    return (
      <nav
        className="navbar navbar-dark fixed-top justify-content-md-center p-0 shadow bg-primary">
        <div className="navbar-main d-flex col col-md-3 mr-0">
          {this.renderNavbarHeader()}
          <button
            className="navbar-toggler d-md-none"
            type="button"
            data-toggle="collapse"
            data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent"
            aria-expanded="false"
            aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
        </div>
        <div className="px-0 d-md-block col-md-9 col-lg-6 pr-md-2 pr-lg-0">
          <form
            id="birdSearchForm"
            className="input-group input-group-lg"
            action="/bird/search"
            method="get">
            <input
              aria-describedby="button-addon"
              className="form-control form-control-light"
              name="query"
              placeholder='Search bird'
              aria-label="Search bird" />
            <div className="input-group-append">
              <button
                className="btn btn-light rounded-0"
                type="submit"
                id="button-addon">
                Search
              </button>
            </div>
          </form>
        </div>
        <div className="d-none d-lg-block col-lg-3">
        </div>
        <CollapsibleMenu items={this.props.items} />
      </nav>
    );
  }
}