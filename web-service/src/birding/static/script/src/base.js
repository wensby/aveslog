'use strict';

class NavbarLogo extends React.Component {
  constructor(props) {
    super(props);
  }

  renderImg() {
    return (
      <img
        id='navbarLogoImage'
        className='navbar-brand'
        src='/static/birdlogo-50.png'
      />
    );
  }

  render() {
    return <a href="/">{this.renderImg()}</a>;
  }
}

const navbarContainer = document.querySelector('#navbarLogo');
ReactDOM.render(<NavbarLogo />, navbarContainer);