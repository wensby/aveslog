import React, { Component } from 'react';
import { Route, Link } from "react-router-dom";
import queryString from 'query-string';
import BirdService from './BirdService.js';

class BirdQueryResult extends Component {

  constructor(props) {
    super(props);
    this.state = {
      query: '',
      authenticated: false,
      resultItems: [],
    };
    this.birdService = new BirdService();
  }

  componentDidMount() {
    const query = this.getLocationQuery(this.props);
    this.doSearch(query);
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const oldQuery = prevState.query;
    const newQuery = this.getLocationQuery(this.props);
    if ( newQuery != oldQuery ) {
      this.doSearch(newQuery);
    }
  }

  async doSearch(query) {
    const response = await this.birdService.queryBirds(query);
    if (response.status === 'success') {
      const result = response.result;
      this.setState({
        query: query,
        resultItems: result,
      })
    }
  }

  getLocationQuery(props) {
    const { location } = props;
    return queryString.parse(location.search).q;
  }

  renderItemPicture = item => {
    if (item.thumbnail) {
      return <img style={{maxHeight: '150px'}} src={item.thumbnail}
        alt="Card image" />;
    }
    return (
      <img style={{maxHeight: '150px'}} src='/placeholder-bird.png'
        alt="Card image cap" />
    );
  }

  renderItemName = item => {
    return [
      <h5 key='1' className="card-title">{ item.binomialName }</h5>,
      <h6 key='2' className="card-subtitle mb-2 text-muted">{ item.binomialName }</h6>
    ];
  }

  renderAddSightingLink = item => {
    const { t } = this.props;
    const { authenticated } = this.state;
    if (authenticated) {
      return <Link to='/' className="btn btn-primary">
        { t('Add new sighting') }
      </Link>;
    }
    else {
      return null;
    }
  }

  renderItem = (item, index) => {
    return (
      <div key={index} className="card">
        <div className="card-horizontal">
          <div className="img-square-wrapper">
            <Link to='/'>
              {this.renderItemPicture(item)}
            </Link>
          </div>
          <div className="card-body">
            {this.renderItemName(item)}
            {this.renderAddSightingLink(item)}
          </div>
        </div>
      </div>
    );
  }

  renderItems = () => {
    const { resultItems } = this.state;
    return resultItems.map(this.renderItem);
  }

  render() {
    return (
      <div className="text-break">
        {this.renderItems()}
      </div>
    );
  }
  
}

export default function Bird({ match }) {
  return (
    <div>
      <Route path={`${match.path}/search`} component={BirdQueryResult}/>
    </div>
  );
}
