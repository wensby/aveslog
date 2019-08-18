import React, { Component } from 'react';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import { withTranslation } from "react-i18next";
import { Redirect, withRouter } from 'react-router-dom';

class SearchBar extends Component {

  constructor(props) {
    super(props);
    this.state = {
      query: '',
      redirect: false,
    }
  }

  renderTextInput = () => {
    const { t } = this.props;
    return (
      <Form.Control variant='light' aria-describedby='button-addon'
        name='query' placeholder={t('Search bird')} aria-label='Search bird'
        onChange={event => this.setState({query: event.target.value})}
        value={this.state.query}/>
    );
  };

  renderButton = () => {
    const { t } = this.props;
    return (
      <Button variant="light" className="rounded-0" type="submit"
        id="button-addon">{t('Search')}</Button>
    );
  };

  onFormSubmit = event => {
    const { query } = this.state;
    event.preventDefault();
    this.props.history.push(`/bird/search?q=${query}`);
    this.setState({query: ''});
  }

  render() {
    const { query, redirect } = this.state;

    if (redirect) {
        return <Redirect to={`/bird?q=${query}`} />
    }
    return (
      <form id="birdSearchForm" onSubmit={this.onFormSubmit}>
        <InputGroup size="lg">
          {this.renderTextInput()}
          <InputGroup.Append>
            {this.renderButton()}
          </InputGroup.Append>
        </InputGroup>
      </form>
    );
  }
}

export default withRouter(withTranslation()(SearchBar));
