import React, { useState, useEffect } from 'react';
import BirdService from './BirdService';

export default function BirdDetails(props) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const service = new BirdService();
      const data = await service.getBird(props.match.params.binomialName);
      setData(data);
    }
    fetchData();
  }, []);

  if (data) {
    return (
      <div className='container'>
        <div className='row picture-cover-container rounded-top overflow-hidden'
          style={{ backgroundImage: data.coverPictureUrl }}>
          <div className='col picture-cover'></div>
          <div className='w-100 d-flex justify-content-center'>
            <div className='shadow bg-white text-center pt-1 mb-0 px-2 rounded-top'>
              <h1 className='text-dark bird-page-name pb-2 mb-0'>
                { data.name }</h1>
              <p className='font-italic font-weight-light text-muted mb-0 pb-2'>
                { data.binomialName }</p>
            </div>
          </div>
        </div>
        <div className='row'>
          <div className='col'>
            <p>
              <small>{`Thumbnail Photo by: ${ data.thumbnailCredit }`}</small>
            </p>
          </div>
        </div>
      </div>
    );
  }
  else {
    return null;
  }
}
