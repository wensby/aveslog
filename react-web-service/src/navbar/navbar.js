import React, { Component } from 'react';
import { Link } from "react-router-dom";
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Nav from 'react-bootstrap/Nav';
import { Navbar as BootstrapNavbar } from "react-bootstrap";
import './navbar.css';

class SearchBar extends Component {

  renderTextInput() {
    return (
      <Form.Control
          variant='light'
          aria-describedby='button-addon'
          name='query'
          placeholder='Search bird'
          aria-label='Search bird' />
    );
  }

  renderButton() {
    return (
      <Button
          variant="light"
          className="rounded-0"
          type="submit"
          id="button-addon">
        Search
      </Button>
    );
  }

  render() {
    return (
      <Form id="birdSearchForm" action="/bird/search" method="get">
        <InputGroup size="lg">
          {this.renderTextInput()}
          <InputGroup.Append>
            {this.renderButton()}
          </InputGroup.Append>
        </InputGroup>
      </Form>
    );
  }
}

function Brand() {
  return (
    <BootstrapNavbar.Brand>
      <Link to="/">
        <img id='navbarLogoImage' src='/birdlogo-50.png' alt=''/>
      </Link>
    </BootstrapNavbar.Brand>
  );
}

class Menu extends Component {

  constructor(props) {
    super(props);
    this.wrapperRef = React.createRef();
  }

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

export default class Navbar extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      menuCollapseState: 'collapsed',
    };
    this.toggleNavbar = this.toggleNavbar.bind(this);
    this.onDocumentClick = this.onDocumentClick.bind(this);
    this.collapseMenu = this.collapseMenu.bind(this);
    this.setFullNavbarRef = this.setFullNavbarRef.bind(this);
    this.setGridRef = this.setGridRef.bind(this);
  }

  setFullNavbarRef(node) {
    this.fullNavbarRef = node;
  }

  setGridRef(node) {
    this.gridRef = node;
  }

  toggleNavbar = () => {
    if (this.state.menuCollapseState === 'collapsed') {
      this.expandMenu();
    }
    if (this.state.menuCollapseState === 'expanded') {
      this.collapseMenu();
    }
  };

  expandMenu() {
    this.setState({ menuCollapseState: 'expanding' });
    setTimeout(() => {
      if (this.state.menuCollapseState === 'expanding') {
        this.setState({ menuCollapseState: 'expanded' });
      }
    }, 300);
  }

  collapseMenu = () => {
    this.setState({ menuCollapseState: 'collapsing' });
    setTimeout(() => {
      if (this.state.menuCollapseState === 'collapsing') {
        this.setState({ menuCollapseState: 'collapsed' });
      }
    }, 300);
  }

  isMenuFullyCollapsed() {
    return this.state.menuCollapseState === 'collapsed';
  }

  isTargetOutsideNavbar(target) {
    return this.fullNavbarRef && !this.fullNavbarRef.contains(target);
  }

  isTargetInsideStaticNavbar(target) {
    return this.gridRef && this.gridRef.contains(target);
  }

  onDocumentClick = (event) => {
    if (!this.isMenuFullyCollapsed()) {
      const target = event.target;
      if (this.isTargetOutsideNavbar(target)) {
        this.collapseMenu();
        event.preventDefault();
      }
      else if (this.isTargetInsideStaticNavbar(target)) {
        this.collapseMenu();
      }
    }
  };

  componentDidMount() {
    document.addEventListener('click', this.onDocumentClick, true);
  }

  componentWillUnmount() {
    document.removeEventListener('click', this.onDocumentClick);
  }

  renderBrand() {
    return (
      <div className='navbar-main d-flex mr-0 flex-grow-1 align-self-center'>
        <Brand />
      </div>
    );
  }

  renderMenuButton() {
    return (
      <div className='menu-button'>
        <Button onClick={this.toggleNavbar} className='navbar-toggler'>
          <span className="navbar-toggler-icon"></span>
        </Button>
      </div>
    );
  }

  renderSearch() {
    return (
      <div className='search-bar-item'>
        <SearchBar />
      </div>
    );
  }

  renderCollapsibleMenu() {
    const needMaxHeight = ['expanding', 'expanded'].indexOf(this.state.menuCollapseState) >= 0; 
    const style = needMaxHeight ? {maxHeight: `${this.props.items.length * 37}px`} : {};
    return (
      <div
          className={`menu ${this.state.menuCollapseState}`}
          style={style}>
        <Menu
            items={this.props.items}
            onLinkClick={() => setTimeout(this.collapseMenu, 0)} />
      </div>
    );
  }

  render() {
    return (
      <div
          ref={this.setFullNavbarRef}
          className="navbar navbar-dark shadow p-0 bg-primary fixed-top">
        <div ref={this.setGridRef} className='grid'>
          {this.renderBrand()}
          {this.renderMenuButton()}
          {this.renderSearch()}
        </div>
        {this.renderCollapsibleMenu()}
      </div>
    );
  }
}